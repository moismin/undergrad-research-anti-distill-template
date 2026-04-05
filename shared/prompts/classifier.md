# 共用分类规则

在分类前必须先读取：

- `../skill-core.md`
- `../decision-profiles.md`
- `../field-profiles.md`

并根据运行时 `config` 调整判定。

## 分类目标

对每个段落、要点、例子、话术、命令、规则，标记为以下六类之一：

- `[SAFE]`
- `[DILUTE]`
- `[REMOVE]`
- `[MASK]`
- `[REVIEW]`
- `[KEEP-CRITICAL]`

## 参数驱动

### `share_target`

- 若为 `new-member-onboarding`，优先把安全、权限、环境 prerequisites 归为 `[KEEP-CRITICAL]`
- 若为 `course-presentation`，依据 `classification_bias` 更积极地把局部路径和未公开方向归为 `[REMOVE]`

### `advisor_role`

- 高敏角色的真实姓名和偏好，优先 `[MASK]` 或 `[REVIEW]`
- 互动策略若带有明显博弈性，不直接 `[SAFE]`

### `field`

- 使用 `field_profile.terminology_whitelist` 防止把专业表达误删成空话
- 使用 `field_profile.leak_patterns` 捕捉本领域常见的泄漏实体
- 使用 `field_profile.compliance_focus` 提升合规相关内容的保护等级

### `lab_name`

- 命中 `lab_context.primary_name / aliases / internal_platform_aliases / meeting_aliases / repo_aliases` 时，优先 `[MASK]`
- 若内容显式依赖 `lab_context.local_context_markers`，至少 `[DILUTE]`，很多场景应 `[REMOVE]` 或 `[REVIEW]`
- 替换时统一转成中性表达，如“组内公开流程”“实验室既定系统”“课题组共享仓库”

## onboarding 特殊规则

onboarding 文档优先保留“新成员不踩线、不误配环境”的内容。

只稀释以下隐性路径：

- 谁来批权限
- 谁最容易帮你
- 默认找哪个 senior
- 组会怎么避雷
- 不违规拿数据的隐性捷径

以下内容默认 `[KEEP-CRITICAL]`：

- 安装前置条件
- 权限边界
- 安全规范
- 数据使用红线
- 最小可执行步骤

## 常见判定

### `[SAFE]`

- 公开常识
- 标准科研规范
- 删除后会让文档明显残缺的基础结构内容

### `[DILUTE]`

- 可保留外壳但要抽掉关键路径的经验
- 一般性沟通建议
- 可泛化的汇报原则

### `[REMOVE]`

- 未发表方向
- 核心排错诀窍
- 稀缺判断阈值
- 只在本组设备、脚本、数据格式下成立的经验

### `[MASK]`

- 人名
- 组名
- 仓库名
- 平台名
- 内部路径
- 编号
- `lab_name` 及其别名和相关内部称呼

### `[REVIEW]`

- 无法确定是“最低必要”还是“隐性优势”的灰区内容
- 导师互动策略中既有普适性又有博弈性的内容
- 交接文档里可能影响执行但又带局部性的内容

### `[KEEP-CRITICAL]`

- 安全
- 合规
- 最低可用性
- 最低前置条件
- 权限与数据边界

## 输出格式

按输入顺序输出：

```text
[TAG] 原文片段
置信度：high / medium / low
原因：一句话
受哪些配置影响：share_target / field / advisor_role / lab_name / backup_mode
建议动作：保留 / 稀释 / 替换 / 匿名化 / 人工确认
```
