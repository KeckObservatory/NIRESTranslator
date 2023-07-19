from nires.calibration.take_flats_on_off import TakeFlatsOnOff as tfof 
import unittest
from unittest.mock import Mock, patch, MagicMock
import ktl
import os


def logger_side_effect(msg):
    print(msg)

class TestTakeFlatsOnOff(unittest.TestCase):

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
    
    def test_take_flats_on_off(self):
        services = 'nsds'
        ktl.write(services, 'sampmode', 3)
        ktl.wait(f'${services}.sampmode=={3}', timeout=2)
        ktl.write(services, 'itime', 5)
        ktl.wait(f'${services}.itime=={5}', timeout=2)
        ktl.write(services, 'numfs', 1)
        ktl.wait(f'${services}.numfs=={1}', timeout=2)
        ktl.write(services, 'coadds', 1)
        ktl.wait(f'${services}.coadds=={1}', timeout=2)
        framenumBeforeSpec = int(ktl.read(services, 'framenum'))
        
        tfof._take_flats_on_off(logger=self.logger, cfg=self.cfg, nFrames=2)
        
        framenumAfterSpec = int(ktl.read(services, 'framenum'))

        self.assertEqual(framenumAfterSpec, framenumBeforeSpec+2)

        filenames = ktl.read(services, 'filename')
        self.assertTrue(os.path.exists(filenames))

    def test_execute(self):
        services = 'nsds'
        ktl.write(services, 'sampmode', 3)
        ktl.wait(f'${services}.sampmode=={3}', timeout=2)
        ktl.write(services, 'itime', 5)
        ktl.wait(f'${services}.itime=={5}', timeout=2)
        ktl.write(services, 'numfs', 1)
        ktl.wait(f'${services}.numfs=={1}', timeout=2)
        ktl.write(services, 'coadds', 1)
        ktl.wait(f'${services}.coadds=={1}', timeout=2)
        framenumBeforeSpec = int(ktl.read(services, 'framenum'))
        
        args = {
            'nFrames': 1
        }
        tfof.execute(args=args, logger=self.logger, cfg=self.cfg)
        
        framenumAfterSpec = int(ktl.read(services, 'framenum'))

        self.assertEqual(framenumAfterSpec, framenumBeforeSpec+1)

        filenames = ktl.read(services, 'filename')
        self.assertTrue(os.path.exists(filenames))


if __name__ == "__main__":
    unittest.main()
