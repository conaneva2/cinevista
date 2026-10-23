import sys
import unittest
import json
import tempfile
from unittest.mock import Mock, patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from virtual_camera import Console, boot_status, safe_asset


class VirtualCameraContracts(unittest.TestCase):
    def test_echoed_command_is_not_success(self):
        s = boot_status('/ # echo DMM_INSMOD_STATUS=0\n', True)
        self.assertFalse(s['dmm'])

    def test_driver_success_does_not_claim_android_or_apk(self):
        s = boot_status('ULOGIO_INSMOD_STATUS=0\nDMM_INSMOD_STATUS=0\n', False)
        self.assertTrue(s['ulogio'])
        self.assertTrue(s['dmm'])
        self.assertFalse(s['android'])
        self.assertFalse(s['apk'])

    def test_failure_survives_normal_host_exit(self):
        s = boot_status('DMM_INSMOD_STATUS=0\nEntering exception monitor.\n', False)
        self.assertEqual(s['state'], 'stopped_at_error')

    def test_assets_cannot_expose_firmware_or_workspace(self):
        self.assertEqual(safe_asset('/'), 'index.html')
        for path in ('/../config.json', '/.local/firmware', '/%2e%2e/a', '/server.py'):
            self.assertIsNone(safe_asset(path))

    def console_fixture(self, root):
        (root / 'config').mkdir()
        (root / 'config/virtual-camera.lock.json').write_text(json.dumps({
            'profile': {}, 'inputs': {'input.bin': '0' * 64}}))
        (root / '.local').mkdir()
        (root / '.local/CAMERA_WRITE_HOLD').touch()
        return Console(root)

    def test_input_drift_never_launches_a_process(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            c = self.console_fixture(root)
            (root / 'input.bin').write_bytes(b'changed')
            with patch('virtual_camera.subprocess.Popen') as launch:
                with self.assertRaises(ValueError):
                    c.start()
                launch.assert_not_called()

    def test_manual_stop_preserves_an_existing_firmware_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            c = self.console_fixture(root)
            c.process = Mock()
            c.process.poll.return_value = -2
            c.user_stopped = True
            self.assertEqual(c.status()['state'], 'stopped_by_user')
            c.output = root
            (root / 'serial.log').write_text('Entering exception monitor.\n')
            self.assertEqual(c.status()['state'], 'stopped_at_error')

    def test_clean_host_exit_without_guest_completion_is_incomplete(self):
        with tempfile.TemporaryDirectory() as directory:
            c = self.console_fixture(Path(directory))
            c.process = Mock()
            c.process.poll.return_value = 0
            self.assertEqual(c.status()['state'], 'probe_incomplete')


if __name__ == '__main__':
    unittest.main()
