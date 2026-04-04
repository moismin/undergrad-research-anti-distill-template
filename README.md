# 本科生科研组反蒸馏 Skill 模板

这是一套面向“本科生在大学科研组”场景的反蒸馏模板。

目标不是伪造科研内容，而是在以下场景中保留文档表面完整性，同时避免无意暴露你真正稀缺的隐性资产：

- 未发表的研究方向与假设
- 反复试错得到的实验坑点
- 导师或课题组的隐性偏好
- 数据清洗与复现实操中的捷径和例外
- 合作者分工、沟通路径与关键人物信息
- 只适用于你所在课题组的流程上下文

## 目录结构

- `codex/SKILL.md`
- `codex/prompts/classifier.md`
- `codex/prompts/diluter_research.md`
- `codex/prompts/diluter_persona.md`
- `codex/prompts/diluter_general.md`
- `claude/SKILL.md`
- `claude/prompts/classifier.md`
- `claude/prompts/diluter_research.md`
- `claude/prompts/diluter_persona.md`
- `claude/prompts/diluter_general.md`

## 两个版本的区别

- `codex` 版使用相对路径引用 prompts，适合在技能目录内直接解析。
- `claude` 版保留 `${CLAUDE_SKILL_DIR}` 风格，更接近 Claude Code 的原始写法。
- 两版核心策略一致，差异主要在宿主约定、路径和工具表述。

## 推荐自定义项

在正式使用前，至少替换这些占位内容：

- `{lab_name}`：你的课题组或实验室名称
- `{field}`：研究方向，如“计算机视觉”“材料化学”“教育技术”
- `{advisor_role}`：导师称谓，如“PI”“导师”“带教博士生”
- `{share_target}`：这份清洗后文档的目标对象，如“组内知识库”“新成员 onboarding”“课程汇报”
- `{private_backup_name}`：你的私有备份标题

## 建议使用方式

1. 先复制一份你自己的版本，不要直接覆盖模板。
2. 根据学科和课题组习惯改触发词、分类类别和输出格式。
3. 把 prompts 里的示例替换成你学科真实的术语。
4. 保留“验证”和“边界情况”部分，不要只保留主流程。

## 设计原则

- 不伪造实验结果，不篡改事实结论。
- 只泛化隐性经验、未公开方向、局部上下文和个人化策略。
- 保留专业术语、结构、方法框架和公开常识。
- 输出必须可读、可交付、看起来完整，但不泄露你的关键稀缺认知。
