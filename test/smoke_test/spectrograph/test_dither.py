
from nires.spectrograph.dither import Dither
import unittest
from unittest.mock import Mock, patch, MagicMock
try:
    import ktl
except ImportError:
    ktl = Mock()

def logger_side_effect(msg):
    print(msg)

class TestTakeExposures(unittest.TestCase):

    def setUp(self):
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
            }
        }
    
    @patch('nires.spectrograph.dither.MarkBase')
    def test_pre_condition(self, mock_ktl):
        args = {'sv': 's', 'pattern': 'ABBA', 'offset': 1}
        Dither.pre_condition(args, self.logger, self.cfg)


if __name__ == "__main__":
    unittest.main()
