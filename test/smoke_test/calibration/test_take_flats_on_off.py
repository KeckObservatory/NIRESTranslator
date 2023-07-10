from nires.calibration.take_flats_on_off import TakeFlatsOnOff as tfof 
import unittest
from unittest.mock import Mock, patch, MagicMock
try:
    import ktl
except ImportError:
    ktl = Mock()


def ktl_side_effects(service, value):
    if value == 'filename': return 'test_file.fits' 
    return 0

def logger_side_effect(msg):
    print(msg)

class TestTakeFlatsOnOff(unittest.TestCase):

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
            },
            'operation_mode': {
                'operation_mode': 'test'
            }
        }
    
    @patch('nires.calibration.take_flats_on_off.ktl')
    @patch('nires.calibration.take_flats_on_off.te')
    @patch('nires.calibration.take_flats_on_off.tdl')
    def test_take_flats_on_off(self, mock_tdl, mock_te, mock_ktl):
        mock_tdl.execute = Mock()
        mock_te.execute = Mock()
        mock_ktl.read = Mock()
        mock_ktl.read.side_effect = ktl_side_effects
        tfof._take_flats_on_off(logger=self.logger, cfg=self.cfg, nFrames=2)
        

if __name__ == "__main__":
    unittest.main()
