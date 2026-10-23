# 08｜来源与证据

核查日期：2026-09-19。技术事实来自原始项目/官方文档；选型、等级、流程和阈值为本项目判断。检索和读源码不是构建或实机验证。

## S01｜Sony-PMCA-RE
https://github.com/ma1co/Sony-PMCA-RE

安装、Android2.3.7说明；LICENSE.txt为MIT。此轮未锁安装实际提交。

## S02｜PMCADemo
https://github.com/ma1co/PMCADemo/tree/12f34e49d48a1d9496ea3c2792911867ea4c985b

CameraActivity/BaseActivity/Playback示例；MIT。

## S03｜OpenMemories-Framework
https://github.com/ma1co/OpenMemories-Framework/tree/f8df3504d8684433a331ee869e64f67cc8be9730

DisplayManager、MediaManager、Sony存根；许可MIT；声明不等于设备通过。

## S04｜Recipe Lab
https://github.com/voxivoid/recipe-lab-sony-pmca/tree/d4c64239ddb775e11b9343b54bc71616dd62a7a5

Recipes/Params/MainActivity与DEVELOPMENT；MIT。只复用明确范围。

## S05｜CameraSequence声明
https://github.com/ma1co/OpenMemories-Framework/blob/f8df3504d8684433a331ee869e64f67cc8be9730/stubs/src/main/jasmin/com/sony/scalar/hardware/CameraSequence.j

帧句柄、预览插件、保存；不是成熟desqueeze实现。

## S06｜JPEG.CAM README与许可证
https://github.com/upsetstomach56/JPEG.CAM-2.0/tree/20a30c82a058560c64002e205f2152104c3ea8ba

early beta/proof of concept；根LICENSE为继承MIT，资产需另核。

## S07｜CinemaMatteView
https://github.com/upsetstomach56/JPEG.CAM-2.0/blob/20a30c82a058560c64002e205f2152104c3ea8ba/app/src/main/java/com/github/ma1co/pmcademo/app/CinemaMatteView.java

Canvas、2.71f、3:2假设。

## S08｜JPEG.CAM native-lib.cpp
https://github.com/upsetstomach56/JPEG.CAM-2.0/blob/20a30c82a058560c64002e205f2152104c3ea8ba/app/src/main/cpp/native-lib.cpp

读取前230行：分行/分块、近似裁切、全部APP/COM复制、输出wb。

## S09｜libjpeg-turbo官方
https://github.com/libjpeg-turbo/libjpeg-turbo

成熟JPEG codec候选；未选定PMCA构建提交。

## S10｜libjpeg-turbo许可
https://libjpeg-turbo.org/About/License

多许可证组件，不能改标成MIT。

## S11｜libyuv官方
https://chromium.googlesource.com/libyuv/libyuv

缩放/转换/旋转组件；没有提供Sony取帧能力；具体提交许可待导入审核。

## S12｜DeviceFarmer旧Android JPEG构建
https://github.com/DeviceFarmer/android-libjpeg-turbo

README有旧NDK/armeabi参考，无JNI；不是默认生产codec版本。

## S13｜Android ExifInterface
https://developer.android.com/reference/android/media/ExifInterface

核对API10时可用子集；当前文档含后续API，不可全用。

## S14｜Android SharedPreferences
https://developer.android.com/reference/android/content/SharedPreferences

平台偏好组件；注意具体方法API级别。

## S15｜Android SQLiteOpenHelper
https://developer.android.com/reference/android/database/sqlite/SQLiteOpenHelper

平台数据库迁移入口；当前尚未完成job repository。

## S16｜Android D8
https://developer.android.com/tools/d8

独立DEX工具、min-api、lib与desugaring区别。

## S17｜Android apksigner
https://developer.android.com/tools/apksigner

签名验证与zipalign必须在前。

## S18｜GitHub workflow security
https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions

固定完整Actions提交，最小权限与不可信代码风险。

## S19｜Android TextureView
https://developer.android.com/reference/android/view/TextureView

类/API14，不能当API10默认方案。

## S20｜NDK revision history
https://developer.android.com/ndk/downloads/revision_history

旧ABI/平台支持随版本变化，native需单独鉴定。

## 不可变锚点
核心四个仓库提交见third_party/upstreams.lock.json。GitHub Actions由连接器实际取回：checkout v4.2.2 = 11bd71901bbe5b1630ceea73d27597364c9af683；setup-java v4.7.1 = c5195efecf7bdfc987ee8bae7a71cb8b11521c00。它们是固定的研究基线，不声称是当前最新版本。

本轮容器不能联网获取SDK/完整上游仓库；联网读取通过浏览器/连接器完成。不存在完整第三方构建复现、许可证资产全量审计或用户机身测试。上游范围和本工程来源保留是两层不同的证据。
