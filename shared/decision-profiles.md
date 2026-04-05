# 决策配置映射

本文件定义运行时配置如何影响分类阈值、替换词表和验证标准。

在构建 `config` 前，必须先读取：

- `./field-profiles.md`

## 运行时配置对象

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

## `share_target_profile`

所有目标对象只能使用以下默认强度枚举之一：

- `light`
- `medium`
- `heavy`

### `new-member-onboarding`

- `default_intensity = light`
- `classification_bias = retain_safety_and_setup`
- 重点保留：环境前置条件、禁止事项、数据边界、安全要求、最小复现步骤、基本沟通规则
- 升级为 `[KEEP-CRITICAL]`：安全、权限边界、环境 prerequisites、数据使用红线
- 升级为 `[REVIEW]`：导师互动技巧、默认找谁、默认绕开什么人

### `lab-knowledge-base`

- `default_intensity = medium`
- `classification_bias = balanced`
- 重点保留：公开流程框架、输入输出、术语、标准操作
- 升级为 `[KEEP-CRITICAL]`：公共依赖、公共边界、共享流程底线

### `internal-handoff`

- `default_intensity = medium`
- `classification_bias = retain_execution_path`
- 重点保留：任务状态、公共目录结构、最低可执行步骤、已知风险类别
- 升级为 `[REVIEW]`：具体联系人、局部策略、隐性优先级

### `course-presentation`

- `default_intensity = medium`
- `classification_bias = prefer_remove_for_unpublished_and_lab_local_content`
- 重点保留：背景、公开方法、结论、限制
- 更倾向 `[MASK]` / `[REMOVE]`：未公开方向、组内路径、协作网络

## `classification_bias` 到标签动作的映射

- `retain_safety_and_setup`：安全、权限边界、环境前置条件、最小安装步骤优先 `[KEEP-CRITICAL]`；隐性求助路径优先 `[DILUTE]` 或 `[MASK]`。
- `balanced`：公开框架优先 `[SAFE]`；局部经验优先 `[DILUTE]`；显式敏感实体优先 `[MASK]`。
- `retain_execution_path`：最低执行路径、公共依赖、任务状态优先 `[KEEP-CRITICAL]`；联系人与隐性优先级优先 `[REVIEW]` 或 `[MASK]`。
- `prefer_remove_for_unpublished_and_lab_local_content`：未公开方向、组内局部路径、协作网络优先 `[REMOVE]`；显式实体优先 `[MASK]`；公开讲解框架可 `[SAFE]`。

## 强度解析规则

### 默认强度

- 先读取 `share_target_profile.default_intensity`
- 若用户覆盖，则仍只能落在 `light / medium / heavy` 三档中

### 强度守卫

- `new-member-onboarding` 不允许因为提高清洗强度而移除 `[KEEP-CRITICAL]`
- `internal-handoff` 不允许因为提高清洗强度而删掉最低执行路径
- `course-presentation` 即使默认强度为 `medium`，也应依据 `classification_bias` 更积极保护未公开和组内局部内容

## `advisor_sensitivity`

### 高敏

适用：

- `PI`
- `导师`
- `advisor`
- `课题负责人`

规则：

- 真实姓名优先 `[MASK]`
- 互动策略默认 `[DILUTE]` 或 `[REVIEW]`
- 涉及偏好和评价标准时，除非明显公共，否则不直接 `[SAFE]`

### 中敏

适用：

- `带教博士生`
- `博士后`
- `postdoc`
- `项目带教`

规则：

- 称谓泛化为“带教成员”“项目负责人”或英文等价表达
- 局部协作策略优先 `[REVIEW]`

### 低敏

适用：

- `同门`
- `lab mate`
- `值班同学`

规则：

- 人名仍 `[MASK]`
- 流程角色可保留为泛化职能名

## `lab_name` 到决策链的绑定

`lab_name` 不是记录字段，而是泄漏与局部性判断的控制参数。

必须派生：

```text
lab_context = {
  primary_name,
  aliases,
  internal_platform_aliases,
  meeting_aliases,
  repo_aliases,
  local_context_markers
}
```

来源顺序必须固定：

1. 显式配置：优先使用用户显式提供的 `lab_name` 及其已知别名。
2. 本地语料发现：若显式配置不足，则从当前文档、本地目录命名、文件标题、仓库名、组会名中发现补充 alias。
3. 留空并进入 REVIEW：若仍无法稳定确认，则对应字段留空或置为空集合，并把相关内容送入 `[REVIEW]` / 复核流程。

最小规则：

- `primary_name`：用户显式提供的 `lab_name`
- `aliases`：简称、英文缩写、常见大小写变体
- `internal_platform_aliases`：与该组绑定的 Notion、飞书、NAS、内部平台名
- `meeting_aliases`：组会、周会、内部 seminar 的常见叫法
- `repo_aliases`：组内仓库、共享盘、代码库简称
- `local_context_markers`：`本组`、`组内`、`实验室内部`、`内部流程` 及其英文等价表达

下游用途：

1. 若命中 `primary_name / aliases / internal_platform_aliases / meeting_aliases / repo_aliases`，优先 `[MASK]`
2. 若内容显式依赖 `local_context_markers`，至少 `[DILUTE]`，很多场景应 `[REMOVE]` 或 `[REVIEW]`
3. 匿名化替换时统一替换为“组内公开流程”“实验室既定系统”“课题组共享仓库”等中性表达
4. 泄漏检查必须扫描 `lab_context` 全部词典

## `field_profile`

`field_profile` 必须来自 `./field-profiles.md` 的内置 profile，或按以下顺序降级：

1. 精确命中内置 profile
2. 映射到最接近的内置 profile
3. 回退到 `generic-research`
4. 从当前文档抽取高频专业词，补充 `terminology_whitelist`
5. 若命中人体数据、危险实验、许可证关键词，自动补强 `compliance_focus`

最小结构：

```text
field_profile = {
  profile_name,
  terminology_whitelist,
  compliance_focus,
  leak_patterns,
  required_context_tokens
}
```

## `backup_mode`

### `none`

- 不生成私有备份

### `summary`

- 仅记录被处理的类别、原因和位置
- 不回填完整敏感原文
- 推荐默认值

### `full_private`

- 需要用户明确选择
- 必须独立目录存放
- 启用前必须提示二次暴露风险

## `minimum_retention_set`

必须从 `share_target_profile` 派生，至少覆盖：

- 安全
- 合规
- 最低可用性
- 目标对象完成任务所需的最小步骤

若最终输出缺少这些内容，验证必须失败。
