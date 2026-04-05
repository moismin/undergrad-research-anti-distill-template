import re
import unittest
from pathlib import Path


TEMPLATE_ROOT = Path(__file__).resolve().parents[1]
SHARED_ROOT = TEMPLATE_ROOT / "shared"
CODEX_ROOT = TEMPLATE_ROOT / "codex"
CLAUDE_ROOT = TEMPLATE_ROOT / "claude"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
    if not match:
        raise AssertionError(f"Missing section: {heading}")
    return match.group(1)


class TemplateConsistencyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.skill_core = read_text(SHARED_ROOT / "skill-core.md")
        self.decision_profiles = read_text(SHARED_ROOT / "decision-profiles.md")
        self.field_profiles = read_text(SHARED_ROOT / "field-profiles.md")
        self.shared_classifier = read_text(SHARED_ROOT / "prompts" / "classifier.md")
        self.codex_skill = read_text(CODEX_ROOT / "SKILL.md")
        self.claude_skill = read_text(CLAUDE_ROOT / "SKILL.md")

    def test_required_shared_files_exist(self) -> None:
        expected_files = [
            SHARED_ROOT / "skill-core.md",
            SHARED_ROOT / "decision-profiles.md",
            SHARED_ROOT / "field-profiles.md",
            SHARED_ROOT / "prompts" / "classifier.md",
            SHARED_ROOT / "prompts" / "diluter_research.md",
            SHARED_ROOT / "prompts" / "diluter_persona.md",
            SHARED_ROOT / "prompts" / "diluter_general.md",
            SHARED_ROOT / "prompts" / "diluter_onboarding.md",
        ]
        for path in expected_files:
            self.assertTrue(path.exists(), f"Missing shared file: {path}")

    def test_hosts_bootstrap_from_shared_rule_source(self) -> None:
        for host_text in (self.codex_skill, self.claude_skill):
            self.assertIn("shared/skill-core.md", host_text)
            self.assertIn("shared/decision-profiles.md", host_text)
            self.assertIn("shared/field-profiles.md", host_text)
            self.assertIn("shared/prompts/classifier.md", host_text)

    def test_hosts_use_only_three_intensity_levels(self) -> None:
        for host_text in (self.codex_skill, self.claude_skill, self.decision_profiles):
            self.assertIn("light", host_text)
            self.assertIn("medium", host_text)
            self.assertIn("heavy", host_text)
            self.assertNotIn("中高", host_text)

    def test_course_presentation_uses_medium_plus_bias(self) -> None:
        course_section = section(self.decision_profiles, "`share_target_profile`")
        self.assertIn("### `course-presentation`", course_section)
        self.assertIn("`default_intensity = medium`", course_section)
        self.assertIn(
            "`classification_bias = prefer_remove_for_unpublished_and_lab_local_content`",
            course_section,
        )

    def test_field_profiles_define_built_in_fallback_profiles(self) -> None:
        for name in [
            "generic-research",
            "computer-science",
            "wet-lab",
            "human-subjects",
            "education-research",
        ]:
            self.assertIn(f"## `{name}`", self.field_profiles)
        self.assertIn("回退到 `generic-research`", self.field_profiles)

    def test_review_fallback_defines_concrete_actions_per_share_target(self) -> None:
        review_section = section(self.skill_core, "REVIEW 批量处理策略")
        self.assertRegex(
            review_section,
            r"new-member-onboarding.*?(保留|稀释|替换|匿名化)",
            "Missing explicit fallback action for unresolved REVIEW items in new-member-onboarding.",
        )
        self.assertRegex(
            review_section,
            r"course-presentation.*?(保留|稀释|替换|匿名化)",
            "Missing explicit fallback action for unresolved REVIEW items in course-presentation.",
        )
        self.assertRegex(
            review_section,
            r"internal-handoff.*?(保留|稀释|替换|匿名化)",
            "Missing explicit fallback action for unresolved REVIEW items in internal-handoff.",
        )

    def test_lab_context_defines_deterministic_source_order(self) -> None:
        lab_context_section = section(self.decision_profiles, "`lab_name` 到决策链的绑定")
        self.assertRegex(
            lab_context_section,
            r"(显式配置|用户配置|用户显式提供)",
            "lab_context is missing an explicit-config source step.",
        )
        self.assertRegex(
            lab_context_section,
            r"(本地语料|本地文档|corpus|目录搜索|local corpus)",
            "lab_context is missing a local-corpus discovery step.",
        )
        self.assertRegex(
            lab_context_section,
            r"(为空|留空|空集).*(REVIEW|复核)",
            "lab_context is missing an empty-plus-review fallback step.",
        )

    def test_classification_bias_maps_to_executable_tag_behavior(self) -> None:
        share_target_section = section(self.decision_profiles, "`share_target_profile`")
        for bias in [
            "retain_safety_and_setup",
            "balanced",
            "retain_execution_path",
            "prefer_remove_for_unpublished_and_lab_local_content",
        ]:
            self.assertIn(f"`classification_bias = {bias}`", share_target_section)

        bias_mapping_markers = [
            r"retain_safety_and_setup.*?\[KEEP-CRITICAL\]",
            r"balanced.*?\[SAFE\]|\[DILUTE\]",
            r"retain_execution_path.*?(最低执行路径|\[KEEP-CRITICAL\]|\[REVIEW\])",
            r"prefer_remove_for_unpublished_and_lab_local_content.*?\[REMOVE\]",
        ]
        for marker in bias_mapping_markers:
            self.assertRegex(
                self.decision_profiles,
                marker,
                "classification_bias is missing deterministic tag/action mapping.",
            )


if __name__ == "__main__":
    unittest.main()
