from nires.shared.take_exposures import TakeExposures as te 
from nires.shared.set_detector_configuration import SetDetectorConfig as sdc
import unittest
from unittest.mock import Mock, patch, MagicMock
import ktl
import re
import os


def logger_side_effect(msg):
    print(msg)

class TestTakeExposures(unittest.TestCase):

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
            }
        }

        args = {}
        # config detector for exposures
        args['nCoadds'] = 2 
        args['numreads'] = 1 
        args['readoutMode'] = 3 
        args['itime'] = 3 
        args['sv'] = 's'
        sdc.execute(args=args, logger=self.logger, cfg=self.cfg)
    
    def test_take_an_exposure(self):
        
        service = 'nsds'
        # check that one file was created
        framenumBeginning = int(ktl.read(service, 'framenum'))
        te._take_an_exposure(logger=self.logger, cfg=self.cfg)
        framenumAfter = int(ktl.read(service, 'framenum'))
        self.assertEqual(framenumBeginning + 1, framenumAfter)
        filename= ktl.read(service, 'filename')
        self.assertTrue(os.path.exists(filename))

        # check that 3 files were created
        framenumBeginning = int(ktl.read(service, 'framenum'))
        te._take_an_exposure(logger=self.logger, cfg=self.cfg, nFrames=3)
        framenumAfter = int(ktl.read(service, 'framenum'))
        self.assertEqual(framenumBeginning + 3, framenumAfter)
        filename= ktl.read(service, 'filename')
        self.assertTrue(os.path.exists(filename))


        # Check that sv mode creates 2 files
        framenumSBeginning = int(ktl.read(service, 'framenum'))
        framenumIBeginning = int(ktl.read('nids', 'framenum'))
        te._take_an_exposure(logger=self.logger, cfg=self.cfg, nFrames=1, sv='sv')
        framenumSAfter = int(ktl.read(service, 'framenum'))
        self.assertEqual(framenumSBeginning + 1, framenumSAfter)
        filenameS = ktl.read(service, 'filename')
        self.assertTrue(os.path.exists(filenameS))
        framenumIAfter = int(ktl.read('nids', 'framenum'))
        self.assertEqual(framenumIBeginning + 1, framenumIAfter)
        filenameI = ktl.read('nids', 'filename')
        self.assertTrue(os.path.exists(filenameI))

    def test_execute(self):
        nFrames = 1 
        sv = 's' 
        service = 'nsds'
        args = {
            'nFrames': nFrames,
            'sv': sv
        }

        framenumBeginning = int(ktl.read(service, 'framenum'))
        te.execute( args=args, logger=self.logger, cfg=self.cfg )
        framenumAfter = int(ktl.read(service, 'framenum'))

        self.assertEqual(framenumBeginning + 1, framenumAfter)
        filename = ktl.read(service, 'filename')
        self.assertTrue(os.path.exists(filename))

if __name__ == "__main__":
    unittest.main()
