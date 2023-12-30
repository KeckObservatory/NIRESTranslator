from nires.calibration.take_arcs import TakeArcs as ta 
import unittest
from unittest.mock import Mock, patch, MagicMock
try:
    import ktl
except ImportError:
    ktl = Mock()


def ktl_side_effects(service, value):
    if value == 'flimagin': return 'on'
    if value == 'flspectr': return 'off' 
    if value == 'filename': return 'test_file.fits' 
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

class TestTakeArcs(unittest.TestCase):

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
            },
            'logger': {
                'ping_period': 1,
            },
            'exposure': {
                'sleep_length': 1,
            }
        }
    
    @patch('nires.calibration.take_arcs.ktl')
    @patch('nires.shared.wait_for_exposure.ktl')
    @patch('nires.shared.take_exposures.ktl')
    @patch('nires.NIRESTranslatorFunction.ktl')
    def test_take_arcs(self, mock_ktl, mk_ktl, m_ktl, _ktl):
        _ktl.read = Mock()
        _ktl.read.side_effect = ktl_side_effects
        m_ktl.read = Mock()
        m_ktl.read.side_effect = ktl_side_effects
        mk_ktl.read = Mock()
        mk_ktl.read.side_effect = ktl_side_effects
        mock_ktl.read = Mock()
        mock_ktl.read.side_effect = ktl_side_effects
        ktl.read = Mock()
        ktl.read.side_effect = ktl_side_effects
        ta._take_arcs(logger=self.logger, cfg=self.cfg, nFrames=1)
        ta._take_arcs(logger=self.logger, cfg=self.cfg, nFrames=1)



if __name__ == "__main__":
    unittest.main()
