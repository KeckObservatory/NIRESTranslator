from test.smoke_test.calibration.test_take_arcs import TestTakeArcs 
from test.smoke_test.calibration.test_take_darks import TestTakeDarks
from test.smoke_test.calibration.test_take_flats import TestTakeFlats
from test.smoke_test.calibration.test_take_flats_on_off import TestTakeFlatsOnOff
from test.smoke_test.calibration.test_toggle_dome_lamps import TestToggleDomeLamps
from test.smoke_test.shared.test_set_detector_configuration import TestSetDetectorConfiguration
from test.smoke_test.shared.test_take_exposures import TestTakeExposures
from test.smoke_test.shared.test_take_tests import TestTakeTests
from test.smoke_test.shared.test_wait_for_exposure import TestWaitForExposure


import unittest

if __name__ == "__main__":
    unittest.main()