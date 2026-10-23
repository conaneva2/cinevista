# T01 主机工具复用决定（2026-09-19）

问题：已有探针只有Java语法检查，缺真实API10 SDK和可用JDK。

采用：Google官方API10 r02和Build Tools30.0.3；Eclipse Temurin17.0.20.1+1 macOS aarch64。精确URL、分发hash和实际android.jar hash位于config/toolchain.lock.json；下载与校验记录位于handoff/runs/20260919T141703Z/toolchain-downloads.json。Google存档按官方XML的SHA1/大小校验，另计算SHA256；Temurin按发行方SHA256核对。官方索引和上游构建脚本的元数据hash另存。

许可范围：Android SDK分发受包内/官方android-sdk-license条款约束，不改标MIT，不纳入源包再分发；Temurin/OpenJDK为GPLv2 with Classpath Exception，保留下载包LICENSE/legal。所有工具和原始分发留.local，仅输出APK包含本工程代码/资源及正常构建结果。此次没有引入Film Studio代码、素材或任何用户照片。

复用参考：Recipe Lab MIT，固定d4c64239ddb775e11b9343b54bc71616dd62a7a5/build.sh，只审阅既有aapt/javac/D8/zipalign/apksigner路径；未移植源代码。Recipe Lab使用platform28/NDK的部分没有照搬，幕野继续真实API10 bootclasspath且无JNI。已有统一Python编排保留，不另造编译器、DEX生成器或签名器。

替代方案：系统JDK不存在；Homebrew全局安装没有必要，采用官方ARM64 tar包本地解压。API28替代不需要，因为API10官方存档可取得。Linux构建备用暂不启用，本Mac已执行成功；可复现发行和JNI旧NDK另作资格验证。

维护/退出成本：删除.local/toolchains可移除本轮局部工具；不要删除.local/cinevista-debug.jks，以免失去同包更新身份。不修改shell配置、系统安全开关或USB驱动。当前未准备或执行Sony-PMCA-RE安装，T03需先固定并审查安装器与Python依赖。
