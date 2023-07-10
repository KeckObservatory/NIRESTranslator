from nires.shared.take_exposures import TakeExposures as te 
from nires.shared.set_detector_configuration import SetDetectorConfig as sdc
import unittest
from unittest.mock import Mock, patch, MagicMock
import ktl
import re
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
                'extra_wait': 1
            },
            'operation_mode': {
                'operation_mode': 'production'
            }
        }
    
    def test_take_an_exposure(self):

        args = {}
        # config detector for exposures
        args['det_exp_number'] = 1 # coadds
        args['det_exp_read_pairs'] = 1 # numreads
        args['det_samp_mode'] = 4 # sampmode
        args['det_exp_time'] = 3 # itime
        args['sv'] = 's'
        service = 'nsds'
        sdc.perform(args=args, logger=self.logger, cfg=self.cfg)

        # check that one file was created
        framenumBeginning = ktl.read(service, 'framenum')
        te._take_an_exposure(logger=self.logger, cfg=self.cfg)
        framenumAfter = ktl.read(service, 'framenum')
        self.assertEqual(framenumBeginning + 1, framenumAfter)
        filename= ktl.read(service, 'filename')
        self.assertTrue(os.path.exists(filename))

        # check that 3 files were created
        framenumBeginning = ktl.read(service, 'framenum')
        te._take_an_exposure(logger=self.logger, cfg=self.cfg, nFrames=3)
        framenumAfter = ktl.read(service, 'framenum')
        self.assertEqual(framenumBeginning + 3, framenumAfter)
        filename= ktl.read(service, 'filename')
        self.assertTrue(os.path.exists(filename))


        # Check that sv mode creates 2 files
        framenumBeginning = ktl.read(service, 'framenum')
        te._take_an_exposure(logger=self.logger, cfg=self.cfg, nFrames=1, sv='sv')
        framenumAfter = ktl.read(service, 'framenum')
        self.assertEqual(framenumBeginning + 2, framenumAfter)
        filename= ktl.read(service, 'filename')
        self.assertTrue(os.path.exists(filename))


if __name__ == "__main__":
    unittest.main()
