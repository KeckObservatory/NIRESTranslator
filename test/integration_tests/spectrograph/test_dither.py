from nires.spectrograph.dither import Dither
import unittest
from unittest.mock import Mock, patch, MagicMock
from nires.shared.set_detector_configuration import SetDetectorConfig as sdc
import time
import os
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
            'dither_delta': { 'dither_delta': 1 },
            'slit_length': { 'slit_length': 10 },
            'logger': {
                'subsystem':"NIRES",
                'configLoc': None,
                'ping_period':120
            },
            'exposure': {
                'sleep_length':1
            }
        }

        args = {}
        # config detector for exposures
        args['nCoadds'] = 2 
        args['numreads'] = 2 
        args['readoutMode'] = 3 
        args['itime'] = 3 
        args['nSamp'] = 1 
        args['sv'] = 's'
        args['obsType'] = 'object'
        sdc.execute(args=args, logger=self.logger, cfg=self.cfg)
    
    def test_execute(self):
        service = 'nsds'
        nFrames = 4 # ABBA creates 4 frames
        args = {'sv': 's', 'pattern': 'ABBA', 'offset': 1}

        framenumBeginning = int(ktl.read(service, 'framenum'))
        Dither.execute(args, self.logger, self.cfg)
        time.sleep(1)
        framenumAfter = int(ktl.read(service, 'framenum'))

        self.assertEqual(framenumBeginning + nFrames, framenumAfter)



if __name__ == "__main__":
    unittest.main()
