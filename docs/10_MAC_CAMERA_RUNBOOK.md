> 2026-09-20现状修订：主机Apple Silicon/macOS（历史测试平台）已核实，真实APK已构建。PMCA隔离环境已准备、libusb加载及无设备枚举成功，尚无机身通信/安装。下方初稿“无APK/工具链未知”是历史记录；当前操作以[连接环境](CAMERA_CONNECTION.md)和PROJECT_STATUS为准。

> **v0.6修订优先：** 后端主线改为原生颜色持久化，同时保留实时样张创作。参见 `15_NATIVE_PERSISTENCE.md` 和 ADR0011。下文的软件主线/永不持久写入/所有机身API10表述作为历史设计，不覆盖新决定。实现状态仍以 PROJECT_STATUS 为准。

# 幕野 v0.4｜Apple Silicon Mac → A7R II 实施手册

日期：2026-09-19。历史参考配置：Apple Silicon/macOS（参考平台）。具体芯片、系统 build、机身固件仍未知。

## 1. 三个不同运行环境

- **Mac**：写代码、跑测试、编写配方、生成 APK、经 USB 安装。
- **相机**：安装兼容 Android 2.3.7 / API10 的 APK；断开电脑后从 MENU → Application → Application List 独立运行。
- **Studio**：Mac 本地颜色创作工具；输出数据，不是重新生成整台相机的固件。

Mac 是 ARM64，不代表相机 APK 要编成 arm64-v8a。纯 Java 是 DEX；若以后引入本地库，按相机 ABI 独立验证。Recipe Lab 目前的 JNI 是 armeabi，不是 Mac 的架构。[M01][M02]

不需要 App Store、Apple 开发者账号或 Xcode iOS 工程。系统 Command Line Tools 可供 git/native 工具使用，但不等于 Android SDK。不开相机温控、地区、校准或保护设置，不靠刷固件安装。

## 2. 本轮按 Recipe Lab 复核了什么

读取了实际 build.sh、FAQ、PMCA USB 调度与 requirements。

| 上游实际实现 | 幕野采用或区分 |
|---|---|
| JDK17、Build Tools30.0.3、platform28编译入口 | 保持候选版本，不自动升级整套工具链 |
| javac → D8 --min-api10 → aapt → zipalign → v1签名 → verify | 采用相同基本流程；构建脚本使用 java -cp d8.jar |
| Manifest minSDK/targetSDK10 | 相机运行时约束不因Mac系统新而改变 |
| NDK r16b、armeabi、Backup JNI | 原生Java探针不需要；不为接配方整包引入未知持久化写入 |
| 原生CameraEx取景、相机按键 | 已有工程保留索尼适配层，不迁入Studio |
| 应用内调整配方，永久保存颜色 | 幕野先做App内生效；永久PP写入另立验证，不能复制A6000槽位 |
| FAQ明确：尚不能命名/保存个人配方；77款内置 | 我们新增数据格式、Studio和Camera导入器，不声称现有RecipeLab会读.CVL |

上游在编译时用 platform28，而运行时仍为10，二者不冲突。幕野额外保持真实 API10 bootclasspath 检查，缺少时不能用假存根掩盖。**目前没有任何一次完成的幕野 APK 构建。**

## 3. Mac 环境准备（命令供你在Mac执行，本轮没有在Mac运行）

优先全套 Apple Silicon 原生 JDK/Python/Homebrew。只在遇到确实为Intel的旧SDK工具时使用系统提供的兼容能力。Apple官方明确通用Rosetta支持到macOS27；这不是所有旧驱动/NDK必然兼容的证明。[M05]

已安装 Homebrew 的情况下：

```bash
brew install openjdk@17 python@3.12 libusb
# 仅开发Studio测试需要；打开编写台不需要Node。
brew install node@22
```

不要将这些命令当成软件版本锁；鉴定成功后记录实际patch、来源与hash。不要sudo pip，不把arm64 Python与Intel libusb混用。

通过官方Android Studio或Command-line Tools安装SDK，默认目录：`$HOME/Library/Android/sdk`。然后在工程根目录：

```bash
source .env.macos.example
python3 tools/macos/doctor.py
sdkmanager --licenses
sdkmanager --list --include_obsolete
sdkmanager 'build-tools;30.0.3' 'platforms;android-28'
# 只有上一条列表确实包含此包时再执行：
sdkmanager 'platforms;android-10'
```

`--include_obsolete` 官方用于列表/更新，不给安装命令乱加。若列表没有旧平台，先从可验证的官方归档取得API10包并记录来源/hash；不可把重命名的28 jar冒充10，也不要下载来源不明的“修复SDK”。[M06]

```bash
file "$ANDROID_SDK_ROOT/build-tools/30.0.3/aapt"
file "$ANDROID_SDK_ROOT/build-tools/30.0.3/zipalign"
"$ANDROID_SDK_ROOT/build-tools/30.0.3/aapt" version
python3 tools/cv.py doctor --android
python3 tools/cv.py check
node --test studio/tests/*.test.js
python3 tools/cv.py android
```

SDK原生可执行文件若因架构、动态库或新系统不兼容而失败，记录准确错误。不批量关闭Gatekeeper/SIP、不降低启动安全级别“试试看”。优先将构建阶段移到固定Linux x86_64 CI；Mac仍负责编辑和安装。容器构建并不自动解决USB，USB不默认透传给Docker。

## 4. 先验证安装通路，再拿幕野验证应用

推荐顺序：

1. 先读取相机型号/固件，证明数据线、USB模式和权限可用。
2. 使用已知项目的最小演示APK验证安装/启动；PMCADemo比直接套颜色更适合作基线。不要在未确认的A7R II上首先运行Recipe Lab全局写入。
3. 安装我们的Probe，依次验证取景、一次快门、回执和显示比例。
4. 各项留下日志，再扩展导入颜色、照片出片。

存在M1 MacBook给A7R II安装TimeLapse成功的第一人称记录（2022年，2023年补充），路线是命令行、MTP、可传数据的micro USB线；部分权限错误通过特定sudo调用解决。[M04] 它不是macOS27验证记录。

### 4.1 配置 PMCA 的独立 Python 环境

```bash
mkdir -p "$HOME/Developer"
cd "$HOME/Developer"
git clone https://github.com/ma1co/Sony-PMCA-RE.git
cd Sony-PMCA-RE
git rev-parse HEAD           # 保存本次上游commit；后续基线固定在该commit
"$(brew --prefix python@3.12)/bin/python3.12" -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip freeze --all > pmca-requirements-qualified.txt
python pmca-console.py --help
```

上游有老旧或未锁定依赖，不把这次pip成功与否预设成已知。旧requirements如果冲突，应提交独立兼容补丁并做回归；不能悄悄修改上游、又说完全原版。冻结文件是鉴定记录，不代表已完成供应链审查。[M03]

### 4.2 第一路：MTP + libusb

退出可能占用相机的照片导入、Image Capture、Imaging Edge、云盘自动导入等软件。连接支持数据传输的线；相机菜单USB Connection设MTP。Mac提示是否允许USB附件时正常允许。**不是PC Remote，也不是默认依赖Mass Storage驱动。**

```bash
# 在Sony-PMCA-RE目录及其venv内：
python pmca-console.py info -d libusb
# 仅在确有可验证APK以后：
python pmca-console.py install -d libusb -f /absolute/path/CineVista-Probe-0.4-debug.apk
```

命令名称、-d libusb和-f都来自上游，不自研安装协议。上游info输出可能含序列号和GPS信息，公开日志前删除这些信息；幕野doctor不连接相机、不收集这些数据。[M02][M03]

若只在USB访问上明确报权限错误，先核对设备占用；确需提权时用已审查的上游与当前venv绝对路径，只提权那次操作：

```bash
PMCA_PY="$PWD/.venv/bin/python"
sudo "$PMCA_PY" "$PWD/pmca-console.py" info -d libusb
```

不要用sudo重新安装Python依赖；不要让sudo切换到另一套Python架构；不要以关闭全机保护作为前置。安装错误不能通过serviceshell/updatershell猜测修复，这两个不是本项目的标准安装路线。

### 4.3 第二路：Mass Storage / 原生驱动

上游macOS说明要求MSC路径安装Sony Camera Driver，且说Mac二进制比Windows少测试。[M02] 我们没有核验macOS27上该驱动与A7R II组合，所以不把“装这个驱动即可”当结论。必须独立确认版本、官方OS支持和权限要求后再决定。

若MTP路径确实失败，先判断是数据线、占用、依赖、证书、USB切换还是相机任务错误。使用另一台已支持主机只安装一次可以是备选，但不是要求你换开发电脑。

### 4.4 装完后怎样跑

以上游电脑终端的安装成功结果为准，不因相机停在Connecting界面就认定失败。安全断开后按需要重开相机，从 `MENU → Application → Application List → CineVista Probe` 启动。之后独立运行，不需要连着Mac。具体名称以当前manifest为准。

不要默认自定义键、开机自启、原生菜单全局反挤压或普通USB ADB直接可用。上游FAQ也明确其启动入口是Application List。持续ADB调试若要启用，需另行授权和验证，发行版不留网络调试服务。[M01]

## 5. 发布与升级

本工程debug签名保存在`.local`，不得加入仓库/zip。更新同一包名须使用同一签名；Recipe Lab源码也提示改签名无法覆盖旧安装。[M01]

不要反复生成新密钥再让用户卸载丢配方。正式发行会独立固定包名、versionCode、签名备份与fingerprint。APK通过D8/签名/接口检查只代表构建，不代表机身已通过。

## 6. 本轮可直接用的入口

- `python3 tools/macos/doctor.py`：环境报告，不装东西、不碰相机。
- `open studio/index.html`：本地配方编写台；本轮Safari/macOS27尚未验证。
- `python3 tools/cv.py check`：原工程主机检查；本轮已复跑。
- `node --test studio/tests/*.test.js`：配方契约22项测试；本轮已执行。
- `.env.macos.example`：Mac路径示例。

相机固件未知、真实SDK缺失、USB未连接时，报告保持unknown，不写兼容概率。
