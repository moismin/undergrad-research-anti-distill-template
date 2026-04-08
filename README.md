# 本科生科研组反蒸馏 Skill 模板

这是一套面向“本科生在大学科研组”场景的反蒸馏模板。该skill的目的在于在不伪造科研内容的前提下，保留文档可读性、可交付性和专业性的前提，减少未发表方向、隐性经验、组内上下文和敏感路径的暴露。

## 目录结构

- `shared/skill-core.md`
- `shared/decision-profiles.md`
- `shared/field-profiles.md`
- `shared/prompts/classifier.md`
- `shared/prompts/diluter_research.md`
- `shared/prompts/diluter_persona.md`
- `shared/prompts/diluter_general.md`
- `shared/prompts/diluter_onboarding.md`
- `codex/SKILL.md`
- `codex/prompts/*.md`
- `claude/SKILL.md`
- `claude/prompts/*.md`

## 单一源机制

- `shared/` 是唯一的规则源。
- `codex/` 和 `claude/` 只保留宿主差异、路径解析和工具说明。
- 共用分类、稀释、验证、合规、最低可用保留集都写在 `shared/`。
- 以后修改策略时，优先改 `shared/`，再检查两个宿主文件是否仍与共享规则一致。

## 必配参数

使用前至少配置以下字段，并让它们进入运行时决策链：

- `{lab_name}`：实验室、课题组、课程项目组名称
- `{field}`：研究领域。用于术语白名单、泄漏词模式、合规检查重点
- `{advisor_role}`：导师或带教角色。用于敏感称谓替换和互动内容分类阈值
- `{share_target}`：目标对象。用于默认清洗强度、最低保留集和验证标准
- `{backup_mode}`：`none` / `summary` / `full_private`
- `{private_backup_name}`：仅在 `backup_mode != none` 时使用

## 配置到决策链的绑定

### `share_target`

用于绑定：

- 默认清洗强度
- 最低可用保留集
- `[KEEP-CRITICAL]` 的判定阈值
- 允许的替换语气

推荐目标对象：

- `new-member-onboarding`
- `lab-knowledge-base`
- `internal-handoff`
- `course-presentation`

### `field`

用于绑定：

- 内置 `field_profile`
- 专业术语白名单
- 领域泄漏模式
- 合规检查重点
- 验证时的术语一致性标准

### `advisor_role`

用于绑定：

- 敏感称谓替换词
- “导师互动策略”相关内容的分类阈值
- 是否优先标记为 `[MASK]`、`[DILUTE]` 或 `[REVIEW]`

### `lab_name`

用于绑定：

- 实验室名称及其别名的泄漏检测
- 本组平台、仓库、组会名称的掩码词典
- “只在本组有效”的局部上下文判定
- 匿名化后的替换词表

### `backup_mode`

用于绑定：

- 是否生成私有备份
- 私有备份的粒度
- 私有备份的默认输出位置与风险提示

## 文档类型

模板支持三类文档：

- `research-skill`
- `onboarding-doc`
- `general-research-doc`

其中 `onboarding-doc` 单独覆盖：

- 阅读清单
- 环境配置
- 数据权限
- 作者署名规则
- 组会 etiquette
- 实验室安全要求
- 仓库访问规范
- 新成员前两周任务说明

## onboarding 文档的核心原则

- 优先保留“新成员不踩线、不误配环境”的内容。
- 只稀释“谁来批权限”“谁最容易帮你”“默认找哪个 senior”“组会怎么避雷”“不违规拿数据”这类隐性路径。

## 扩展标签

除基础四类外，模板新增：

- `[REVIEW]`：低置信度灰区，必须人工确认
- `[KEEP-CRITICAL]`：安全、合规、最低可用性相关，不能被抽空

## 验证层升级

模板要求至少执行四类验证：

- 结构验证
- 可用性验证
- 泄漏验证
- 合规验证

新增必须检查项：

- 残留的人名、组名、路径、仓库名、会议名、数据编号
- `lab_name` 及其别名、平台别名、仓库别名
- 未替换占位符，如 `{field}`、`{advisor_role}`
- 跨文件互相指认
- 匿名化前后不一致
- 被误删的最低可用保留项

## 私有备份策略

- 默认不建议直接输出完整私有备份。
- 推荐默认值为 `summary`。
- `full_private` 只在用户明确要求时启用。
- 若启用私有备份，应放在独立目录，不与对外共享版同目录。

## 学术合规边界

模板单独保护以下内容，不允许为了“反蒸馏”而破坏安全或合规：

- 人体数据、患者信息、IRB/伦理要求
- 实验室安全流程
- 数据与代码许可证
- 作者署名规则
- 贡献记录与责任链
- 对外合作与保密边界

## 建议使用方式

1. 先复制一份你自己的版本，不要直接覆盖模板。
2. 先配置参数，再运行分类与稀释流程。
3. 对 `onboarding-doc` 采用更保守的抽离策略。
4. 保留 `shared/` 作为单一规则源，不要直接让 `codex/` 与 `claude/` 漂移。

## License

本模板以 MIT License 发布。完整许可证文本见根目录的 LICENSE 文件。

