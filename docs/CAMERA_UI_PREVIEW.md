> 2026-09-20更新：用户已确认第一款暗色大字方案及顶部贴边修订。当前原生取景页已使用probe_viewfinder.xml，不再全部由Java建控件。新增viewfinder.html为有限结构近似；下方早期首页范围说明保留为阶段记录。语言资源目前已覆盖三页操作提示，尚无英语/语言选择，原始诊断保持稳定。

# 相机界面制作与预览

## 实际实现

幕野相机端是旧版 Android 原生 View 应用，不是 Studio 网页。首页现在由 `app/res/layout/probe_home.xml` 描述，MainActivity 只绑定动作；Android 自己负责测量、排版和焦点。PreviewActivity 仍以 Java 创建 SurfaceView、按钮和 Canvas Guide；真实图像来自 CameraSession，Sony 私有调用留在 sony 模块。此次不更改捕获生命周期。

普通宽幅构图框是几何叠层，不能当成内容反挤压。界面结构预览也与 Studio 的颜色预览、相机原生响应模型分别记录。

## 三种预览的用途

| 方式 | 能看什么 | 当前状态与边界 |
|---|---|---|
| 本地 HTML 结构草图 | 首页文字、入口排列、不同假设视口下的滚动 | 本轮已运行；浏览器字体/按钮/焦点不是 Android 精确外观 |
| Android Studio Layout Editor | 同一 XML 的原生控件静态布局、主题、字号与尺寸 | 官方支持；本机尚未安装/接入；现有工程是 SDK CLI 构建，并非可直接同步的 Gradle 工程 |
| Android Emulator / 真机 | 实际 Activity 导航和按键；相机上还可测 Sony Surface、EVF | 本轮未运行；模拟器不具有 Sony 私有系统，不能验证相机能力 |

OpenMemories-Framework 提供 dummy 实现供普通 Android/模拟器使用，但不等于我们的 SonyCameraAdapter 已支持模拟器。后续应建立明确的开发专用装配入口，隔离假数据；不能在发布 APK 中遇到相机错误就静默使用假后端。

## 现在如何看

在仓库根目录执行：

```sh
python3 tools/preview_camera_ui.py
open build/camera-ui/index.html
```

生成的 HTML 无外部依赖，可断网打开；修改 XML 后重新生成并刷新。按钮只显示所选入口。640×480、800×480、480×320 是设计检查假设，不是已读取的 A7R II 参数。源布局 SHA256 显示在页面，便于知道预览来自哪版文件。

脚本只支持当前首页的四种节点，不是通用 Android XML 渲染器；新增控件或字符串资源需同步扩展支持或转用原生工具。它不承诺 dp/sp、主题、默认 padding、硬件键、横竖屏或像素比例一致。不能把此页面截图填入机测报告。

## 原生预览接入顺序

1. 从 Google 官方渠道取得 Apple Silicon 版 Android Studio，并核验版本/来源；单独记录新增 SDK 和磁盘占用。
2. 为现有源码/资源目录增加可导入的开发配置，保持资源唯一来源；固定 Gradle/插件/SDK，不替换当前已验签的 API10 CLI 构建链。
3. Layout Editor 打开 probe_home.xml，选横屏、平台黑色全屏主题，按实际读回的逻辑尺寸、density 和字体倍率检查；未读到设备信息前只使用假设配置。
4. 开发专用运行入口通过接口替换设备读取/相机后端；明确显示模拟状态，与相机 APK 分包隔离。模拟器系统架构与相机 ABI 无关。
5. 在 A7R II 上确认启动、方向键/确认/返回、滚动和 LCD/EVF；Surface 内容和颜色效果单独机测。

本轮只完成第一个结构预览与资源解耦，未声称 Android Studio 同步、模拟器运行或相机界面验收完成。

## 本次复用决策与来源

- 采用已锁定的 Google API10 r02 Views/资源系统和 Build Tools30.0.3；来源/hash/SDK许可记录沿用 config/toolchain.lock.json 与工具链台账，不新增 APK 库。
- [Android 官方布局说明](https://developer.android.com/develop/ui/views/layout/declaring-layout)：XML 与代码均可创建布局。本项目采用 XML 分离结构和事件。
- [Android 官方 Layout Editor](https://developer.android.com/studio/views/layout-editor)：原生静态预览的优先路线；本轮未安装，不能声称已工作。
- [OpenMemories-Framework](https://github.com/ma1co/OpenMemories-Framework/tree/f8df3504d8684433a331ee869e64f67cc8be9730)：既有审查固定提交，MIT；候选 dummy 后端可供 Android/模拟器测试。本轮不复制代码、不引入其 SNAPSHOT/JCenter 依赖。
- 拒绝为了结构草图实现 Android 完整排版引擎。仅用 Python 标准库 ElementTree/HTML escaping 输出有限节点的近似结构；无新增第三方包。Java 控件真实渲染仍交给 Android。
- 未引入 Film Studio 代码、字体、照片或模型。

## 中文优先与国际化（2026-09-19用户确认）

相机App和Studio的默认产品语言为简体中文。当前探针尚未全量汉化，以下是实施约束，不是完工声明。

Android原生资源系统允许多语言：完整默认中文放values/strings.xml，后续英文放values-en、繁体候选values-zh-rTW。资源默认值并不等于用户首次语言偏好：有英文资源时英文系统会自动匹配英文。因此若首次启动必须中文，需要App专用语言偏好与兼容旧Android的资源配置边界；不要直接依赖Android13的每App语言功能，也不要改Sony系统语言/地区或持久槽位。

建议设置项为“简体中文 / English / 跟随系统”；先完成中文资源化，再引入经测试的英语，其他语言逐项扩展。界面可翻译，协议字段、日志事件ID和颜色计划指纹不随语言改变。切换语言不能隐式重启拍摄流程或丢失冻结意图。中文字体覆盖取决于目标固件，需检查实机；若缺字，再审查可分发字体、包大小和旧版Typeface加载路线。

依据：[Android本地化资源](https://developer.android.com/guide/topics/resources/localization)、[旧版Configuration.locale字段](https://developer.android.com/reference/android/content/res/Configuration#locale)。可行性来自Android机制，不等于目标Sony固件已通过。

## 设计参考筛选（建议，尚未由用户选定）

用户提供[VoltAgent awesome-design-md](https://github.com/VoltAgent/awesome-design-md)。本轮阅读其Linear、IBM、Apple设计分析；这是社区整理的网站分析，不是各品牌官方相机组件库。

首选Linear的克制暗色层级作为整体视觉参考，结合IBM的明确结构与状态表达；Apple的影像优先适用于Studio样张与A/B区域。相机取景占主体，中文短标签、大而清楚的焦点、固定按键提示优先。只借鉴原则，不复制品牌标识或专有字体，不引入其网页代码。

- [Linear分析](https://github.com/VoltAgent/awesome-design-md/blob/main/design-md/linear.app/DESIGN.md)：适合Studio工具面板与相机菜单的暗色层级；小屏需提高分隔和焦点辨识度，不能照搬细灰线与小字。
- [IBM分析](https://github.com/VoltAgent/awesome-design-md/blob/main/design-md/ibm/DESIGN.md)：借鉴方正布局、信息分组和语义状态，用于发布/备份/恢复；不照搬白底营销页。
- [Apple分析](https://github.com/VoltAgent/awesome-design-md/blob/main/design-md/apple/DESIGN.md)：借鉴影像主导，适用于Studio大图；不照搬官网巨型标题和大量留白。

幕野候选方向：中性炭黑/灰界面，白色主文字，少量琥珀色焦点；危险操作保留红色且配文字，不能只靠颜色。相机端不采用玻璃模糊、悬停专属功能或持续动效；Studio可使用更丰富布局但共享语义。配色是本项目建议，不是假称来自Linear的原色，也未通过实际摄影环境校验。

## 已选方案实现边界

标题栏是垂直根布局第一子节点，取景Surface位于第二个独立FrameLayout；不把全屏取景放在标题后面。Sony底层显示层最终是否遵守区域仍需设备确认。控制20sp、最小60dp高度，初始焦点在画幅；实际density和中文字体仍需读取并机测。

设置中的Surface尺寸实验默认关闭；正常倍率选择仍不能被声称为实时反挤压成功。设置/诊断Dialog通过运行时键映射适配方向、确认和返回，不硬编码Sony数字键。普通Android按键走平台默认行为。

文字与主题用API10平台资源系统（现有GoogleAPI10r02/BuildTools30.0.3），Dialog用平台AlertDialog；没有新增框架或字体依赖。图标暂用清晰文字控制，不引入未经审查字体/图片。原概念的照片不是运行画面，未装入APK。

`python3 tools/preview_camera_ui.py`同时生成首页与`build/camera-ui/viewfinder.html`。浏览器仅近似XML/样式排版，示意倍率与画幅选择，未连接相机。控件大小、对话框、字体和Surface不能由此精确认证。`build/camera-ui/approved-reference.png`是本机概念参考，可选，不随源码分发。
