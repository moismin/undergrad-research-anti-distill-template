# 共用科研文档稀释规则

在执行前先读取：

- `../skill-core.md`
- `../decision-profiles.md`

## 适用范围

- `research-skill`
- 周报
- 实验记录
- 复现手册
- 工作方法说明

## 目标

- 保留公开方法框架和专业术语
- 移除未发表方向、隐性经验、局部路径
- 满足 `share_target` 对最低可用性的要求

## 参数驱动改写

### `share_target = internal-handoff`

- 保留最低执行路径
- 不保留具体联系人与隐性优先级

### `share_target = course-presentation`

- 更积极抽离未公开方向和局部经验

### `field`

- 必须保留 `field_profile.terminology_whitelist` 中术语
- 不得把专业表述降级成空泛建议

## 改写策略

### 具体秘诀 -> 通用原则

原句：

`如果连续三次重跑都不稳，先检查数据切分脚本，再动训练超参。`

改写：

`当结果稳定性异常时，应优先核查数据处理与实验配置的一致性。`

### 未发表方向 -> 谨慎的后续工作表述

原句：

`下一步准备转向跨域设定，因为我们怀疑瓶颈不在当前 backbone。`

改写：

`后续工作可在更广泛设定下进一步检验当前方法的适用边界。`

## 禁止事项

- 不伪造实验完成状态
- 不改变结果真值
- 不删除 `minimum_retention_set`
- 不删除被标为 `[KEEP-CRITICAL]` 的内容
