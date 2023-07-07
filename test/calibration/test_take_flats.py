from nires.calibration.take_flats import TakeFlats as tf 
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

class TestTakeFlats(unittest.TestCase):

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
    
    @patch('nires.calibration.take_flats.ktl')
    @patch('nires.calibration.take_flats.te')
    @patch('nires.calibration.take_flats.tdl')
    def test_toggle_dome_lamps(self, mock_tdl, mock_te, mock_ktl):
        mock_tdl.execute = Mock()
        mock_te.execute = Mock()
        mock_ktl.read = Mock()
        mock_ktl.read.side_effect = ktl_side_effects

        tf._take_flats(logger=self.logger, cfg=self.cfg, nFrames=1, manual=False)
        tf._take_flats(logger=self.logger, cfg=self.cfg, nFrames=3, manual=True)

if __name__ == "__main__":
    unittest.main()
