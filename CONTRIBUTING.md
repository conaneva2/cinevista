# 参与开发

采用短分支 + 小 PR。main 保持可检查；功能未完成用能力状态控制，不编造 success。建议分支 `feat/recipe-import`、`fix/capture-receipt`、`chore/sdk-qualification`。

提交采用 `feat|fix|refactor|test|docs|build|chore(scope): description`；属于本项目约定，不是工具强行生成版本号。一次 PR 不混入无关重排、升级和功能。

PR 必须包含目的、复用调查、影响模块、许可证变化、真实命令结果、未验证项、回退与机测要求。新依赖必须进台账，不得使用 SNAPSHOT、latest、浮动 Git 分支或未解释二进制。

先运行 `python3 tools/cv.py check`。触及 SDK 代码时，补真实 APK 构建与签名/DEX证据；无法执行可提交草稿 PR，但不得标记可发布。

贡献者保留自身版权；提交的原创修改按 MIT 提供，保证有权贡献。第三方代码保留各自许可。暂不引入复杂 CLA 流程；不能以 MIT 为由删除第三方署名或把资产都视为无条件授权。

架构、相机安全、颜色精度、签名策略的变动需要 ADR。Gitee私有远端、分支保护与审查者配置见docs/GITEE.md和docs/04_WORKFLOW.md；本地文件不代表 GitHub 设置已经生效。

每个任务使用Txx/Gxx稳定ID。更新task-board后生成TODO；用户操作变化更新docs/USER_GUIDE.md，文档责任和触发条件见docs/DOCUMENTATION.md。Gitee Issue/PR模板在.gitee目录，GitHub配置仅作可选保留。

Definition of Done：验收项满足；模块/契约反向测试通过；涉及设备代码或构建规则时真实SDK构建通过；必要机测完成或明确保持未验证；文档/CHANGELOG/任务板同步；无未授权数据入库；回退和下一步可复现。
