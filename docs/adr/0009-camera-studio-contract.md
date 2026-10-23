# ADR 0009 — Camera 与 Studio 共用声明式 Look 契约

状态：采纳，协议草稿阶段。日期 2026-09-19。

Camera=旧Android摄影端；Studio=Mac本地颜色创作端。共享配方定义和测试样例，不共享UI或整套执行器。

Sony原生参数、Sony PP与software-lut是互斥颜色后端。任意3D LUT不能无损转为有限Sony参数；PP菜单能力不等于自动写入接口已经验证。

当前交付本地原生配方编写台：可导出 .CVL 和手工设置单；无伪造Sony预览、无相机导入器。真实的视觉反馈优先通过机内样片与未来受控连接实现。

软件LUT工作区将复用成熟的LUT解析/色彩变换库，不新写通用色彩科学。每个LUT必须声明输入/输出色彩空间、传递函数、范围、cube尺寸、上游源及校验。颗粒/光晕/锐化等空间操作不塞进3D LUT。

.CVL作者状态永远unverified；机型/固件/设备测试证据归独立CapabilityRegistry。没有安装器、shell或Backup槽地址可以放进配方。
