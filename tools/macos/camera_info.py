#!/usr/bin/env python3
"""A7R II model query using one upstream MTP session, without updater commands.

Invoke through camera_info.sh, which verifies the pinned upstream checkout.
No installation, firmware version inference, driver patches or permission bypass.
"""
import json
from pathlib import Path
import sys


def query(context, device_factory, is_supported, camera_factory):
    devices = list(context.listDevices(0x054c))
    if len(devices) != 1:
        raise RuntimeError('需要恰好一台 Sony MTP 相机；当前数量：%d' % len(devices))
    # Construct the extended wrapper once. Upstream listDevices constructs a
    # basic wrapper then another extended wrapper, repeating backend.reset().
    device = device_factory(context.openDevice(devices[0]))
    try:
        info = device.getDeviceInfo()
        if info.model != 'ILCE-7RM2' or not is_supported(info):
            raise RuntimeError('型号或协议不在本查询入口的白名单内')
        extra = camera_factory(device).getCameraInfo()
        return {'model': extra.modelName, 'model_code': extra.modelCode,
                'mode': 'MTP', 'firmware': 'not_queried'}
    finally:
        device.closeSession()


def main():
    if len(sys.argv) != 1:
        raise RuntimeError('只读查询不接受额外参数')
    root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(root / '.local/connection/Sony-PMCA-RE'))
    from pmca.usb.driver.generic.libusb import MtpContext
    from pmca.usb.sony import SonyMtpExtCmdDevice, SonyExtCmdCamera, isSonyMtpCamera
    with MtpContext() as context:
        print(json.dumps(query(context, SonyMtpExtCmdDevice, isSonyMtpCamera,
                               SonyExtCmdCamera), ensure_ascii=False))


if __name__ == '__main__':
    main()
