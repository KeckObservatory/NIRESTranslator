from nires.shared.set_detector_configuration import SetDetectorConfig as sdc
from nires.NIRESTranslatorFunction import NIRESTranslatorFunction as ntf 
import unittest
import pdb
from unittest.mock import Mock, patch, MagicMock 
from unittest.mock import MagicMock 
import time
try:
    import ktl
except ImportError:
    ktl = Mock()


def ktl_side_effects(service, value):
    if value == 'sampmode': return 2
    if value == 'numreads': return 3
    if value == 'readtime': return 4
    return 0

def ktl_side_effects_2(service, value):
    return 3

class TestNIRESTranslatorFunction(unittest.TestCase):

    def setUp(self):
        ktl.read = Mock()
        ktl.read.side_effect = ktl_side_effects
    
    @patch('nires.NIRESTranslatorFunction.ktl')
    def test_minimum_integration_time(self, mock_ktl):
        mock_ktl.read = Mock()
        mock_ktl.read.side_effect = ktl_side_effects
        ntf._minimum_integration_time('s')
        minTime = ntf._minimum_integration_time('v')
        self.assertEqual(minTime, 12)

        mock_ktl.read.side_effect = ktl_side_effects_2
        minTime = ntf._minimum_integration_time('v')
        self.assertEqual(minTime, 3)



if __name__ == "__main__":
    unittest.main()

