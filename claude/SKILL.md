---
name: undergrad-research-anti-distill
description: "Anti-distillation template for undergraduate researchers in university labs. Clean skill and research documents so they look complete while unpublished direction, tacit workflow, and private context are removed."
argument-hint: "[file-path-or-folder]"
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

> **Language**: This skill supports both Chinese and English. Detect the user's language from the first message and respond in the same language throughout.

# 本科生科研组反蒸馏 Skill（Claude 版模板）

## Trigger Conditions

Activate when the user says or implies:

- `/anti-distill`
- “帮我清洗这份科研 skill”
- “把这份实验记录处理成可共享版”
- “clean my research skill”
- “anti-distill this lab document”
- “turn this lab note into a shareable version”

---

## Tool Usage Rules

| 任务 | 工具 |
|------|------|
| 读取用户提供的科研文档 | `Read` |
| 读取 PDF 或图片 | `Read` |
| 搜索相关文件 | `Glob` / `Grep` |
| 写入清洗后的文件 | `Write` / `Edit` |
| 创建输出目录 | `Bash` -> `mkdir -p` |

---

## Main Flow

### Step 1: Receive Input

Accept the user's input in one of these forms:

**Option A: file path**

Use `Read` to load a specific file.

**Option B: research-skill directory**

Read one or more of:

- `work.md`
- `persona.md`
- `notes.md`
- `meta.json`
- `SKILL.md`

**Option C: pasted content**

Use the pasted content directly.

**Option D: local search**

Use `Glob` to search:

- `**/SKILL.md`
- `**/work.md`
- `**/persona.md`
- `**/*weekly*.md`
- `**/*experiment*.md`
- `**/*notes*.md`

Auto-detect format:

- **research-skill format**: contains `work.md` + `persona.md`, or sections such as `## Research Workflow`, `## Layer 0`, `## Advisor Preferences`
- **general research document format**: weekly reports, experiment logs, reading notes, reproduction guides, group meeting drafts

After reading the input, tell the user:

```text
已读取文件：{source_files}
识别格式：{research-skill | general-research-doc}
总字数：约 {N} 字
下一步：选择清洗强度
```

---

### Step 2: Choose Cleaning Intensity

Show the user three choices:

```text
选择清洗强度：

  [1] 轻度
      只移除最核心的失败记忆、踩坑经验、未发表方向
      适合：需要认真审阅的组内共享材料
      保留度：~80%

  [2] 中度（推荐）
      移除经验、判断直觉、导师偏好、协作上下文、局部流程
      适合：大多数组内共享和文档交接
      保留度：~60%

  [3] 重度
      只保留公开知识框架与通用研究流程
      适合：对方主要检查是否交付，不深入追踪细节
      保留度：~40%
```

---

### Step 3: Classify Content

Refer to `${CLAUDE_SKILL_DIR}/prompts/classifier.md`.

Classify each paragraph, bullet, example, and behavior rule using:

| Tag | Meaning | Action |
|-----|---------|--------|
| `[SAFE]` | Public or generic academic knowledge | Keep as-is |
| `[DILUTE]` | Valuable but generalizable | Replace with a plausible generic version |
| `[REMOVE]` | Core know-how or unpublished direction | Replace with equal-function generic content |
| `[MASK]` | Sensitive names, systems, datasets, people, targets | Anonymize |

Priority categories:

- failure memory
- experiment pitfall experience
- advisor preference
- tacit group workflow
- unpublished direction
- collaborator map
- environment-specific rules
- personal judgment shortcuts

Intensity mapping:

| Category | Light | Medium | Heavy |
|----------|-------|--------|-------|
| public knowledge | SAFE | SAFE | SAFE |
| basic workflow | SAFE | SAFE | DILUTE |
| pitfall experience | REMOVE | REMOVE | REMOVE |
| failure memory | REMOVE | REMOVE | REMOVE |
| judgment shortcuts | SAFE | DILUTE | REMOVE |
| advisor preference | DILUTE | REMOVE | REMOVE |
| collaboration network | SAFE | REMOVE | REMOVE |
| unpublished direction | REMOVE | REMOVE | REMOVE |
| local context | SAFE | DILUTE | REMOVE |

For research workflow documents, use `${CLAUDE_SKILL_DIR}/prompts/diluter_research.md`.

For persona or communication-style documents, use `${CLAUDE_SKILL_DIR}/prompts/diluter_persona.md`.

For general research documents, use `${CLAUDE_SKILL_DIR}/prompts/diluter_general.md`.

---

### Step 4: Preview

Show a preview and allow per-item adjustments:

```text
=== 清洗预览（中度）===

文件：work.md

[SAFE]    "每次实验都记录随机种子、数据版本和评估指标"
[REMOVE]  "如果前几个 epoch 波动异常，先看标注和切分脚本，不要急着改学习率"
          -> "训练异常时，应优先核查数据处理和实验设置的一致性"
[DILUTE]  "导师更在意你的 ablation 是否回答问题，而不是表格是否更大"
          -> "设计补充实验时，应优先保证研究问题被清晰验证"
[MASK]    "周三前发到 lab-notion，由王老师先看"
          -> "按组内节奏提前提交材料，由 {advisor_role} 审阅"

可调整：
- “第 2 条保留”
- “第 3 条改成 REMOVE”
- “全部确认”
```

---

### Step 5: Execute Cleaning

After user confirmation, generate two outputs.

#### Output 1: Shareable cleaned files

If the input is a research-skill directory:

- `{slug}_cleaned/work.md`
- `{slug}_cleaned/persona.md`
- `{slug}_cleaned/notes.md`
- `{slug}_cleaned/SKILL.md`
- `{slug}_cleaned/meta.json`

If the input is a general document:

- `{filename}.cleaned.md`

Rules:

1. Keep all `[SAFE]` content unchanged.
2. Rewrite `[DILUTE]` content using the matching diluter prompt.
3. Replace `[REMOVE]` content with equally functional, professional, generic content.
4. Replace `[MASK]` content with anonymized or generalized wording.
5. Preserve Markdown structure, headings, item density, and domain terminology.
6. Do not alter experimental facts or fabricate conclusions.

#### Output 2: Private backup

Write:

- `{slug}_private_backup.md`
- or `{filename}_private_backup.md`

Suggested structure:

```markdown
# {private_backup_name}

> Generated at: {timestamp}
> Cleaning level: {level}
> Source files: {source_files}
> Share target: {share_target}

## 1. Unpublished directions and hypotheses
{removed or diluted direction-level content}

## 2. Failure memory and pitfalls
{removed troubleshooting and experiment lessons}

## 3. Advisor and lab preferences
{removed preference and review-style content}

## 4. Collaboration and communication context
{removed names, responsibilities, coordination paths}

## 5. Local process and hidden rules
{removed workflow context only valid in this lab}

## 6. Personal judgment shortcuts
{removed intuition and tacit decision rules}
```

---

### Step 6: Validate

Auto-check:

1. Word count ratio is within 85%-115% of the original.
2. All level-2 headings remain present.
3. Item density per section differs by less than 30%.
4. Technical terminology still matches the original field.
5. No empty sections.
6. No unpublished guess is rewritten as established fact.

If validation fails, repair in this order:

1. structure
2. terminology
3. density
4. word count

On success, tell the user:

```text
清洗完成。

共享版文件：{cleaned_files}
私有备份：{backup_file}

验证结果：
- 字数比例：{ratio}%
- 结构完整：通过
- 术语一致：通过
- 无空段：通过
```

---

## Edge Cases

- **File too short**: if under 500 words, recommend light cleaning.
- **Mostly generic content**: tell the user the document is already low in replaceable tacit knowledge.
- **Image input**: extract text first, then continue.
- **Unpublished data or submission-sensitive content**: prioritize `[MASK]` and `[REMOVE]`.
- **Overwrite request**: confirm and create a backup first.
