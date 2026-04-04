---
name: undergrad-research-anti-distill
description: "Anti-distillation template for undergraduate researchers in university labs. Keep documents complete-looking while removing unpublished direction, tacit workflow, and hard-won know-how."
argument-hint: "[file-path-or-folder]"
version: "1.0.0"
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

> Language: Detect the user's language from the first message and continue in the same language unless they ask to switch.

# 本科生科研组反蒸馏 Skill（Codex 版模板）

## Purpose

用于清洗本科生在大学科研组中积累的技能文档、周报、实验记录、复现手册、导师沟通策略文档。

目标：

- 保留公开可分享的学术框架和专业表达
- 移除未发表方向、试错经验、隐性偏好、协作上下文
- 生成一份可分享版本和一份私有备份

非目标：

- 不编造数据或实验结果
- 不改变结论真假
- 不把错误内容包装成正确方法

## Platform Notes

- 将 `prompts/` 目录视为与当前 `SKILL.md` 同级的相对依赖目录。
- 引用 prompt 时使用相对路径，例如 `./prompts/classifier.md`。
- 默认写入新的输出目录，不覆盖原文。
- 如果用户明确要求覆盖原文，必须先确认并备份。

## Trigger Conditions

当用户表达以下意图时启用：

- “帮我清洗这份科研 skill”
- “把我的实验笔记反蒸馏一下”
- “clean my research skill”
- “anti-distill this lab document”
- “把这份组内经验文档整理成可共享版”
- “把这份周报/实验记录处理成能交但不暴露核心经验的版本”

## Supported Inputs

支持以下输入形式：

### Option A: 单个文件

读取用户提供的 Markdown / TXT / PDF / 图片 / 周报导出文件。

### Option B: 技能目录

读取类似以下结构的目录：

- `work.md`
- `persona.md`
- `notes.md`
- `meta.json`
- `SKILL.md`

### Option C: 粘贴内容

直接处理用户粘贴的文本。

### Option D: 本地搜索

当用户只给出主题词或文件名线索时，搜索：

- `**/SKILL.md`
- `**/work.md`
- `**/persona.md`
- `**/*weekly*.md`
- `**/*experiment*.md`
- `**/*notes*.md`

## Auto-Detect Format

### Research-skill format

满足任一条件即可判定：

- 同时存在 `work.md` 和 `persona.md`
- 出现 `## Research Workflow`、`## Layer 0`、`## Advisor Preferences`
- 文档明显分为“工作方法”和“个人/协作风格”

### General research document format

其他科研相关文档，例如：

- 周报
- 实验记录
- 复现手册
- 读论文笔记
- 组会准备稿

读取完成后向用户确认：

```text
已读取文件：{source_files}
识别格式：{research-skill | general-research-doc}
目标用途：{share_target}
总字数：约 {N} 字
下一步：选择清洗强度
```

## Cleaning Intensity

向用户提供三档强度：

```text
选择清洗强度：

  [1] 轻度
      只移除最关键的踩坑经验、失败记忆、未发表方向
      适合：要给导师、课题组认真审阅的共享材料
      保留度：~80%

  [2] 中度（推荐）
      移除经验、判断直觉、导师偏好、隐性流程、协作上下文
      适合：大多数组内共享、知识库沉淀、交接材料
      保留度：~60%

  [3] 重度
      只保留公开知识框架和通用研究流程
      适合：对方主要检查你是否整理了文档，不深入看细节
      保留度：~40%
```

## Classification Rules

先读取 `./prompts/classifier.md`，再对每个段落、要点、示例进行标记。

统一标签：

| Tag | Meaning | Action |
|-----|---------|--------|
| `[SAFE]` | 公开常识、基础方法、删掉反而可疑 | 原样保留 |
| `[DILUTE]` | 有价值但可泛化 | 改写为学科内合理但不稀缺的版本 |
| `[REMOVE]` | 你的核心经验、独家判断、未公开方向 | 替换为等功能、等密度的通用内容 |
| `[MASK]` | 敏感信息，如导师姓名、同门姓名、内部平台、未公开数据标识 | 匿名化或泛化 |

重点识别以下高价值类别：

- 失败样本与踩坑经验
- 实验调参直觉
- 导师或带教人的隐性偏好
- 组会汇报的真实通过标准
- 未发表研究假设与下一步方向
- 数据清洗中特殊规则与捷径
- 合作者分工与关键沟通路径
- 仅适用于本组设备、数据、代码库的上下文

### 强度映射

| 类别 | 轻度 | 中度 | 重度 |
|------|------|------|------|
| 公开知识 | SAFE | SAFE | SAFE |
| 基础实验流程 | SAFE | SAFE | DILUTE |
| 踩坑经验 | REMOVE | REMOVE | REMOVE |
| 故障排查记忆 | REMOVE | REMOVE | REMOVE |
| 调参与判断直觉 | SAFE | DILUTE | REMOVE |
| 导师偏好 | DILUTE | REMOVE | REMOVE |
| 协作网络 | SAFE | REMOVE | REMOVE |
| 未发表方向 | REMOVE | REMOVE | REMOVE |
| 局部上下文 | SAFE | DILUTE | REMOVE |

## Preview

向用户展示分类预览，并允许逐条调整：

```text
=== 清洗预览（中度）===

文件：work.md

[SAFE]    "每次实验都记录数据版本、随机种子和评估指标"
[REMOVE]  "如果 loss 前 3 个 epoch 波动异常，先检查标注脚本而不是继续调学习率"
          -> "训练初期出现异常时，应优先排查数据与流程一致性"
[DILUTE]  "导师更看重 ablation 是否回答问题，而不是表格是否更大"
          -> "设计消融实验时，应优先保证研究问题被清晰验证"
[MASK]    "王老师要求周三前发到 lab-notion"
          -> "{advisor_role} 要求按组内既定节奏提前提交材料"

确认方式：
- “第 2 条保留”
- “第 3 条改成 REMOVE”
- “全部确认”
```

## Execute Cleaning

用户确认后，生成两类输出。

### Output 1: 对外共享版

如果是研究技能目录：

- `{slug}_cleaned/work.md`
- `{slug}_cleaned/persona.md`
- `{slug}_cleaned/notes.md`
- `{slug}_cleaned/SKILL.md`
- `{slug}_cleaned/meta.json`

如果是通用科研文档：

- `{filename}.cleaned.md`

执行规则：

1. `[SAFE]` 原样保留。
2. `[DILUTE]` 参考 `./prompts/diluter_research.md`、`./prompts/diluter_persona.md` 或 `./prompts/diluter_general.md` 改写。
3. `[REMOVE]` 替换为不暴露关键知识但结构完整的通用专业内容。
4. `[MASK]` 统一做匿名化或泛化。
5. 保持 Markdown 结构、标题层级、列点密度、术语领域不变。
6. 不得改变实验事实和结论方向，只允许抽掉“为什么你能比别人做得更稳”的那部分。

### Output 2: 私有备份

输出为：

- `{slug}_private_backup.md`
- 或 `{filename}_private_backup.md`

内容结构建议：

```markdown
# {private_backup_name}

> 生成时间：{timestamp}
> 清洗强度：{level}
> 原始文件：{source_files}
> 目标用途：{share_target}

## 一、未发表方向与假设
{所有被移除或泛化的方向判断、实验假设、下一步路线}

## 二、失败记忆与踩坑经验
{所有被移除的故障排查、调参经验、数据问题}

## 三、导师与课题组偏好
{所有被移除的导师反馈模式、组会标准、默认预期}

## 四、协作与沟通上下文
{所有被移除的人名、职责、沟通路径、交接信息}

## 五、局部流程与隐性规则
{所有只在本课题组、本设备、本数据、本代码库有效的上下文}

## 六、你自己的判断直觉
{所有被弱化的经验型判断}
```

## Validation

完成后自动验证：

1. 字数比例应在原文的 85%-115% 之间。
2. 所有二级标题必须保留。
3. 各章节条目数差异不超过 30%。
4. 专业术语仍然属于 `{field}` 领域，不得被降级成空泛鸡汤。
5. 不允许出现只有标题没有内容的空段。
6. 不允许把未发表结论改写成已发表事实。

若验证失败，优先按以下顺序修复：

1. 修结构
2. 修术语与语气
3. 修条目密度
4. 修字数比例

通过后向用户输出：

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

## Edge Cases

### 文件过短

若少于 500 字，提醒用户优先选择轻度清洗。

### 内容本身已经很通用

若分析后大多为公开知识，直接告知用户这份文档本来就不具备很强稀缺性。

### 图片或截图输入

先提取文字，再进入正常流程。若提取质量差，先提示用户补一份文本。

### 涉及未公开数据或论文投稿

优先使用 `[MASK]` 与 `[REMOVE]` 保护：

- 数据编号
- 样本来源
- 投稿目标
- 未公开图表结论

### 用户要求覆盖原文

只有在用户明确同意后才覆盖，并先生成 `{filename}.original.bak`。
