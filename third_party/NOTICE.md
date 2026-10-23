# Third-party notices and import status

CineVista original changes use the root MIT license. This does not relicense third-party software or assets.

- PMCADemo lifecycle/key routing informed the existing adaptation. Copyright (c) 2015 ma1co; full MIT in PMCADemo-MIT.txt.
- OpenMemories-Framework signatures were reviewed at f8df3504d8684433a331ee869e64f67cc8be9730. Copyright (c) 2016 ma1co; full MIT in OpenMemories-MIT.txt. No Sony implementation binary/stub classes are shipped.
- Recipe Lab selected for future data/runtime-parameter integration: copyright (c) 2026 André Domingues; RecipeLab-MIT.txt. No recipe code has been imported into this version.
- JPEG.CAM 2.0 root license is MIT, copyright (c) 2015 ma1co inherited from its base. Root license alone is not an audit of all later files, fonts, LUTs, textures, libjpeg or stb components. No JPEG.CAM implementation or assets are bundled here.

No font files, LUT assets, firmware, SDK distributions, private camera photos or private signing keys are included. The libjpeg-turbo/libyuv candidate libraries are not yet bundled. The registry records candidacy separately from inclusion.

Before importing: preserve upstream notices; document exact copied paths and modifications; hash the actual bytes; obtain component/asset authorization where needed. Do not label a rebuilt binary with a test record belonging to another SHA.

2026-09-19 local build: official Google SDK and Temurin distributions are present only under ignored .local for development, along with the private debug key. They are not part of the MIT source/redistribution set. See TOOLCHAIN_DECISION_20260919.md; never package .local or private device reports. No additional upstream application code was imported.

## QEMU source patch exception

The root MIT license does not cover emulator/qemu patches. Patch 0001 follows LGPL-2.1-or-later; 0002–0004 follow GPL-2.0-or-later. Full upstream license texts, original provenance and modification notices are in emulator/qemu/README.md. No QEMU binary or Sony firmware is distributed.
