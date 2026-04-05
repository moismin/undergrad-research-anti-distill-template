---
name: undergrad-research-anti-distill
description: "Host adapter for Claude Code. Follow shared anti-distill rules for undergraduate research labs, then apply Claude-specific path and tool conventions."
argument-hint: "[file-path-or-folder]"
version: "1.2.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

> **Language**: Detect the user's language from the first message and continue in the same language throughout unless they ask to switch.

# 本科生科研组反蒸馏 Skill（Claude 版）

## Host Bootstrap

Before any classification or rewriting, read:

- `${CLAUDE_SKILL_DIR}/../shared/skill-core.md`
- `${CLAUDE_SKILL_DIR}/../shared/decision-profiles.md`
- `${CLAUDE_SKILL_DIR}/../shared/field-profiles.md`
- `${CLAUDE_SKILL_DIR}/../shared/prompts/classifier.md`

Then read the matching shared diluter:

- `${CLAUDE_SKILL_DIR}/../shared/prompts/diluter_research.md`
- `${CLAUDE_SKILL_DIR}/../shared/prompts/diluter_persona.md`
- `${CLAUDE_SKILL_DIR}/../shared/prompts/diluter_general.md`
- `${CLAUDE_SKILL_DIR}/../shared/prompts/diluter_onboarding.md`

`claude/prompts/` files are host wrappers only. Shared files are the source of truth.

## Config Resolution

Resolve or safely default:

- `language`
- `lab_name`
- `field`
- `advisor_role`
- `share_target`
- `backup_mode`

Defaults:

- `share_target = lab-knowledge-base`
- `backup_mode = summary`
- Chinese session: `advisor_role = 导师`
- English session: `advisor_role = advisor`

Build:

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

Use `config` to drive:

1. classification thresholds
2. replacement vocabulary
3. retention requirements
4. leakage validation
5. compliance validation

## Trigger Conditions

Activate when the user says or implies:

- `/anti-distill`
- “帮我清洗这份科研 skill”
- “把这份新成员 onboarding 文档处理成可共享版”
- “clean my research skill”
- “anti-distill this lab document”

## Input and Detection

Support:

- file path
- skill directory
- pasted text
- local search

When searching, include onboarding patterns:

- `**/*onboarding*.md`
- `**/*setup*.md`
- `**/*environment*.md`
- `**/*permission*.md`
- `**/*safety*.md`
- `**/*authorship*.md`

Detect:

- `research-skill`
- `onboarding-doc`
- `general-research-doc`

For `onboarding-doc`, follow this rule:

- 优先保留“新成员不踩线、不误配环境”的内容。
- 只稀释“谁来批权限”“谁最容易帮你”“默认找哪个 senior”“组会怎么避雷”“不违规拿数据”这类隐性路径。

After detection, show:

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

The executable workflow only allows:

- `light`
- `medium`
- `heavy`

Resolve intensity in this order:

1. read `share_target_profile.default_intensity`
2. accept user override only if it maps to one of the three levels
3. apply `share_target_profile.classification_bias`

Guardrails:

- `new-member-onboarding` defaults to `light` and must not downgrade `[KEEP-CRITICAL]`
- `internal-handoff` defaults to `medium` and must preserve the minimum execution path
- `course-presentation` defaults to `medium`, but must still use the presentation-specific protective bias for unpublished and lab-local content

## Classification

Follow the shared classifier and use six tags:

- `[SAFE]`
- `[DILUTE]`
- `[REMOVE]`
- `[MASK]`
- `[REVIEW]`
- `[KEEP-CRITICAL]`

Rules:

- `[REVIEW]` never auto-executes before confirmation
- `[KEEP-CRITICAL]` can only be kept or anonymized
- onboarding documents must preserve safe setup and boundary information

## Minimum Retention Gate

Derive `minimum_retention_set` from `share_target_profile`.

If any required item is missing in the cleaned output, validation fails even if structure looks complete.

## Compliance Branch

Treat the following as compliance-critical:

- human data / patient data / IRB
- lab safety
- data and code licenses
- authorship rules
- contribution chain
- confidentiality boundaries

These default to `[KEEP-CRITICAL]` or `[MASK]`.

## Preview

Preview must show:

- tag
- confidence
- config impact
- whether it belongs to `minimum_retention_set`
- whether it hits the compliance branch

## Execute Cleaning

### Shareable output

- research-skill directory -> `{slug}_cleaned/...`
- general doc -> `{filename}.cleaned.md`

Actions:

1. keep `[SAFE]`
2. rewrite `[DILUTE]`
3. replace `[REMOVE]`
4. anonymize `[MASK]`
5. require confirmation for `[REVIEW]`
6. preserve or anonymize `[KEEP-CRITICAL]`

### Private backup

Private backup is optional and depends on `backup_mode`:

- `none`
- `summary`
- `full_private`

If `full_private`:

- require explicit user choice
- store in an isolated directory
- warn about secondary exposure risk

## Validation

Run all four layers:

1. structure
2. usefulness
3. leakage
4. compliance

Leakage checks must include:

- names
- lab names and aliases
- internal platforms and meeting aliases
- internal paths
- repositories
- ids
- unresolved placeholders
- cross-file references
- inconsistent anonymization

Usefulness checks must include:

- onboarding output still prevents unsafe setup and line-crossing
- handoff output still preserves minimum execution path

## Edge Cases

- too short -> suggest light cleaning
- mostly generic -> tell user low replacement value
- image input -> extract text first
- compliance-sensitive input -> prioritize compliance branch
- overwrite request -> backup first
