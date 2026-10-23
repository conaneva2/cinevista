# ADR 0012：Mac 开发构建、不可覆盖证据与受审查例外

日期：2026-09-19。状态：本地开发采用；不授予设备或发行资格。

## 决策与实测

沿用现有模块和 Recipe Lab 固定提交 d4c64239ddb775e11b9343b54bc71616dd62a7a5 的官方命令链参考；不引入 Gradle/NDK，不复制上游代码。取得 Google 原始 Android 2.3.3/API10 r02 和 Build Tools 30.0.3 macOS 包，校验官方 XML 所列大小/SHA1，再记录 SHA256。使用 Temurin 17.0.20.1+1 ARM64 tar.gz，核对上游 SHA256。完整来源见 config/toolchain.lock.json。

Apple Silicon/macOS（历史测试平台） 已实际运行 x86_64 aapt/zipalign，现有系统可执行；没有安装 Rosetta、没有关闭 Gatekeeper/SIP。API10 bootclasspath、min/target10、DEX035、v1签名约束保持。JDK17、Python3.12.10、Node26.8.2为本次实测，不冒充JDK21/Node22矩阵。主机工具兼容不推导相机 ABI。

原 Manifest 的系统 drawable 使 aapt badging 无法解析；改为自有 API10 layer-list 图标，保持检查非零失败。aapt 隐含 READ_EXTERNAL_STORAGE 单独记录，显式 Manifest 仍只有 CAMERA/WRITE_EXTERNAL_STORAGE。包身份/版本、权限、对齐、签名和DEX定义类继续检查。

## 运行证据

cv.py 为每次调用创建 evidence/runs/UTC-随机ID，并通过 CINEVISTA_RUN_DIR 传给子进程。显式指定已用目录时同名证据以 exclusive create 失败，不覆盖。Android产物按run目录保存；旧evidence文件保持原字节。主机编译目录仍为可重建缓存，日志不是缓存。环境准备在.local隔离，签名密钥仅本地且0600。

## T02 过渡规则

- config/build-profiles.json 的 java-probe 白名单为空：默认仍不允许JNI/Backup写入。未来例外须精确库路径、相机ABI、SHA256、上游commit、许可和本地审查记录；源码例外还须绑定 sony/src 的文件hash及精确符号。未经批准的ABI/额外库/变更字节失败。没有为本机启用任何native例外。
- tests/fixtures/v0.6 保留旧unknown状态。生产状态允许进展，但implemented、真实运行时、模型或机型profile等真值必须有匹配报告与工件hash。软件工作区的未实现文字仅在发布器确未实现时要求。
- release-check检查全部必需门禁，拒绝删门禁；启用的optional_features也检查。报告路径须仓库内、非空、防路径穿越和符号链接逃逸；报告、工件hash及型号/固件/APK/计划绑定匹配。JSON拒绝重复键和NaN等常量。
- 人工报告可以撒谎：schema/hash只能检验一致性，不能证明实验发生或图像质量；最终仍须审阅真实样片/操作。测试使用临时合成证据，绝不写入生产通过报告。

## 未完成的资格

本次未实现NativeColorStore、相机导入器、原生预览模型或JNI构建。可选API16隔离、ELF符号/链接依赖、真实JNI来源与ABI鉴定、逐门禁专用取证语义和人工证据审核流程仍在T02/T05中。不能把一个带自报reviewer的JSON当独立认证。工具链qualification_complete仍false；公开发布仍受阻。
