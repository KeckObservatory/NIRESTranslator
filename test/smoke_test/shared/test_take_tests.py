from nires.shared.take_tests import TakeTests as tt 
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

class TestTakeTests(unittest.TestCase):

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
            }
        }
    
    @patch('nires.shared.take_tests.ktl')
    def test_take_tests(self, mock_ktl):
        mock_ktl.read = Mock()
        mock_ktl.read.side_effect = ktl_side_effects
        tt._take_tests(nFrames=1, sv='s', logger=self.logger, cfg=self.cfg)
        tt._take_tests(nFrames=5, sv='s', logger=self.logger, cfg=self.cfg)
        tt._take_tests(nFrames=None, sv='s', logger=self.logger, cfg=self.cfg)


if __name__ == "__main__":
    unittest.main()
