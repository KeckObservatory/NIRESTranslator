from nires.calibration.toggle_dome_lamps import ToggleDomeLamp as tdl 
import unittest
from unittest.mock import Mock, patch, MagicMock
import ktl


def logger_side_effect(msg):
    print(msg)

class TestToggleDomeLamps(unittest.TestCase):

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
                'operation_mode': 'production'
            }
        }
    
    def test_toggle_dome_lamps(self):
        sts = 'off'
        tdl._toggle_dome_lamps(sts, logger=self.logger, cfg=self.cfg)
        status = tdl._show_lamp_status(self.logger)
        self.assertEqual(sts, status)
        sts = 'both'
        tdl._toggle_dome_lamps(sts, logger=self.logger, cfg=self.cfg)
        status = tdl._show_lamp_status(self.logger)
        self.assertEqual(sts, status)
        sts = 'spectral'
        tdl._toggle_dome_lamps(sts, logger=self.logger, cfg=self.cfg)
        status = tdl._show_lamp_status(self.logger)
        self.assertEqual(sts, status)
        sts = 'imaging'
        tdl._toggle_dome_lamps(sts, logger=self.logger, cfg=self.cfg)
        status = tdl._show_lamp_status(logger=self.logger)
        self.assertEqual(sts, status)


if __name__ == "__main__":
    unittest.main()
