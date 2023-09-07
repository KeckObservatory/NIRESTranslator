from nires.shared.take_exposures import TakeExposures as te 
from nires.spectrograph.dither import Dither
import unittest
from unittest.mock import Mock, patch, MagicMock
try:
    import ktl
except ImportError:
    ktl = Mock()

def logger_side_effect(msg):
    print(msg)

class TestDither(unittest.TestCase):

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
            }, 
            'dither_delta': { 'dither_delta': -1 },
            'slit_length': { 'slit_length': -1 }
        }
    
    @patch('nires.spectrograph.dither.MarkBase')
    def test_pre_condition(self, mock_MarkBase):
        def mb_execute_side_effect(args):
            return {'ra': 1, 'dec': 1}
        mock_MarkBase.execute = mb_execute_side_effect
        args = {'sv': 's', 'pattern': 'ABBA', 'offset': 1}
        outArgs = Dither.pre_condition(args, self.logger, self.cfg)
        self.assertTrue( 'starting_pos' in outArgs.keys() )

    @patch('nires.spectrograph.dither.MarkBase')
    def test_post_condition(self, mock_MarkBase):
        def mb_execute_side_effect(args):
            return {'ra': 1, 'dec': 1}
        mock_MarkBase.execute = mb_execute_side_effect
        pc_args = {'starting_pos': {'ra': 1, 'dec': 1}, 'sv': 's', 'pattern': 'ABBA', 'offset': 1}
        outArgs = Dither.post_condition(pc_args, self.logger, self.cfg)
        self.assertTrue( 'starting_pos' in outArgs.keys() )

    @patch('nires.shared.take_exposures.TakeExposures')
    @patch('nires.spectrograph.dither.SlitMove')
    def test_execute_dither(self, mock_SlitMove, mock_TakeExposures):
        def sm_execute_side_effect(args):
            return 
        def te_execute_side_effect(args):
            print('take exposure execute!')
        mock_SlitMove.execute = sm_execute_side_effect
        mock_TakeExposures.execute = te_execute_side_effect
        args = { 'offset': 1, 'pattern': 'ABBA', 'sv': 's'}
        Dither.execute_dither(args, self.logger, self.cfg)



if __name__ == "__main__":
    unittest.main()
