> **v0.6修订优先：** 后端主线改为原生颜色持久化，同时保留实时样张创作。参见 `15_NATIVE_PERSISTENCE.md` 和 ADR0011。下文的软件主线/永不持久写入/所有机身API10表述作为历史设计，不覆盖新决定。实现状态仍以 PROJECT_STATUS 为准。

# 幕野 Studio｜实时调色是主流程（v0.5）

日期：2026-09-19。用户新要求：**导入样张，看着实时效果调整，然后导出给 A7R II 上的幕野使用。**

## 1. 对上一版的修正

v0.4 的参数编写台不能满足此核心要求：调整数值不改变导入样片。不能把“回到相机试拍，再回来比较”当成主流程完成。旧工具保留为 `studio/native.html` / `CineVista_Studio_0.1.html`；现在 `studio/index.html` 默认进入真正的软件颜色工作区。

主流程：导入本地样张 → 连续调整 → 原图/当前/分屏对照 → 多样张检查 → 保存可编辑工程 → 导出颜色数据 → Camera 软件像素管线应用（尚待接入）。

## 2. 本轮实际交付

Studio 实时调色 0.2 Alpha：

- JPEG/PNG 本地载入；最多 6 张切换，同一组调色参数；文件上限 50 MiB、解码后像素上限 6500 万（不是对浏览器解码峰值内存的保证）。透明 PNG 白底合成。
- 数字亮度、冷暖/绿洋红创作偏色、对比度、饱和度、低饱和色增强、暗部/亮部亮度、抬黑。
- 五点单调分段线性明暗曲线；阴影/高光偏色；六色色相和饱和度（实现为 HSV，不伪称 Sony 六色 Depth）。
- 输入事件即触发计算，无需点“应用”；Web Worker 避免像素循环阻塞页面；新结果带序号，旧请求不能覆盖新效果。
- 原图、当前、分屏及按住看原图；撤销/重做、恢复中性。
- 17³ / 33³ 两档 LUT，预览从 LUT 采样，而非 CSS/filter 或另一套临时调色算法。
- `.CVG` 可编辑工程；`.CUBE` 标准文本颜色表；`.CVP` 相机素材包草稿（内含同一 CUBE 和输入说明）；预览尺寸 PNG。

Camera 源码未改、Manifest 仍为 0.4-probe。v0.5 是工程包版本，Studio 是 0.2，**不是已完成 v0.5 相机应用**。没有 APK、没有相机素材包导入器、没有机内软件 LUT 渲染实测。

## 3. 预览与导出的一致性契约

1. 当前参数先生成 RGB 3D LUT，节点存为 Float32。
2. 预览对样张 sRGB 像素使用该表，以固定三线性插值采样。
3. 导出使用同一张表，以 9 位有效数字保存 Float32；不是导出后再重新拟合一套 Sony 参数。
4. LUT 为 red-fastest；输入和输出均为 sRGB 编码、full range、[0,1]。不是 Rec.709 limited、不是 Log、不是 linear-sRGB。
5. 17³/33³切换会影响曲线采样精度，因此切换后预览也更新；不能预览33³而导出17³且不通知。
6. 导出按钮在当前参数尚未得到对应渲染结果时禁用，避免导出上一张颜色表。
7. 主机测试对 32768 个随机 RGBA 像素验证：内存中的表与导出后重读的表产生完全相同的字节结果。此结论只限该 CPU 参考范围。
8. 未来 Camera 端应对同一输入像素执行同一表和插值契约。库的默认插值不能代替显式指定；OCIO 文档也指出默认/最佳插值可能随版本变化。[R03]

**同一 LUT 不等于已证明所有相机成片与屏幕逐像素一致。**浏览器/机内 JPEG 解码、颜色转换、缩放顺序、JPEG 重压缩、屏幕校准仍可引入差异。当前预览先缩小，再应用 LUT；高分辨率最终出片可能先应用 LUT，再重采样，两种结果在局部纹理边缘不会严格相同。必须用相同 RGB 数组做颜色核验，再做完整文件链路与感官画质验收。

## 4. 输入基线：只看着图调色还不够

浏览器负责解码，并请求 sRGB Canvas/getImageData；原型检查返回的画布空间（可得时）。这使用平台能力，不自制 JPEG 解码器或 ICC 颜色管理。[R01][R02]

这并不证明相机源文件本来就是 sRGB，也不把已调色 JPEG 逆转为 RAW。相机素材包导出要求记录实际输入条件，并确认用于同一 sRGB 基线。这是用户声明，不是自动识别认证。

建议用 A7R II 将来软件上色之前的真实 JPEG 做样张。记录 Creative Style 或 PP、DRO、白平衡策略等；允许选择自己的基线，不把某个猜测的 Neutral 设置强行称为“标准底片”。不要拿一张有别家 LUT 的成片调色，再将得到的表套到完全不同的相机 JPEG。

数字 EV 是对已记录像素的编辑，不会恢复拍摄时丢失的高光；冷暖和色调是创作偏色，不是精确模拟光源色温和相机传感器白平衡。HDR/Log/RAW/P3 原始管线与完整 ICC 元数据识别不是此版功能。

## 5. 为什么与 Recipe Lab 分开

Recipe Lab 调用相机已有参数，不做像素 LUT 调色；上游 FAQ 明确区分这两条路线。[R04] 它的配方仍保留在原生路线，不能被软件工作区替换或抹掉来源。

但是，任意曲线和六色色相调色不保证能由 Sony 菜单有限参数精确复现。因此：

- **主工作区 software-lut：**所见颜色导出为 LUT；将来由幕野在相机内拍后执行。
- **辅助原生区 CS/PP：**保留原有编写台；没有相机流程标定之前，不在 Mac 上伪装为精确原生模拟。
- 可以后续研究 LUT 到原生配方的近似拟合，但必须独立命名、显示误差，不能把它当成无损转换。

电脑实时调色，不构成 A7R II 实时取景 LUT、视频上色或高分辨率秒出的承诺。机内处理时间、内存、耗电与连续拍摄行为分别验收。原片仍应先安全落盘、保留不变。

## 6. 文件职责，不把自定义格式叫索尼格式

| 文件 | 作用 | 当前消费者 |
|---|---|---|
| `.CVG` | `cinevista.grade/1`；算法版本、参数、输入基线 | Studio 可保存、重开继续调整 |
| `.CUBE` | 17/33点、[0,1] RGB；三线性解释约定 | 可导出；通用软件如何解释仍需设置正确 |
| `.CVP` | `cinevista.lut-package/1`；内含同一 CUBE 文本和工程声明 | 草稿数据包；Camera 导入器未完成 |
| `.CVL` | 旧原生 CS/PP 参数草稿 | 原生编写台；不是本 LUT 格式 |

.CVP 是单个有界数据对象，不是任意 ZIP、不包含图像、脚本或硬件地址。本轮没有签名、完整性散列或 Camera 解析器，不宣称安全生产导入。后续导入器需要大小限制、严格语法、重复键拒绝、节点计数/数值检查、读取后指纹、未认证兼容状态和实际输入契约核对。

自制颜色文件的许可由作者决定；工具 MIT 不自动让用户颜色作品成为 MIT。本版不导入/捆绑第三方 LUT，不把软件滑杆实现包装成真实胶片厂的色彩科学。

## 7. 模块、复用与测试

- `grade-core.js`：有限参数、LUT 生成、三线性参考、工程序列化；不访问相机、网络或文件系统。
- `render-worker.js`：处理导入的代理像素；不读磁盘、不管理快门。
- `ui.js`：文件选择、状态和预览；不包含 Sony API。
- `tools/build_studio_realtime.py`：从拆分源码构建单文件 HTML，并计算 CSP 哈希。
- 浏览器内建 JPEG/PNG 解码、画布颜色空间、缩放、Blob、Worker 为复用基础。没有引入另一套 RAW/ICC/编解码实现。
- 小型 LUT 数据适配和本项目调色参数是参考实现，非“成熟工业调色引擎”声明。正式 Camera 优先复用已审查的 LUT/JPEG 后端；不将浏览器JS塞进 Android API10。

标准检查已纳入两组 Node 测试；GitHub Actions 新增完整SHA固定的 Node设置动作。远端 CI 未运行。

```bash
python3 tools/build_studio_realtime.py
node --test studio/tests/look-core.test.js studio/grading/tests/grade-core.test.js
python3 tools/cv.py check
# 可选，需测试用 Playwright、Chromium：
python3 studio/grading/tests/browser_smoke.py
```

本轮 27 项新增调色测试通过；原原生配方 22 项测试与工程主机回归通过。浏览器10个场景检查通过：载入、真实像素变化、原图回看、撤销、LUT/工程/素材/PNG导出、输入确认门槛、快速多次输入不发布旧效果。

由于环境策略阻止 file 导航，浏览器测试通过 `set_content` 在内存中装入**实际生成的完整 HTML**，保留 CSP，不修改浏览器管理策略。验证包含真实文件选择、Blob图片解码、Worker与下载。它不覆盖 Mac 文件关联、file URL 权限差异、macOS27 Safari、屏幕校准或相机运行。不要把这里的20ms等某次测试数字当成用户电脑性能承诺。

## 8. 下一条真正的闭环

Studio 当前屏幕 → 导出 CUBE → Camera 在同一测试 JPEG 上应用 → 回到 Mac 核对像素与观感。只有这条链路实测通过，才可以对外说“颜色已经可以交给 A7R II 使用”。先验证单图，后接自动快门队列；不中断原本的反挤压与宽画幅开发。

## 来源

- [R01] MDN Canvas getImageData： https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/getImageData
- [R02] MDN getContextAttributes： https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/getContextAttributes
- [R03] OpenColorIO interpolation enums： https://opencolorio.readthedocs.io/en/v2.4.0/api/enums.html
- [R04] Recipe Lab FAQ： https://github.com/voxivoid/recipe-lab-sony-pmca/blob/main/docs/FAQ.md （本轮所读 blob 8276480d480650cf132d56a64025d6450b12ae88）
- [R05] OCIO IridasCube 实现： https://github.com/AcademySoftwareFoundation/OpenColorIO/blob/main/src/OpenColorIO/fileformats/FileFormatIridasCube.cpp （本轮所读 blob b6da8d7e81bfd30ce77a53fbf8417e7fb203ad07；研究格式，没有复制源文件）
- [R06] setup-node v4.4.0 固定提交：49933ea5288caeca8642d1e84afbd3f7d6820020。不是“最新版”或远端CI已通过声明。
