from nires.calibration.take_flats import TakeFlats as tf 
import unittest
from unittest.mock import Mock, patch, MagicMock
import ktl
import os
import pdb

def logger_side_effect(msg):
    print(msg)

class TestTakeFlats(unittest.TestCase):

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
                'operation_mode': 'test'
            },
            'logger': {
                'subsystem':"NIRES",
                'configLoc': None,
                'ping_period':120
            },
            'exposure': {
                'sleep_length':1
            }
        }
    
    def test_take_flats(self):
        breakpoint()
        service = 'nsds'
        ktl.write(service, 'sampmode', 3)
        ktl.waitfor(f'${service}.sampmode==3', timeout=2)
        ktl.write(service, 'itime', 5)
        ktl.waitfor(f'${service}.itime==5', timeout=2)
        ktl.write(service, 'numfs', 1)
        ktl.waitfor(f'${service}.numfs==1', timeout=2)
        ktl.write(service, 'coadds', 1)
        ktl.waitfor(f'${service}.coadds==1', timeout=2)

        framenumBefore1 = int(ktl.read(service, 'framenum'))
        tf._take_flats(logger=self.logger, cfg=self.cfg, nFrames=1)
        framenumAfter1 = int(ktl.read(service, 'framenum'))
        self.assertEqual(framenumAfter1, framenumBefore1+1)

        filename = ktl.read(service, 'filename')
        self.assertTrue(os.path.exists(filename))


        framenumBefore3 = int(ktl.read(service, 'framenum'))
        tf._take_flats(logger=self.logger, cfg=self.cfg, nFrames=3)
        framenumAfter3 = int(ktl.read(service, 'framenum'))
        self.assertEqual(framenumAfter3, framenumBefore3+3)

        filename = ktl.read(service, 'filename')
        self.assertTrue(os.path.exists(filename))

    def test_execute(self):
        service = 'nsds'
        ktl.write(service, 'sampmode', 3)
        ktl.waitfor(f'${service}.sampmode==3', timeout=2)
        ktl.write(service, 'itime', 5)
        ktl.waitfor(f'${service}.itime==5', timeout=2)
        ktl.write(service, 'numfs', 1)
        ktl.waitfor(f'${service}.numfs==1', timeout=2)
        ktl.write(service, 'coadds', 1)
        ktl.waitfor(f'${service}.coadds==1', timeout=2)

        framenumBefore1 = int(ktl.read(service, 'framenum'))

        args = {
            'nFrames': 1,
        }
        tf.execute( args=args, logger=self.logger, cfg=self.cfg )
        framenumAfter1 = int(ktl.read(service, 'framenum'))
        self.assertEqual(framenumAfter1, framenumBefore1+1)

        filename = ktl.read(service, 'filename')
        self.assertTrue(os.path.exists(filename))

        framenumBefore3 = int(ktl.read(service, 'framenum'))
        tf._take_flats(logger=self.logger, cfg=self.cfg, nFrames=3)
        framenumAfter3 = int(ktl.read(service, 'framenum'))
        self.assertEqual(framenumAfter3, framenumBefore3+3)
        
        filename = ktl.read(service, 'filename')
        self.assertTrue(os.path.exists(filename))

if __name__ == "__main__":
    unittest.main()
