from nires.calibration.take_flats import TakeFlats as tf 
import unittest
from unittest.mock import Mock, patch, MagicMock
import ktl


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
                'extra_wait': 1
            },
            'operation_mode': {
                'operation_mode': 'test'
            }
        }
    
    def test_take_flats(self):
        service = 'nsds'
        ktl.write(service, 'sampmode', 3)
        ktl.wait(f'${service}.sampmode=={3}', timeout=2)
        ktl.write(service, 'itime', 5)
        ktl.wait(f'${service}.itime=={5}', timeout=2)
        ktl.write(service, 'numfs', 1)
        ktl.wait(f'${service}.numfs=={1}', timeout=2)
        ktl.write(service, 'coadds', 1)
        ktl.wait(f'${service}.coadds=={1}', timeout=2)

        framenumBefore1 = ktl.read(service, 'framenum')
        tf._take_flats(logger=self.logger, cfg=self.cfg, nFrames=1, manual=True)
        framenumAfter1 = ktl.read(service, 'framenum')
        self.assertEqual(framenumAfter1, framenumBefore1+1)

        framenumBefore3 = ktl.read(service, 'framenum')
        tf._take_flats(logger=self.logger, cfg=self.cfg, nFrames=3, manual=True)
        framenumAfter3 = ktl.read(service, 'framenum')

        self.assertEqual(framenumAfter3, framenumBefore3+3)

    def test_execute(self):
        service = 'nsds'
        ktl.write(service, 'sampmode', 3)
        ktl.wait(f'${service}.sampmode=={3}', timeout=2)
        ktl.write(service, 'itime', 5)
        ktl.wait(f'${service}.itime=={5}', timeout=2)
        ktl.write(service, 'numfs', 1)
        ktl.wait(f'${service}.numfs=={1}', timeout=2)
        ktl.write(service, 'coadds', 1)
        ktl.wait(f'${service}.coadds=={1}', timeout=2)

        framenumBefore1 = ktl.read(service, 'framenum')

        args = {
            'nFrames': 1,
            'manual': True
        }
        tf.execute( args=args, logger=self.logger, cfg=self.cfg )
        framenumAfter1 = ktl.read(service, 'framenum')
        self.assertEqual(framenumAfter1, framenumBefore1+1)

        framenumBefore3 = ktl.read(service, 'framenum')
        tf._take_flats(logger=self.logger, cfg=self.cfg, nFrames=3, manual=True)
        framenumAfter3 = ktl.read(service, 'framenum')

        self.assertEqual(framenumAfter3, framenumBefore3+3)

if __name__ == "__main__":
    unittest.main()
