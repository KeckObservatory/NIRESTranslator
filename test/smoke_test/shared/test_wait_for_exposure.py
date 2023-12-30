from nires.shared.wait_for_exposure import WaitForExposure as wfe 
import unittest
from unittest.mock import Mock, patch, MagicMock
import pdb
try:
    import ktl
except ImportError:
    ktl = Mock()


def ktl_side_effects(service, value):
    if value == 'itime': return 4
    if value == 'sampmode': return 4
    if value == 'numreads': return 1
    if value == 'coadds': return 1
    if value == 'readtime': return 1
    if value == 'readtime': return 1
    if value == 'imagedone': return 0
    return 0

def logger_side_effect(msg):
    print(msg)

class TestWaitForExposure(unittest.TestCase):

    def setUp(self):
        ktl.read = Mock()
        ktl.read.side_effect = ktl_side_effects
        self.logger = MagicMock(side_effect=logger_side_effect)
        self.logger.info.side_effect = logger_side_effect
        self.logger.debug.side_effect = logger_side_effect
        self.cfg = {
            'ob_keys': {
                'n_read_padding': 1.5,
                'extra_wait': 1,
                'ktl_wait': False,
                'ktl_timeout': 2,
            },
            'operation_mode': {
                'operation_mode': 'operational'
            },
            'logger': {
                'ping_period': 1
            },
            'exposure': {
                'sleep_length': 1
            }
        }
    
    @patch('nires.shared.wait_for_exposure.ktl')
    def test_wait_for_exposure(self, mock_ktl):
        mock_ktl.read = Mock()
        mock_ktl.read.side_effect = ktl_side_effects
        wait = wfe.wait_for_exposure(sv='s', logger=self.logger, cfg=self.cfg)
        self.assertEqual(wait, 7.0)


if __name__ == "__main__":
    unittest.main()
