"""Passive USB evidence must fail when ioreg properties are missing."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools/macos'))
from observe_usb import IOR_COMMAND, summarize

class UsbObservationTests(unittest.TestCase):
    def device(self, **props):
        return dict({'IOObjectClass': 'IOUSBHostDevice', 'IORegistryEntryName': 'Camera',
                     'idVendor': 0x054c, 'idProduct': 1}, **props)

    def test_command_requests_properties(self):
        self.assertIn('-l', IOR_COMMAND)
        self.assertIn('-a', IOR_COMMAND)

    def test_missing_vendor_is_invalid_not_absent(self):
        for key in ('idVendor', 'idProduct'):
            node = self.device(); del node[key]
            with self.assertRaises(ValueError): summarize([node])

    def test_nested_sony_found_without_serials(self):
        node = self.device(**{'USB Serial Number': 'private-value'})
        result = summarize([{'IORegistryEntryChildren': [node]}])
        self.assertEqual(1, result['usb_device_count'])
        self.assertEqual(1, len(result['sony_devices']))
        self.assertNotIn('private-value', str(result))

    def test_non_sony_counts_as_control(self):
        result = summarize([self.device(idVendor=0x2109)])
        self.assertEqual(1, result['usb_device_count'])
        self.assertEqual([], result['sony_devices'])

    def test_android_vid_retained_without_claiming_sony_identity(self):
        result = summarize([self.device(idVendor=0x18d1, idProduct=0xd002,
                                      locationID=123)])
        self.assertEqual([], result['sony_devices'])
        self.assertEqual([{'idVendor': 0x18d1, 'idProduct': 0xd002,
                           'locationID': 123}], result['usb_identities'])

    def test_same_count_reenumeration_remains_observable(self):
        before = summarize([self.device(idVendor=0x054c, idProduct=1)])
        after = summarize([self.device(idVendor=0x18d1, idProduct=0xd002)])
        self.assertEqual(before['usb_device_count'], after['usb_device_count'])
        self.assertNotEqual(before['usb_identities'], after['usb_identities'])

    def test_other_vendor_metadata_not_retained(self):
        result = summarize([self.device(idVendor=0x1234,
                              **{'USB Serial Number': 'secret-serial',
                                 'USB Product Name': 'private-device',
                                 'IORegistryEntryName': 'private-name'})])
        for value in ('secret-serial', 'private-device', 'private-name'):
            self.assertNotIn(value, str(result))

    def test_empty_and_wrong_shape_rejected(self):
        for value in ([], {}, None, 'bad'):
            with self.assertRaises(ValueError): summarize(value)

    def test_macos_single_root_dictionary(self):
        self.assertEqual(1, len(summarize({'IOObjectClass': 'IORegistryEntry',
                                         'IORegistryEntryChildren': [self.device()]})['sony_devices']))

    def test_live_controller_with_no_devices(self):
        self.assertEqual(0, summarize([{'IOObjectClass': 'IORegistryEntry'}])['usb_device_count'])
