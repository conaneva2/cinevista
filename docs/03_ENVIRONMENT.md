> **v0.6修订优先：** 后端主线改为原生颜色持久化，同时保留实时样张创作。参见 `15_NATIVE_PERSISTENCE.md` 和 ADR0011。下文的软件主线/永不持久写入/所有机身API10表述作为历史设计，不覆盖新决定。实现状态仍以 PROJECT_STATUS 为准。

> v0.4变更：参考开发平台为Apple Silicon/macOS（参考平台）。以下Linux基线改为CI备选；完整Mac路径见10_MAC_CAMERA_RUNBOOK.md。

# 03｜开发环境、工具链与构建方式

> 当前实测修订：本Mac的真实API10构建已完成，工具链精确版本/hash见config/toolchain.lock.json；下方早期缺SDK/Linux描述为历史候选。历史兼容测试平台为Apple Silicon/macOS（历史测试平台），远端方向为Gitee私有且CI尚未接入。现有.local/env.sh可加载本机工具，其他电脑需独立按来源配置。

## 选择：现代开发主机，严格旧版运行时
| 项目 | 基线选择 | 当前状态 |
|---|---|---|
| 主验证环境 | Linux x86_64，CI Ubuntu22.04 | 本机为 Linux；CI未运行 |
| 日常编辑器 | VS Code + Java 支持 + Python；可使用其他 IDE | 仓库提供 tasks.json，不依赖 IDE魔法 |
| 主JDK | JDK17；额外 JDK21 做主机回归 | 本轮实际执行哪个版本见 doctor；不是已测双版本 |
| Python | ≥3.10，建议3.12；工具仅标准库 | 运行时由 doctor记录 |
| 相机程序 | Java，轻量 API10 View/Canvas | 不用 Compose/CameraX/Room/WorkManager |
| 编译平台 | 原始 Android API10 android.jar | 当前环境缺失 |
| Android Build Tools | 30.0.3 为初始候选固定版本 | 未鉴定整套组合，不宣称已成功编译 |
| Java语言/字节码 | 保守 Java8源/目标；相机模块用 API10 bootclasspath | 不允许因此调用 Java8平台新增类 |
| DEX/签名 | DEX035，v1签名必须通过 SDK10 检查 | SDK构建后实际核验 |
| 安装 | 外部 Sony-PMCA-RE，宿主原生USB | 固定真实使用版本后实测 |
| Native | 不作为当前 APK 必须依赖 | 需要软件后端时单独鉴定 ABI/NDK/链接 |

这不是对某个最新发行版的推荐；是为了隔离遗留平台风险的拟议基线。确切 JDK分发、SDK包与哈希在首次成功构建后写回 lock；未知值保持 null。主机离线测试通过不等于工具链鉴定结束。

## Windows / macOS
Windows 推荐在 WSL2/Linux 中编译，在 Windows 原生执行 PMCA安装；不要把 USB 透传问题混在 APK 问题里。也可原生 Windows 运行本仓库 Python/Java工具，Android脚本依赖工具可执行入口仍需实际验证。

macOS 可以作为编辑与主机测试环境。旧版 SDK/NDK宿主二进制在 Apple Silicon 的兼容性不得预设；APK优先由 LinuxCI/独立Linux环境构建，安装在直接连接相机的主机进行。Linux容器做编译隔离，不把容器当有相机USB的模拟器。

本轮不提供宣称可立即工作的 Dev Container 或打包 SDK镜像，因为 Android10 SDK缺件及分发条款未完成鉴定。取得合法分发后再固定镜像 digest；不能塞入来源不明 android.jar 让编译器安静。

## 为什么第一阶段不用整套最新 Android Gradle Plugin
并非禁止 Gradle，而是我们已有简单、可检查的官方SDK命令链；迁移未经验证的 AGP组合会新增另一组兼容问题。先沿用官方工具，以小型Python入口串联。D8官方文档支持独立使用、指定min-api和android.jar。[S16]

编译顺序：模块分开javac → aapt资源与manifest → D8(min-api10) → zipalign → apksigner → 包检查。具体先后以脚本资源类生成需求为准；zipalign必须在签名前。[S17] 本工具不实现Java编译、图像codec、DEX生成或签名算法。

不把这个入口扩成包管理器/依赖解析器。外部JAR增多或IDE集成确有收益时，写ADR选择经过实测的Gradle Wrapper组合，仍调用相同模块契约、API检查和测试。禁止为了用新AGP而提高相机minSdk，禁止继续复制依赖jcenter/SNAPSHOT的旧示例而不锁定。

## 可执行入口
```sh
python3 tools/cv.py doctor
python3 tools/cv.py check
python3 tools/cv.py doctor --android
python3 tools/cv.py android
python3 tools/cv.py release-check
```
Windows可用 `python` 替换 `python3`。前两条不自动联网安装依赖。

`check`=边界与规范检查、工具负向测试、Java模块编译/44项既有回归、Python差分、Android源码语法检查、Python原参考回归。`android` 缺SDK必须退出非零，不生成假APK。`release-check` 是生产发布门禁；未知项会阻断，不能用它阻断结果说明代码测试失败。

设置 `ANDROID_HOME` 或 `ANDROID_SDK_ROOT`，以 `.env.example` 指明的变量为准；文件只是说明，脚本不暗中读取或上传用户环境。SDK安装条款由用户/维护者主动接受。

## 获取旧SDK
优先官方sdkmanager/已授权官方存档或可信的个人缓存；检验来源与哈希。手工Android工作流尝试 `platforms;android-10` 与`build-tools;30.0.3`；如果服务器不再提供平台包就真实失败，不假设“写了sdkmanager命令就能成功”。不得用现代android.jar替代API10，导致类型检查失真。

## 原生工具链的独立门槛
Recipe Lab/旧libjpeg包装工程可以作为旧NDK经验，但它们不能证明任意新codec在该工具链可编译。需要：真实机身ABI/CPU特性、最低导入符号、库依赖、NDK版本、C/C++运行库、许可证、安全修补可维护性、安装加载测试。默认只用可移植标量路径，未确认不得强开NEON/现代ABI。

旧工具链置于隔离的构建环境，不运行不可信native样本，不提供网络服务。图像输出和实时帧处理可以分别鉴定，无需为“以后可能用C++”现在就引入NDK。

## 可复现程度
当前是“有可复核命令和候选版本”，不是“任何电脑位级相同APK”。完整资格要求：依赖SHA256、Git提交、JDK/SDK精确分发、平台环境、生成资源策略、源码路径/时间戳处理、签名方式、两次干净构建的差异解释。正式签名密钥不得进仓库、普通PR任务或下载包。
