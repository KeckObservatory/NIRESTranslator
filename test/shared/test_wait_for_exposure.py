from nires.shared.wait_for_exposure import WaitForExposure as wfe 
import unittest
from unittest.mock import Mock, patch, MagicMock
try:
    import ktl
except ImportError:
    ktl = Mock()


def ktl_side_effects(service, value):
    if value == 'itime': return 1
    if value == 'sampmode': return 4
    if value == 'numreads': return 1
    if value == 'coadds': return 1
    if value == 'readtime': return 1
    if value == 'readtime': return 1
    if value == 'imagedone': return 1
    return 0

def logger_side_effect(msg):
    print(msg)

def cfg_side_effect(service, value):
    if value == 'operation_mode': return 'testing'
    if value == 'n_read_padding': return 1 
    if value == 'extra_wait': return 1

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
                'extra_wait': 1
            }
        }
    
    @patch('nires.shared.wait_for_exposure.ktl')
    def test_wait_for_exposure(self, mock_ktl):
        mock_ktl.read = Mock()
        mock_ktl.read.side_effect = ktl_side_effects
        wait = wfe.wait_for_exposure(sv='s', logger=self.logger, cfg=self.cfg)
        self.assertEqual(wait, 2.5)


if __name__ == "__main__":
    unittest.main()
