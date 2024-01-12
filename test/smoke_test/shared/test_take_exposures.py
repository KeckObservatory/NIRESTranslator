from nires.shared.take_exposures import TakeExposures as te 
import unittest
from unittest.mock import Mock, patch, MagicMock
import pdb
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
    if value == 'framenum': return 1
    return 0

def logger_side_effect(msg):
    print(msg)

class TestTakeExposures(unittest.TestCase):

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
                'operation_mode': 'test'
            },
            'logger': {
                'ping_period': 1,
            },
            'exposure': {
                'sleep_length': 1,
            }
        }
    
    @patch('nires.shared.take_exposures.ktl')
    @patch('nires.shared.wait_for_exposure.ktl')
    @patch('nires.NIRESTranslatorFunction.ktl')
    def test_take_an_exposure(self, mock_ktl, mk_ktl, m_ktl):
        m_ktl.read = Mock()
        m_ktl.read.side_effect = ktl_side_effects
        mk_ktl.read = Mock()
        mk_ktl.read.side_effect = ktl_side_effects
        mock_ktl.read = Mock()
        mock_ktl.read.side_effect = ktl_side_effects
        te._take_an_exposure(logger=self.logger, cfg=self.cfg)
        te._take_an_exposure(logger=self.logger, cfg=self.cfg, nFrames=3)
        te._take_an_exposure(logger=self.logger, cfg=self.cfg, nFrames=1, sv='sv')


if __name__ == "__main__":
    unittest.main()
