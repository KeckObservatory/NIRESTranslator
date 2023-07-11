from nires.calibration.take_flats_on_off import TakeFlatsOnOff as tfof 
import unittest
from unittest.mock import Mock, patch, MagicMock
import ktl


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
        framenumBeforeSpec = ktl.read(services, 'framenum')
        
        servicev = 'nids'
        ktl.write(servicev, 'sampmode', 3)
        ktl.wait(f'${servicev}.sampmode=={3}', timeout=2)
        ktl.write(servicev, 'itime', 5)
        ktl.wait(f'${servicev}.itime=={5}', timeout=2)
        ktl.write(servicev, 'numfs', 1)
        ktl.wait(f'${servicev}.numfs=={1}', timeout=2)
        ktl.write(servicev, 'coadds', 1)
        ktl.wait(f'${servicev}.coadds=={1}', timeout=2)
        framenumBeforeImag = ktl.read(servicev, 'framenum')

        tfof._take_flats_on_off(logger=self.logger, cfg=self.cfg, nFrames=2)
        
        framenumAfterSpec = ktl.read(services, 'framenum')
        framenumAfterImag = ktl.read(servicev, 'framenum')

        self.assertEqual(framenumAfterSpec, framenumBeforeSpec+1)
        self.assertEqual(framenumAfterImag, framenumBeforeImag+1)

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
        framenumBeforeSpec = ktl.read(services, 'framenum')
        
        servicev = 'nids'
        ktl.write(servicev, 'sampmode', 3)
        ktl.wait(f'${servicev}.sampmode=={3}', timeout=2)
        ktl.write(servicev, 'itime', 5)
        ktl.wait(f'${servicev}.itime=={5}', timeout=2)
        ktl.write(servicev, 'numfs', 1)
        ktl.wait(f'${servicev}.numfs=={1}', timeout=2)
        ktl.write(servicev, 'coadds', 1)
        ktl.wait(f'${servicev}.coadds=={1}', timeout=2)
        framenumBeforeImag = ktl.read(servicev, 'framenum')

        args = {
            'nFrames': 1
        }
        tfof.execute(args=args, logger=self.logger, cfg=self.cfg)
        
        framenumAfterSpec = ktl.read(services, 'framenum')
        framenumAfterImag = ktl.read(servicev, 'framenum')

        self.assertEqual(framenumAfterSpec, framenumBeforeSpec+1)
        self.assertEqual(framenumAfterImag, framenumBeforeImag+1)

if __name__ == "__main__":
    unittest.main()
