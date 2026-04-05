import re
import unittest
from dataclasses import dataclass, field as dataclass_field
from typing import Dict, List, Set


PLACEHOLDER_RE = re.compile(r"\{[A-Za-z_][A-Za-z0-9_]*\}")
ID_RE = re.compile(r"\b(?:P|EXP|PAT|SUBJ)-?\d{2,}\b", re.IGNORECASE)
PATH_RE = re.compile(r"(?:[A-Za-z]:\\|/)[^\s]+")


@dataclass
class ScenarioConfig:
    share_target: str
    doc_type: str
    field: str = "computer-science"
    lab_name: str = "VisionLab"
    aliases: List[str] = dataclass_field(default_factory=lambda: ["VisionLab", "visionlab", "VLab"])
    internal_platform_aliases: List[str] = dataclass_field(default_factory=lambda: ["VisionLab Notion", "VLab Drive"])
    meeting_aliases: List[str] = dataclass_field(default_factory=lambda: ["VisionLab组会", "VLab Weekly"])
    repo_aliases: List[str] = dataclass_field(default_factory=lambda: ["visionlab-train", "vlab-shared-repo"])


class SkillScenarioHarness:
    retention_terms: Dict[str, List[str]] = {
        "new-member-onboarding": ["环境", "权限", "安全", "禁止", "数据"],
        "internal-handoff": ["状态", "步骤", "依赖", "风险"],
        "lab-knowledge-base": ["流程", "输入", "输出", "术语"],
        "course-presentation": ["背景", "方法", "结论", "局限"],
    }

    def classify(self, text: str, config: ScenarioConfig) -> str:
        normalized = text.lower()

        if self._contains_alias(text, config):
            return "MASK"
        if PLACEHOLDER_RE.search(text) or ID_RE.search(text) or PATH_RE.search(text):
            return "MASK"
        if self._is_critical(text, config):
            return "KEEP-CRITICAL"
        if self._is_unpublished_or_local(text, config):
            return "REMOVE"
        if self._is_review_gray_zone(text, config):
            return "REVIEW"
        if self._is_dilutable(text):
            return "DILUTE"
        if any(token in normalized for token in ["baseline", "评估指标", "随机种子", "method", "结果"]):
            return "SAFE"
        return "SAFE"

    def validate(self, source_text: str, cleaned_text: str, config: ScenarioConfig) -> Set[str]:
        failed_layers: Set[str] = set()
        source_categories = self._extract_categories(source_text)
        cleaned_categories = self._extract_categories(cleaned_text)

        if self._contains_alias(cleaned_text, config):
            failed_layers.add("leakage")
        if PLACEHOLDER_RE.search(cleaned_text) or ID_RE.search(cleaned_text) or PATH_RE.search(cleaned_text):
            failed_layers.add("leakage")

        for token in self.retention_terms.get(config.share_target, []):
            if token in source_categories and token not in cleaned_categories:
                failed_layers.add("usefulness")

        if {"IRB", "consent", "伦理", "隐私"} & source_categories and not (
            {"IRB", "consent", "伦理", "隐私"} & cleaned_categories
        ):
            failed_layers.add("compliance")

        if "安全" in source_categories and "安全" not in cleaned_categories:
            failed_layers.add("compliance")

        return failed_layers

    def review_fallback_action(self, config: ScenarioConfig) -> str:
        if config.share_target == "new-member-onboarding":
            return "keep_or_mask"
        if config.share_target == "course-presentation":
            return "remove_or_mask"
        if config.share_target == "internal-handoff":
            return "dilute_or_keep"
        return "dilute"

    def _contains_alias(self, text: str, config: ScenarioConfig) -> bool:
        dictionaries = (
            config.aliases
            + config.internal_platform_aliases
            + config.meeting_aliases
            + config.repo_aliases
        )
        return any(alias.lower() in text.lower() for alias in dictionaries)

    def _is_critical(self, text: str, config: ScenarioConfig) -> bool:
        critical_terms = ["权限", "安全", "禁止", "IRB", "伦理", "consent", "隐私", "数据访问"]
        onboarding_terms = ["环境", "安装", "前置条件", "最小步骤"]
        if any(term.lower() in text.lower() for term in critical_terms):
            return True
        if config.doc_type == "onboarding-doc" and any(
            term.lower() in text.lower() for term in onboarding_terms
        ):
            return True
        return False

    def _is_unpublished_or_local(self, text: str, config: ScenarioConfig) -> bool:
        unpublished_markers = ["下一步", "我们怀疑", "未发表", "备选方向", "reviewer", "bottleneck"]
        local_markers = ["本组", "组内", "实验室内部", "内部流程"]
        if config.share_target == "course-presentation" and any(
            marker.lower() in text.lower() for marker in unpublished_markers + local_markers
        ):
            return True
        return False

    def _is_review_gray_zone(self, text: str, config: ScenarioConfig) -> bool:
        review_markers = ["默认先找", "谁最好说话", "避开", "组会怎么避雷", "老师一打断"]
        if any(marker in text for marker in review_markers):
            return True
        if config.share_target == "internal-handoff" and "联系人" in text:
            return True
        return False

    def _is_dilutable(self, text: str) -> bool:
        dilutable_markers = ["优先核查", "汇报原则", "一般性建议", "职业化沟通"]
        return any(marker in text for marker in dilutable_markers)

    def _extract_categories(self, text: str) -> Set[str]:
        categories: Set[str] = set()
        mapping = {
            "环境": ["环境", "安装", "setup"],
            "权限": ["权限", "访问", "申请"],
            "安全": ["安全", "培训", "危险"],
            "禁止": ["禁止", "不得", "不可"],
            "数据": ["数据", "样本", "participant"],
            "状态": ["状态", "当前任务"],
            "步骤": ["步骤", "执行路径", "复现"],
            "依赖": ["依赖", "公共依赖"],
            "风险": ["风险", "已知问题"],
            "IRB": ["IRB"],
            "consent": ["consent", "知情同意"],
            "伦理": ["伦理"],
            "隐私": ["隐私", "去标识化"],
        }
        lowered = text.lower()
        for category, markers in mapping.items():
            if any(marker.lower() in lowered for marker in markers):
                categories.add(category)
        return categories


class TemplateScenarioTests(unittest.TestCase):
    def setUp(self) -> None:
        self.harness = SkillScenarioHarness()

    def test_onboarding_permission_snippet_is_keep_critical(self) -> None:
        config = ScenarioConfig(share_target="new-member-onboarding", doc_type="onboarding-doc")
        text = "训练前必须先申请数据访问权限并完成安全培训。"
        self.assertEqual(self.harness.classify(text, config), "KEEP-CRITICAL")

    def test_course_presentation_unpublished_direction_is_remove(self) -> None:
        config = ScenarioConfig(share_target="course-presentation", doc_type="research-skill")
        text = "下一步准备转向跨域设定，因为我们怀疑核心瓶颈不在当前 backbone。"
        self.assertEqual(self.harness.classify(text, config), "REMOVE")

    def test_lab_alias_and_internal_platform_are_masked(self) -> None:
        config = ScenarioConfig(share_target="lab-knowledge-base", doc_type="general-research-doc")
        text = "周三前发到 VisionLab Notion，由 VisionLab组会先过一遍。"
        self.assertEqual(self.harness.classify(text, config), "MASK")

    def test_advisor_interaction_gray_zone_is_review(self) -> None:
        config = ScenarioConfig(share_target="new-member-onboarding", doc_type="persona")
        text = "默认先找带教博士生确认组会汇报方向，老师一打断就先切结论。"
        self.assertEqual(self.harness.classify(text, config), "REVIEW")

    def test_generic_methodology_statement_is_safe(self) -> None:
        config = ScenarioConfig(share_target="lab-knowledge-base", doc_type="research-skill")
        text = "先复现 baseline，再记录随机种子、评估指标和结果。"
        self.assertEqual(self.harness.classify(text, config), "SAFE")

    def test_leakage_validation_fails_on_alias_and_placeholder_residue(self) -> None:
        config = ScenarioConfig(share_target="lab-knowledge-base", doc_type="general-research-doc")
        source = "由 VisionLab Notion 维护共享流程，提交前联系 {advisor_role}。"
        cleaned = "由 VisionLab Notion 维护共享流程，提交前联系 {advisor_role}。"
        self.assertEqual(self.harness.validate(source, cleaned, config), {"leakage"})

    def test_onboarding_output_missing_safety_and_permission_fails(self) -> None:
        config = ScenarioConfig(share_target="new-member-onboarding", doc_type="onboarding-doc")
        source = "训练前必须先申请数据访问权限并完成安全培训，禁止直接导出原始数据。"
        cleaned = "开始实验前先准备开发环境，并阅读公开文档。"
        self.assertEqual(self.harness.validate(source, cleaned, config), {"usefulness", "compliance"})

    def test_human_subjects_output_with_irb_and_consent_passes(self) -> None:
        config = ScenarioConfig(
            share_target="lab-knowledge-base",
            doc_type="general-research-doc",
            field="human-subjects",
        )
        source = "涉及 participant 数据时，必须满足 IRB、知情同意和隐私保护要求。"
        cleaned = "涉及 participant 数据时，必须满足 IRB、知情同意和隐私保护要求。"
        self.assertEqual(self.harness.validate(source, cleaned, config), set())

    def test_internal_handoff_missing_execution_path_fails_usefulness(self) -> None:
        config = ScenarioConfig(share_target="internal-handoff", doc_type="research-skill")
        source = "当前任务状态：数据清洗已完成。最低执行路径：先拉取依赖，再运行预处理步骤。"
        cleaned = "当前任务状态：数据清洗已完成。"
        self.assertEqual(self.harness.validate(source, cleaned, config), {"usefulness"})

    def test_review_fallback_actions_are_share_target_specific(self) -> None:
        self.assertEqual(
            self.harness.review_fallback_action(
                ScenarioConfig(share_target="new-member-onboarding", doc_type="onboarding-doc")
            ),
            "keep_or_mask",
        )
        self.assertEqual(
            self.harness.review_fallback_action(
                ScenarioConfig(share_target="course-presentation", doc_type="general-research-doc")
            ),
            "remove_or_mask",
        )
        self.assertEqual(
            self.harness.review_fallback_action(
                ScenarioConfig(share_target="internal-handoff", doc_type="research-skill")
            ),
            "dilute_or_keep",
        )


if __name__ == "__main__":
    unittest.main()

