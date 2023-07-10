from nires.shared.take_tests import TakeTests as tt 
from nires.shared.set_detector_configuration import SetDetectorConfig as sdc
import unittest
from unittest.mock import Mock, patch, MagicMock
import ktl
import os


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
                'extra_wait': 1
            },
            'operation_mode': {
                'operation_mode': 'production'
            }
        }
    
    def test_perform(self):

        args = {}
        args['nFrames'] = 1
        args['sv'] = 'v'
        args = {}
        # config detector for exposures
        args['det_exp_number'] = 1 # coadds
        args['det_exp_read_pairs'] = 1 # numreads
        args['det_samp_mode'] = 4 # sampmode
        args['det_exp_time'] = 3 # itime
        args['sv'] = 's'
        service = 'nsds'
        sdc.perform(args=args, logger=self.logger, cfg=self.cfg)

        # check that file is not created
        framenumBeginning = ktl.read('nids', 'framenum')
        tt.perform(args, logger=self.logger, cfg=self.cfg)
        framenumAfter = ktl.read('nids', 'framenum')
        self.assertEqual(framenumBeginning, framenumAfter)
        filename= ktl.read('nids', 'filename')
        self.assertFalse(os.path.exists(filename), 'File should not have been created')

if __name__ == "__main__":
    unittest.main()
