#!/usr/bin/env python3
"""Read macOS IORegistry snapshots only; never open a camera USB interface."""
import argparse
import datetime
import json
import plistlib
import subprocess
import time

IOR_COMMAND = ['/usr/sbin/ioreg', '-a', '-l', '-p', 'IOUSB']


def summarize(nodes):
    if isinstance(nodes, dict) and 'IOObjectClass' in nodes:
        nodes = [nodes]
    if not isinstance(nodes, list) or not nodes:
        raise ValueError('IORegistry root missing or invalid; device absence cannot be inferred')
    count = 0
    sony = []
    identities = []

    def walk(node):
        nonlocal count
        if not isinstance(node, dict):
            raise ValueError('Malformed IORegistry node')
        if node.get('IOObjectClass') in ('IOUSBHostDevice', 'IOUSBDevice') or 'idVendor' in node:
            if not all(isinstance(node.get(k), int) for k in ('idVendor', 'idProduct')):
                raise ValueError('USB properties missing; invalid observation, not no-device')
            count += 1
            # Record every VID/PID: diagnostic modes need not use Sony's VID.
            # Numeric location distinguishes ports without retaining names/serials.
            identity = {k: node[k] for k in ('idVendor', 'idProduct')}
            if isinstance(node.get('locationID'), int):
                identity['locationID'] = node['locationID']
            identities.append(identity)
            if node['idVendor'] == 0x054c:
                # No serial numbers or data about unrelated devices in logs.
                sony.append({k: node.get(k) for k in
                             ('IORegistryEntryName', 'USB Product Name', 'idVendor', 'idProduct')})
        for child in node.get('IORegistryEntryChildren', []):
            walk(child)

    for node in nodes:
        walk(node)
    return {'usb_device_count': count, 'sony_devices': sony,
            'usb_identities': identities}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds', type=int, choices=range(1, 31), default=10)
    args = parser.parse_args()
    end = time.monotonic() + args.seconds
    while True:
        result = subprocess.run(IOR_COMMAND, capture_output=True, check=True, timeout=5)
        row = summarize(plistlib.loads(result.stdout))
        row['time'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        print(json.dumps(row, ensure_ascii=False), flush=True)
        if time.monotonic() >= end:
            break
        time.sleep(min(.25, max(0, end - time.monotonic())))


if __name__ == '__main__':
    main()
