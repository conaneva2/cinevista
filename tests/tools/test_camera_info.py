"""No USB access: connection lifecycle and fail-closed target checks."""
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools' / 'macos'))
from camera_info import query

class CameraInfoTests(unittest.TestCase):
    def setUp(self):
        self.ctx = Mock()
        self.ctx.listDevices.return_value = [object()]
        self.dev = Mock()
        self.dev.getDeviceInfo.return_value = SimpleNamespace(model='ILCE-7RM2')
        self.factory = Mock(return_value=self.dev)
        self.camera = Mock()
        self.camera.return_value.getCameraInfo.return_value = SimpleNamespace(modelName='ILCE-7RM2', modelCode='0032828070')

    def call(self, supported=True):
        return query(self.ctx, self.factory, lambda _: supported, self.camera)

    def test_single_wrapper_and_closed_session(self):
        self.assertEqual('ILCE-7RM2', self.call()['model'])
        self.factory.assert_called_once()
        self.dev.closeSession.assert_called_once()
        self.assertNotIn('serial', self.call())

    def test_zero_or_multiple_devices_never_opened(self):
        for devices in ([], [object(), object()]):
            self.ctx.listDevices.return_value = devices
            with self.assertRaises(RuntimeError): self.call()
        self.factory.assert_not_called()

    def test_wrong_model_never_queries_extensions(self):
        self.dev.getDeviceInfo.return_value.model = 'OTHER'
        with self.assertRaises(RuntimeError): self.call()
        self.camera.assert_not_called()
        self.dev.closeSession.assert_called_once()

    def test_unsupported_protocol_never_queries_extensions(self):
        with self.assertRaises(RuntimeError): self.call(False)
        self.camera.assert_not_called()

    def test_permission_error_is_not_swallowed_or_retried(self):
        self.factory.side_effect = PermissionError('access denied')
        with self.assertRaises(PermissionError): self.call()
        self.factory.assert_called_once()

    def test_query_failure_closes_session(self):
        self.camera.return_value.getCameraInfo.side_effect = RuntimeError('protocol failure')
        with self.assertRaises(RuntimeError): self.call()
        self.dev.closeSession.assert_called_once()
