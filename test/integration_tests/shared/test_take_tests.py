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
                'extra_wait': 1,
                'ktl_wait': False,
                'ktl_timeout': 2,
            },
            'operation_mode': {
                'operation_mode': 'operational'
            }
        }
    
    def test_execute(self):

        args = {}
        # config detector for exposures
        args['nCoadd'] = 1 
        args['numreads'] = 1 
        args['readoutMode'] = 4 
        args['itime'] = 3 
        args['nSamp'] = None 
        args['sv'] = 'v'
        service = 'nids'
        sdc.perform(args=args, logger=self.logger, cfg=self.cfg)

        # check that file is not created
        framenumBeginning = int(ktl.read('nids', 'framenum'))

        args = {}
        args['nFrames'] = 1
        args['sv'] = 'v'
        tt.execute(args, logger=self.logger, cfg=self.cfg)
        framenumAfter = int(ktl.read('nids', 'framenum'))
        self.assertEqual(framenumBeginning, framenumAfter)


if __name__ == "__main__":
    unittest.main()
