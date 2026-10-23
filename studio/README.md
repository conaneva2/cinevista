# 幕野 Studio · 实时调色 0.2 Alpha

**入口：双击 `CineVista_Studio_Realtime_0.2.html` 或 `index.html`。**单文件、无服务器、无CDN、无需Node运行；Mac Safari/Chrome待用户设备测试。

导入本地 JPEG/PNG → 移动滑杆，画面自动更新 → 原图/分屏对照 → 多样张检查 → 保存 CVG、导出 CUBE 或 CVP 素材包草稿。

已实现：真正的软件像素调色、曲线/分区偏色/六色调整、17³或33³ LUT、撤销/重做与预览PNG。预览采样的就是导出表，不是另一套CSS效果。原生配方编写台仍在 `native.html` 和 `CineVista_Studio_0.1.html`。

**尚未实现：Camera 素材包导入与执行；Sony 原生PP精确仿真；RAW/Log/HDR；原尺寸照片导出；相机性能/兼容认证。**不要把原型叫A7RII已可用功能。

输入基线必须一致。当前浏览器请求 sRGB 像素；不保证原文件为中性影像。用将来相机套LUT之前的同基线JPEG调色；相机素材包要求填写基线并确认。抬黑、冷暖、数字亮度是软件创作参数，不是Sony菜单、光源测量或RAW曝光恢复。

测试：`node --test studio/tests/look-core.test.js studio/grading/tests/grade-core.test.js`。
构建：`python3 tools/build_studio_realtime.py`。

本轮实际 Chromium 内存页通过10项交互和下载检查，保留原CSP。真实file导航被环境策略拦截，未修改策略；尚未在macOS27/Safari或相机验证。

工具代码MIT。用户自创颜色不自动更改为MIT；未捆绑Recipe Lab或第三方LUT。
