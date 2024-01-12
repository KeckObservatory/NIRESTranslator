from nires.spectrograph.dither import Dither
import unittest
import pdb
from astropy.coordinates import SkyCoord
from unittest.mock import Mock, patch, MagicMock
try:
    import ktl
except ImportError:
    ktl = Mock()

    
def ktl_side_effects(service, value):
    if value == 'ra': return '04:16:00.00 h'
    if value == 'dec': return '+45:00:00.0 deg' 
    return 0

def logger_side_effect(msg):
    print(msg)

class TestDither(unittest.TestCase):

    def setUp(self):
        self.logger = MagicMock(side_effect=logger_side_effect)
        self.logger.info.side_effect = logger_side_effect
        self.logger.debug.side_effect = logger_side_effect
        self.logger.warning.side_effect = logger_side_effect
        self.logger.error.side_effect = logger_side_effect
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
            'dither_delta': { 'dither_delta': -1 },
            'slit_length': { 'slit_length': -1 },
            'logger': {
                'ping_period': 1,
            },
            'exposure': {
                'sleep_length': 1,
            }
        }

    @patch('nires.spectrograph.dither.ktl')
    def test_ra_dec_convert(self, mock_ktl):
        mock_ktl.read.side_effect = ktl_side_effects
        raStr = mock_ktl.read('dcs2', 'ra')
        decStr = mock_ktl.read('dcs2', 'dec')
        coords = SkyCoord(raStr, decStr)
        starting_pos = { 'ra': coords.ra.degree, 'dec': coords.dec.degree}
    
    @patch('nires.spectrograph.dither.MarkBase')
    @patch('nires.spectrograph.dither.ktl')
    def test_pre_condition(self, mock_ktl, mock_MarkBase):
        def mb_execute_side_effect(args):
            return {'ra': 1, 'dec': 1}
        mock_ktl.read = Mock() 
        mock_ktl.read.side_effect = ktl_side_effects
        mock_MarkBase.execute = mb_execute_side_effect
        args = {'sv': 's', 'pattern': 'ABBA', 'offset': 1}
        outArgs = Dither.pre_condition(args, self.logger, self.cfg)
        self.assertTrue( 'starting_pos' in outArgs.keys() )

    @patch('nires.spectrograph.dither.MarkBase')
    @patch('nires.spectrograph.dither.ktl')
    def test_post_condition(self, mock_ktl, mock_MarkBase):
        def mb_execute_side_effect(args):
            return {'ra': 1, 'dec': 1}
        mock_ktl.read = Mock()
        mock_ktl.read.side_effect = ktl_side_effects
        mock_MarkBase.execute = mb_execute_side_effect
        pc_args = {'starting_pos': {'ra': 1, 'dec': 1}, 'sv': 's', 'pattern': 'ABBA', 'offset': 1}
        outArgs = Dither.post_condition(pc_args, self.logger, self.cfg)
        self.assertTrue( 'starting_pos' in outArgs.keys() )

    @patch('nires.shared.take_exposures.TakeExposures')
    @patch('nires.spectrograph.dither.SlitMove')
    @patch('nires.NIRESTranslatorFunction.ktl')
    def test_execute_dither(self, mock_ktl, mock_SlitMove, mock_TakeExposures):
        def sm_execute_side_effect(args):
            return 
        def te_execute_side_effect(args):
            print('take exposure execute!')
        mock_ktl.read = Mock()
        mock_ktl.read.side_effect = ktl_side_effects
        mock_SlitMove.execute = sm_execute_side_effect
        mock_TakeExposures.execute = te_execute_side_effect
        args = { 'offset': 1, 'pattern': 'ABBA', 'sv': 's'}
        Dither.execute_dither(args, self.logger, self.cfg)


if __name__ == "__main__":
    unittest.main()
