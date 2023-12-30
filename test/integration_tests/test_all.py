from test.integration_tests.calibration.test_take_arcs import TestTakeArcs 
from test.integration_tests.calibration.test_take_darks import TestTakeDarks
from test.integration_tests.calibration.test_take_flats import TestTakeFlats
from test.integration_tests.calibration.test_take_flats_on_off import TestTakeFlatsOnOff
from test.integration_tests.calibration.test_toggle_dome_lamps import TestToggleDomeLamps
from test.integration_tests.shared.test_set_detector_configuration import TestSetDetectorConfiguration
from test.integration_tests.shared.test_take_exposures import TestTakeExposures
from test.integration_tests.shared.test_take_tests import TestTakeTests
from test.integration_tests.shared.test_wait_for_exposure import TestWaitForExposure
from test.integration_tests.spectrograph.test_dither import TestDither 


import unittest

if __name__ == "__main__":
    unittest.main()