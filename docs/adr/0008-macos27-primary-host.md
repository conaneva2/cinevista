# ADR 0008 — Apple Silicon / macOS 27 是用户主环境

状态：采纳主环境；实际运行仍未验证。日期 2026-09-19。

v0.3 的 Linux x86_64 不再是对用户电脑的要求。Mac 负责编辑、配方工具、主机测试、优先的 APK 构建及 USB 安装；Linux x86_64 保留作 CI/旧 native 工具备选。

沿用 Recipe Lab 的官方工具顺序：javac → D8(min-api10) → aapt → zipalign → v1签名 → verify。Android CPU 与 Mac CPU 分开；纯Java探针无需旧 NDK，不强制在ARM Mac执行上游 Backup JNI。

上游 compile platform28 与 minApi10 不是矛盾。幕野现阶段仍要求真实 API10 bootclasspath 作额外 API 闸门；不得将缺失的旧平台库用假存根补齐。取得 API10 分发包并记录来源、哈希。需改门禁时另立证据和 ADR，不静默提高 minSDK。

Mac 先鉴定 PMCA CLI + MTP/libusb。官方 README 的 MSC 驱动说明不构成 macOS27 上驱动可用证明。任何驱动回退都不默认关闭 SIP、全局 Gatekeeper 或降低启动安全级别。
