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
