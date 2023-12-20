from nires.shared.wait_for_exposure import WaitForExposure as wfe 
from nires.shared.set_detector_configuration import SetDetectorConfig as sdc
import unittest
from unittest.mock import Mock, patch, MagicMock
import ktl
import os


def logger_side_effect(msg):
    print(msg)

class TestTakeTests(unittest.TestCase):

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
                'operation_mode': 'operational'
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
    
    def test_wait_for_exposure(self):
        args = {}
        args['sv'] = 'v'
        wfe.execute(args, logger=self.logger, cfg=self.cfg)


if __name__ == "__main__":
    unittest.main()
