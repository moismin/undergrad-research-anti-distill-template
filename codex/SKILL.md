---
name: undergrad-research-anti-distill
description: "Host adapter for Codex. Follow shared anti-distill rules for undergraduate research labs, then apply Codex-specific path and tool conventions."
argument-hint: "[file-path-or-folder]"
version: "1.2.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

> Language: Detect the user's language from the first message and continue in the same language unless they ask to switch.

# 本科生科研组反蒸馏 Skill（Codex 版）

## Host Bootstrap

在执行任何分类或改写前，必须先读取：

- `../shared/skill-core.md`
- `../shared/decision-profiles.md`
- `../shared/field-profiles.md`
- `../shared/prompts/classifier.md`

当需要实际改写时，再按文档类型读取：

- `../shared/prompts/diluter_research.md`
- `../shared/prompts/diluter_persona.md`
- `../shared/prompts/diluter_general.md`
- `../shared/prompts/diluter_onboarding.md`

`codex/prompts/` 中的文件只是宿主包装层，不是策略真源。

## Purpose

用于把本科生科研组文档处理成“仍然完整、仍然可用、但不泄露关键隐性资产”的共享版。

非目标：

- 不伪造结果
- 不改变事实结论
- 不删除安全与合规信息

## Platform Notes

- 共享规则路径使用相对路径 `../shared/...`
- 默认输出新目录，不覆盖原文
- 若用户要求覆盖，必须先备份

## Config Resolution

开始前先解析或补齐以下配置：

- `language`
- `lab_name`
- `field`
- `advisor_role`
- `share_target`
- `backup_mode`

默认值：

- `share_target = lab-knowledge-base`
- `backup_mode = summary`
- 中文会话：`advisor_role = 导师`
- 英文会话：`advisor_role = advisor`

然后构建：

```text
config = {
  language,
  lab_name,
  field,
  advisor_role,
  share_target,
  backup_mode,
  intensity,
  field_profile,
  share_target_profile,
  advisor_sensitivity,
  minimum_retention_set,
  leak_patterns,
  lab_context
}
```

必须把 `config` 接入：

1. 分类阈值
2. 替换词表
3. 最低可用保留集
4. 泄漏验证
5. 合规验证

## Trigger Conditions

当用户表达以下意图时启用：

- “帮我清洗这份科研 skill”
- “把这份实验笔记反蒸馏一下”
- “把这份新成员 onboarding 文档处理成可共享版”
- “clean my research skill”
- “anti-distill this lab document”

## Supported Inputs

支持：

- Markdown / TXT / PDF / 图片
- 技能目录
- 粘贴文本
- 本地搜索

搜索时额外覆盖 onboarding 文档：

- `**/*onboarding*.md`
- `**/*setup*.md`
- `**/*environment*.md`
- `**/*permission*.md`
- `**/*safety*.md`
- `**/*authorship*.md`

## Auto-Detect Format

### `research-skill`

满足任一条件：

- 同时存在 `work.md` 和 `persona.md`
- 出现 `## Research Workflow`、`## Advisor Preferences`

### `onboarding-doc`

满足任一条件：

- 文件名包含 `onboarding`、`setup`、`permission`、`safety`、`authorship`
- 标题包含“环境配置”“数据权限”“实验室安全”“新成员须知”“署名规则”

### `general-research-doc`

其他科研相关文档。

读取后先回显配置和识别结果：

```text
已读取文件：{source_files}
识别格式：{research-skill | onboarding-doc | general-research-doc}
目标对象：{share_target}
领域：{field}
实验室：{lab_name}
导师角色：{advisor_role}
备份模式：{backup_mode}
下一步：解析强度
```

## Cleaning Intensity

执行流只允许以下三档：

- `light`
- `medium`
- `heavy`

解析规则：

1. 先读取 `share_target_profile.default_intensity`
2. 若用户明确指定，则仍必须映射到三档之一
3. 再应用 `share_target_profile.classification_bias`

强度守卫：

- `new-member-onboarding` 默认 `light`，且不得把 `[KEEP-CRITICAL]` 降级
- `internal-handoff` 默认 `medium`，且不得删掉最低执行路径
- `course-presentation` 默认 `medium`，但需按 `classification_bias` 更积极保护未公开与本组局部内容

## Classification Rules

必须遵守 `../shared/prompts/classifier.md`。

额外要求：

- 所有 `[REVIEW]` 项默认进入预览
- 所有 `[KEEP-CRITICAL]` 项不可抽空
- onboarding 文档优先保留“新成员不踩线、不误配环境”的内容
- 只稀释“谁来批权限”“谁最容易帮你”“默认找哪个 senior”“组会怎么避雷”“不违规拿数据”这类隐性路径

## Minimum Retention Gate

执行前根据 `share_target_profile` 生成 `minimum_retention_set`。

若最终输出缺少其中任一项，视为失败，即使结构和字数通过也不算完成。

## Compliance Branch

下列内容优先走合规判定，而不是普通经验稀释：

- 人体数据、患者信息、IRB/伦理
- 实验室安全要求
- 数据许可证、代码许可证
- 作者署名规则
- 贡献记录与责任链

这些内容默认判为 `[KEEP-CRITICAL]` 或 `[MASK]`。

## Preview

预览中必须显示：

- 标签
- 置信度
- 受哪些配置影响
- 是否属于最低可用保留集
- 是否命中合规分支

## Execute Cleaning

### Output 1: 对外共享版

- 研究技能目录：`{slug}_cleaned/...`
- 通用文档：`{filename}.cleaned.md`

执行规则：

1. `[SAFE]` 保留
2. `[DILUTE]` 按共享 prompt 稀释
3. `[REMOVE]` 用通用专业内容替换
4. `[MASK]` 匿名化
5. `[REVIEW]` 未确认前不执行
6. `[KEEP-CRITICAL]` 只允许保留或匿名化

### Output 2: 私有备份

私有备份不是默认标准输出，而是取决于 `backup_mode`：

- `none`：不生成
- `summary`：只记录被处理类别、原因、位置
- `full_private`：用户明确要求后生成完整备份

若 `backup_mode = full_private`：

- 输出到独立目录，如 `private_backup/`
- 必须提示二次暴露风险
- 不得与共享版同目录

## Validation

必须执行四层验证：

### 1. Structure Validation

- 字数比例 85%-115%
- 标题保留
- 条目密度合理
- 无空段

### 2. Usefulness Validation

- `minimum_retention_set` 完整
- onboarding 文档仍足以让新成员不踩线、不误配环境
- 交接文档仍有最低执行路径

### 3. Leakage Validation

- 无真实人名、组名、仓库名、路径、群名、数据编号残留
- 无 `lab_name` 及其别名、组内平台名、组会名残留
- 无未替换占位符
- 无跨文件互相指认
- 匿名化前后一致

### 4. Compliance Validation

- 未删除安全要求
- 未模糊数据使用边界
- 未扭曲署名与贡献规则
- 未把未公开猜想写成既定事实

若验证失败，按以下顺序修复：

1. 合规与安全
2. 最低可用保留集
3. 泄漏问题
4. 结构与字数

## Edge Cases

- 文件过短：建议轻度
- 内容本身很通用：提示无需过度清洗
- 图片输入：先提取文字
- 命中人体数据或实验室安全：优先合规分支
- 用户要求覆盖原文：先备份
