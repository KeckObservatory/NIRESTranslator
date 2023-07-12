from nires.calibration.take_darks import TakeDarks as td
import unittest
from unittest.mock import MagicMock
import ktl
import os


def logger_side_effect(msg):
    print(msg)

class TestTakeDarks(unittest.TestCase):

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
                'operation_mode': 'operational'
            }
        }
    
    def test_take_darks(self):

        service = 'nsds'
        ktl.write(service, 'sampmode', 3)
        ktl.wait(f'${service}.sampmode=={3}', timeout=2)
        ktl.write(service, 'itime', 5)
        ktl.wait(f'${service}.itime=={5}', timeout=2)
        ktl.write(service, 'numfs', 1)
        ktl.wait(f'${service}.numfs=={1}', timeout=2)
        ktl.write(service, 'coadds', 1)
        ktl.wait(f'${service}.coadds=={1}', timeout=2)

        framenumBefore = ktl.read(service, 'framenum')
        td._take_darks(1, logger=self.logger, cfg=self.cfg)
        framenumAfter = ktl.read(service, 'framenum')
        self.assertEqual(framenumAfter, framenumBefore+1)

        filename = ktl.read(service, 'filename')
        self.assertTrue(os.path.exists(filename))

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

        framenumBefore = ktl.read(service, 'framenum')
        args = {
            'nFrames': 1
        }
        td.execute(args=args, logger=self.logger, cfg=self.cfg)
        framenumAfter = ktl.read(service, 'framenum')
        self.assertEqual(framenumAfter, framenumBefore+1)

        filename = ktl.read(service, 'filename')
        self.assertTrue(os.path.exists(filename))

if __name__ == "__main__":
    unittest.main()
