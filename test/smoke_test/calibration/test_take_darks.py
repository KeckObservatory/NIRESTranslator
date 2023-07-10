from nires.calibration.take_darks import TakeDarks as td
import unittest
from unittest.mock import Mock, patch, MagicMock
try:
    import ktl
except ImportError:
    ktl = Mock()


def ktl_side_effects(service, value):
    if value == 'flimagin': return 'on'
    if value == 'flspectr': return 'off' 
    return 0

def logger_side_effect(msg):
    print(msg)

class TestTakeDarks(unittest.TestCase):

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
    
    @patch('nires.calibration.take_darks.ktl')
    @patch('nires.calibration.take_darks.te')
    @patch('nires.calibration.take_darks.tdl')
    def test_take_darks(self, mock_toggle_dome_lamp, mock_take_exposures, mock_ktl):
        mock_ktl.read = Mock()
        mock_take_exposures.execute = Mock()
        mock_toggle_dome_lamp.execute = Mock()
        td._take_darks(1, logger=self.logger, cfg=self.cfg)



if __name__ == "__main__":
    unittest.main()
