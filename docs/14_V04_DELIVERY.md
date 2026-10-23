# 幕野 v0.4｜Mac安装路径与自制胶片颜色

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


---

# 幕野 Studio｜颜色创作与 A7R II 输出设计

日期：2026-09-19；当前交付：原生配方编写台0.1 Alpha。不是完整LUT调色软件。

## 1. 产品成为双端，不成为两个互相依赖的庞然大物

**幕野 Camera**：相机内的取景、宽画幅、反挤压、拍摄与出片。

**幕野 Studio**：Mac本地创作、管理、比较和导出自己的颜色。你可以从空白配方开始，也可以在授权范围内改编Recipe Lab配方；不用为了每一种新颜色重新编APK。

Studio不做胶片名称选择器就结束。最终工作台应支持样片集、颜色编辑、前后对照、配方版本和目标机身检查。当前先交付真实可实现的原生参数编辑与菜单设置单；软件图像级调色另做后端。

## 2. 三个颜色后端，两个工作区

| 后端 | 颜色由谁执行 | 预览来源 | 文件/限制 |
|---|---|---|---|
| sony-creative-style | 相机原生颜色参数 | 机内Live View及JPEG；Mac只展示实拍/明确标记的未来拟合预览 | .CVL；优先RAW兼容普通参数 |
| sony-picture-profile | A7R II原生PP参数 | 机内PP预览及实拍；App写入能力逐项核实 | .CVL＋手工单；不复制A6000私有槽 |
| software-lut | 幕野拍后像素管线 | Mac受管理的软件预览；与实际JPEG相同输入变换 | .cube＋manifest；机内输出耗时实测；不承诺实时取景 |

前两个构成**原生配方区**；第三个构成**自由调色区**。它们不能混着显示一组任意曲线，然后假设同一条曲线能写进Sony菜单。

Recipe Lab现有FAQ明确个人配方命名保存尚未实现，且不处理LUT。我们复用它的运行时参数方法，不假设它已有.CVL或.cube导入。[M01]

## 3. 为什么 A7R II 不应只按 A6000 的能力设计

A7R II官方帮助列出PP1–PP7；Gamma包括Still、Movie、Cine1–4、ITU709、ITU709(800%)、S-Log2；有Black Level、Black Gamma、Knee、Color Mode、Saturation、Color Phase、R/G/B/C/M/Y Color Depth和Detail。[M07]

这让**自定义原生外观**比只调饱和/锐度有更丰富入口。但它仍不是任意3D LUT：六色Depth不是独立Hue/Sat/Luma曲线，Gamma枚举也不是任意上传曲线。A7R II的这份官方页面没有S-Log3，不从A7S II帮助复制给它。

PP菜单能力已由官方资料确认；App接口是否存在、参数是否可读写、拍照/取景是否生效、是否与RAW/CreativeStyle/DRO互斥，要分别测试。首版PP自动写入门禁保持关闭。可输出手工单先在人可控菜单里试色，形成实际样片。

改变Gamma可能影响ISO范围；曝光改变会影响RAW记录。WB/色彩不能笼统说“只改JPEG所以无任何拍摄影响”。原片已带外观的JPEG也不能当成中性原始数据任意逆转。

## 4. 原生配方区：真正可用的调色循环

1. 选A7R II档案及实际固件，不选不存在的能力。
2. 创建/复制配方；选CreativeStyle或PP，调整其实际支持参数。
3. 记录场景和曝光、白平衡条件；名称如“雨天街景01”只是用户命名，不宣称已模拟某品牌。
4. 导出.CVL；Camera导入器完成前输出手工设置单，在原生菜单录入。先备份当前PP数值，不随机覆盖PP1。
5. 同机位同光线拍下有肤色、绿植、饱和色和灰阶的真实样片；回到Studio作A/B。
6. 修改版本、复拍，满意后保留配方及对应样片证据。

原生预览不能从一张普通JPEG精确逆算相机全部处理。未取得/标定Sony原生流程前，**电脑端滑杆不伪装成精确实时颜色**。可采用真实配方样片接触表；之后再研究明确标记的近似模型。

未来“连接相机→推送参数→返回取景”是加速迭代的独立传输层。PMCA安装模式不等于可边拍边远程调色；USB/MTP、相机App与预览并发能否成立必须另验。首版通过读卡器离线传文件，不让实时网络服务成为相机常驻依赖。

## 5. 自由调色区：你在Mac上真正看着图调色

这是最终必须补齐的另一块，不用原生参数的有限能力替代它。

目标：载入受控sRGB JPEG样片组、参考图；全局曲线、色相/饱和、阴影中间调高光、亮度与色彩对比；A/B与多场景同步；导出17/33点等经过设备鉴定的3D LUT。采用成熟LUT解析/色彩处理库或已审查的JPEG.CAM对应实现，不自写通用编解码器/颜色管理。具体库版本与平台构建未鉴定，不在本轮加进runtime。

首版只接受声明为sRGB输入/输出的可用范围，后续明确增加Log等管线。不能把用于S-Log2素材的.cube套在已带风格sRGB JPEG上，再责怪LUT不好。输入基线应记录相机颜色模式、白平衡策略、输出空间和JPEG处理阶段。

3D LUT表达逐像素RGB颜色映射。颗粒、晕光、柔焦、锐化、空间蒙版、动态局部调整不是一个.cube能编码的操作；若加入，必须另有操作清单和成本。原生配方与LUT不要无意双重上色。

机内软件路径：原生JPEG安全落盘→选择的基线到工作空间→LUT→与裁切/反挤压组合→JPEG另存。能够在Mac实时预览，并不承诺老相机实时或高速全尺寸处理。LUT与原生适配版都可以输出，但必须分别命名，不宣传“一键无损转Sony配方”。

## 6. .CVL 草稿契约

- UTF-8 JSON，`schema=cinevista.look/1`，8字符以内ASCII大写id，中文显示名。
- `engine`分离CS/PP；`parameters`使用语义名称，不含硬件地址、代码、shell或任意插件。
- `target`包含ILCE-7RM2与实际固件或null。
- 记录revision、作者、可选上游project/commit/recipe/license；改编不能抹掉来源。
- `exposure`当前只支持手动曝光建议，不自动改摄影师的曝光。
- `validation.status`只能是unverified。设备通过记录单独生成，不能靠文件作者写一个verified越过门禁。
- `software-lut`未来单独规范并带cube hash、颜色空间、数据范围，不混进当前导出器。

拟议SD结构：`/CVLOOKS/MYLOOK01.CVL`。这只是项目约定，不是Sony已有功能。相机并不会因为文件放进卡里就自动读它；必须完成Camera端的导入器。

导入器职责：大小限制、UTF-8/重复键/未知字段检查、schema升级、path限制、版本冲突、必要参数支持检查、有效计划冻结、测试模式确认、不静默改RAW或持久化。校验只读数据，不解包任意zip，不执行任何文件内容。

## 7. 模块与开发任务

Studio模型/校验器与UI分离；Camera端新增LookRepository/LookValidator/ColorPlan/ColorAdapter接口，不依赖浏览器。用同一套JSON测试向量做跨语言契约测试，不共享Sony整数ID。以后软件LUT后端只实现像素变换，不接管快门和文件归属。

任务顺序：

A. Mac安装通路与真实APK基线。
B. .CVL Camera导入器及一条普通CS配方端到端，不导入危险特殊参数。
C. Recipe Lab合法导入与自制配方共享目录、版本和收藏。
D. PP字段只读探针、手工样片，再开放逐项已验证写入。
E. Studio自由LUT工作区及成熟软件后端，单独验颜色/耗时/内存。
F. 可选受控连接预览，不以云端或常驻服务为前提。

A/B与宽画幅、实时反挤压探针并行；颜色不能取代摄影主目标。

## 8. 本轮真正完成

- 本地HTML/JS原生配方编写台；CS/PP参数编辑；导入/导出.CVL；手工设置单；本地A/B图片展示。
- 22项Node契约测试通过，实际输出样例文件。
- Mac环境诊断脚本与安装手册；仅在本地Linux环境试跑诊断，不等于Mac验证。
- 构建脚本按Recipe Lab改成直接调用d8.jar，v1-only签名；未用真实SDK完成构建。

未完成：自由LUT像素调色、Sony精确预览、相机.CVL导入/应用、PP自动写入、APK/USB安装、Safari/macOS27运行验证。

浏览器自动化尝试因本环境管理策略阻止file://及localhost导航而未执行页面验收；未修改安全策略。JavaScript契约测试不替代界面验收。可下载原型供Mac本地检查，不称正式成品。


---

# v0.4 来源与证据补充

查询日期2026-09-19。下列是读取到的资料，不构成macOS27/相机组合的实测认证。

| 编号 | 来源 | 使用范围 |
|---|---|---|
| M01 | [Recipe Lab build.sh](https://github.com/voxivoid/recipe-lab-sony-pmca/blob/main/build.sh)、[FAQ](https://github.com/voxivoid/recipe-lab-sony-pmca/blob/main/docs/FAQ.md) | JDK/D8/minAPI/v1/NDK；个人配方与LUT限制。FAQ有过期的商店关闭年份，本稿没有沿用 |
| M02 | [Sony-PMCA-RE README](https://github.com/ma1co/Sony-PMCA-RE) | Mac少测、MSC驱动、Android2.3.7、安装路径 |
| M03 | [PMCA commands/usb.py](https://github.com/ma1co/Sony-PMCA-RE/blob/master/pmca/commands/usb.py)、[requirements](https://github.com/ma1co/Sony-PMCA-RE/blob/master/requirements.txt) | 原生/Libusb调度、MTP、安装本地APK、依赖组成 |
| M04 | [M1 MacBook安装TimeLapse到A7RII](https://gist.github.com/andrewpye/1230f66a92dee6aecb37fbcad5857564) | 2022年直接经验，2023补充。不能提升为macOS27认证 |
| M05 | [Apple2026-09-01 Rosetta说明](https://developer.apple.com/news/?id=w5ngl9k2)、[翻译环境](https://developer.apple.com/documentation/apple-silicon/about-the-rosetta-translation-environment) | 通用Rosetta覆盖macOS27；不推导旧驱动必然可用 |
| M06 | [Android sdkmanager](https://developer.android.com/tools/sdkmanager) | 包安装、许可、--include_obsolete适用范围 |
| M07 | [Sony A7RII Picture Profile](https://helpguide.sony.net/ilc/1520/v1/en/contents/TP0001093165.html) | PP1–7、参数范围、Gamma/Knee/ISO关系；不是AppAPI声明 |
| M08 | [Sony-PMCA-RE CLI](https://github.com/ma1co/Sony-PMCA-RE/blob/master/pmca-console.py) | info、install、-d、-f命令 |

读取到的blob SHA：build.sh=8992799dede6b01c3273569e74bc3e0e7aedda17；FAQ=8276480d480650cf132d56a64025d6450b12ae88；commands/usb.py=43443f54f2363eb772cbaf9e7925309a9306f832；requirements=44b2b66b66aacb77f26d15fdd20a228e191fc089。链接main/master可变，blob标识留供复核。未把上游运行时原生库或其字体打包。

未找到macOS27+AppleSilicon+A7RII+本工程APK的已验证全链路；只取得正确安装候选和历史同类成功记录。驱动、PP程序写入、图像表现仍需实机。
