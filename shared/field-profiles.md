# 领域配置内置表

本文件提供可直接执行的 `field_profile` 默认配置，避免运行时完全临场猜测。

## `generic-research`

- `terminology_whitelist`: 方法、数据、指标、实验设置、结果、限制、复现、权限、合规
- `compliance_focus`: 数据使用边界、基本署名规则、公共安全要求
- `leak_patterns`: 内部数据编号、实验编号、仓库路径、共享盘路径
- `required_context_tokens`: 方法、结果、限制

## `computer-science`

- `terminology_whitelist`: baseline, ablation, seed, split, training, validation, inference, benchmark, GPU, checkpoint, config
- `compliance_focus`: 数据许可证、代码许可证、隐私数据、算力权限
- `leak_patterns`: 私有 repo 名、集群名、内部脚本名、实验编号、模型版本号
- `required_context_tokens`: baseline, metric, config, data split

## `wet-lab`

- `terminology_whitelist`: protocol, reagent, sample, assay, replicate, incubation, concentration, safety, storage, contamination
- `compliance_focus`: 实验室安全、样本合规、危险化学品、设备使用资质
- `leak_patterns`: 样本编号、批次号、冰箱/仪器编号、内部 protocol 名称
- `required_context_tokens`: sample, protocol, safety, replicate

## `human-subjects`

- `terminology_whitelist`: participant, consent, IRB, anonymization, questionnaire, interview, cohort, privacy, de-identification
- `compliance_focus`: IRB、知情同意、隐私保护、去标识化、数据边界
- `leak_patterns`: 患者编号、受试者编号、医院名、学校内部项目编号
- `required_context_tokens`: consent, privacy, IRB, anonymization

## `education-research`

- `terminology_whitelist`: intervention, cohort, rubric, coding scheme, classroom observation, survey, learning outcome, consent
- `compliance_focus`: 学生数据、知情同意、课堂隐私、署名与贡献边界
- `leak_patterns`: 班级编号、学校平台名、教师姓名、课程内部代号
- `required_context_tokens`: rubric, cohort, outcome, consent

## 选择规则

- 若 `field` 直接命中以上 profile，直接使用
- 若只命中近义表达，映射到最接近 profile
- 若无法稳定映射，回退到 `generic-research`
- 回退后仍需从当前文档抽取高频专业词补充 `terminology_whitelist`
