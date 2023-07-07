from nires.calibration.toggle_dome_lamps import ToggleDomeLamp as tdl 
import unittest
from unittest.mock import Mock, patch, MagicMock
try:
    import ktl
except ImportError:
    ktl = Mock()


def ktl_side_effects(service, value):
    if value == 'flimagin': return 'on'
    if value == 'flspectr': return 'off' 
    return 0

def logger_side_effect(msg):
    print(msg)

def cfg_side_effect(service, value):
    if value == 'operation_mode': return 'testing'
    if value == 'n_read_padding': return 1 
    if value == 'extra_wait': return 1

class TestTakeExposures(unittest.TestCase):

    def setUp(self):
        ktl.read = Mock()
        ktl.read.side_effect = ktl_side_effects
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
    
    @patch('nires.calibration.toggle_dome_lamps.ktl')
    def test_toggle_dome_lamps(self, mock_ktl):
        tdl._toggle_dome_lamps('off', logger=self.logger, cfg=self.cfg)
        tdl._toggle_dome_lamps('both', logger=self.logger, cfg=self.cfg)
        tdl._toggle_dome_lamps('spectral', logger=self.logger, cfg=self.cfg)
        tdl._toggle_dome_lamps('imaging', logger=self.logger, cfg=self.cfg)

    @patch('nires.calibration.toggle_dome_lamps.ktl')
    def test_show_lamp_status(self, mock_ktl):
        mock_ktl.read = Mock()

        def ktl_side_effects_im(service, value):
            if value == 'flimagin': return 'on'
            if value == 'flspectr': return 'off' 
            return 0
        def ktl_side_effects_spec(service, value):
            if value == 'flimagin': return 'off'
            if value == 'flspectr': return 'on' 
            return 0
        def ktl_side_effects_both(service, value):
            if value == 'flimagin': return 'on'
            if value == 'flspectr': return 'on' 
            return 0
        def ktl_side_effects_off(service, value):
            if value == 'flimagin': return 'off'
            if value == 'flspectr': return 'off' 
            return 0

        mock_ktl.read.side_effect = ktl_side_effects_im
        tdl._show_lamp_status(logger=self.logger )
        mock_ktl.read.side_effect = ktl_side_effects_spec
        tdl._show_lamp_status(logger=self.logger )
        mock_ktl.read.side_effect = ktl_side_effects_both
        tdl._show_lamp_status(logger=self.logger )
        mock_ktl.read.side_effect = ktl_side_effects_off
        tdl._show_lamp_status(logger=self.logger )


if __name__ == "__main__":
    unittest.main()
