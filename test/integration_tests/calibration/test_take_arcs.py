from nires.calibration.take_arcs import TakeArcs as ta 
import unittest
from unittest.mock import MagicMock
import ktl


def logger_side_effect(msg):
    print(msg)

class TestTakeArcs(unittest.TestCase):

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
    
    def test_take_arcs(self):
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
        ta._take_arcs(logger=self.logger, cfg=self.cfg, nFrames=1, manual=True)
        framenumAfter = ktl.read(service, 'framenum')
        self.assertEqual(framenumAfter, framenumBefore+1)

if __name__ == "__main__":
    unittest.main()
