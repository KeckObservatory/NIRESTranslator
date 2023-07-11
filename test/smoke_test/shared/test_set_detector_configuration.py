from nires.shared.set_detector_configuration import SetDetectorConfig as sdc
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
    if value == 'itime': return 6
    if value == 'sampmode': return 2
    if value == 'numreads': return 3
    if value == 'readtime': return 4
    return 0

def logger_side_effect(msg):
    print(msg)

def cfg_side_effect(service, value):
    if value == 'operation_mode': return 'testing'

class TestSetDetectorConfiguration(unittest.TestCase):

    def setUp(self):
        ktl.read = Mock()
        ktl.read.side_effect = ktl_side_effects
        self.logger = MagicMock(side_effect=logger_side_effect)
        self.logger.info.side_effect = logger_side_effect
        self.logger.debug.side_effect = logger_side_effect
        sdc._minimum_integration_time = Mock(return_value=1)
        self.cfg = MagicMock('cfg', side_effect=cfg_side_effect)
        

    @patch('nires.shared.set_detector_configuration.ktl')
    def test_set_integration_time(self, mock_ktl):
        mock_ktl.read = Mock()
        mock_ktl.read.side_effect = ktl_side_effects
        sdc.set_integration_time(5, sv="s", logger=self.logger, cfg=self.cfg)
        sdc.set_integration_time(4, sv="v", logger=self.logger, cfg=self.cfg)
        sdc.set_integration_time(None, sv="s", logger=self.logger, cfg=self.cfg)

    @patch('nires.shared.set_detector_configuration.ktl')
    def test_set_coadd(self, mock_ktl):
        mock_ktl.read = Mock()
        mock_ktl.read.side_effect = ktl_side_effects
        sdc.set_coadd(1, sv='s', logger=self.logger, cfg=self.cfg)
        sdc.set_coadd(0, sv='s', logger=self.logger, cfg=self.cfg)
        sdc.set_coadd(-1, sv='s', logger=self.logger, cfg=self.cfg)
        sdc.set_coadd(None, sv='s', logger=self.logger, cfg=self.cfg)

    @patch('nires.shared.set_detector_configuration.ktl')
    def test_set_readout_mode(self, mock_ktl):
        mock_ktl.read = Mock()
        mock_ktl.read.side_effect = ktl_side_effects

        sdc.check_integration_time = Mock()
        sdc.set_number_of_samples = Mock()
        sdc.set_readout_mode(1, sv='s', logger=self.logger, cfg=self.cfg)
        sdc.set_readout_mode(2, sv='s', logger=self.logger, cfg=self.cfg)
        sdc.set_readout_mode(3, sv='s', logger=self.logger, cfg=self.cfg, nSamp=1)
        sdc.set_readout_mode(4, sv='s', logger=self.logger, cfg=self.cfg)

        sdc.set_readout_mode('UTR', sv='s', logger=self.logger, cfg=self.cfg, nSamp=1)
        sdc.set_readout_mode('PCDS', sv='s', logger=self.logger, cfg=self.cfg, nSamp=1)
        sdc.set_readout_mode('MCDS', sv='s', logger=self.logger, cfg=self.cfg, nSamp=1)
        sdc.set_readout_mode('single', sv='s', logger=self.logger, cfg=self.cfg, nSamp=1)

        sdc.set_readout_mode(None, sv='s', logger=self.logger, cfg=self.cfg)
        sdc.set_readout_mode(3, sv='s', logger=self.logger, cfg=self.cfg, nSamp=None)


    @patch('nires.shared.set_detector_configuration.ktl')
    def test_check_integration_time(self, mock_ktl):
        mock_ktl.read = Mock()
        mock_ktl.read.side_effect = ktl_side_effects
        sdc._minimum_integration_time = Mock()
        sdc._minimum_integration_time.side_effect = lambda _: 1 

        sdc.check_integration_time(sv='s', logger=self.logger, cfg=self.cfg)

        sdc._minimum_integration_time.side_effect = lambda x: 10 
        sdc.set_integration_time = Mock()
        sdc.check_integration_time(sv='s', logger=self.logger, cfg=self.cfg)


    @patch('nires.shared.set_detector_configuration.ktl')
    def test_set_number_of_samples(self, mock_ktl):
        mock_ktl.read = Mock()
        mock_ktl.read.side_effect = ktl_side_effects

        sdc.set_number_of_samples(11, sv='s', logger=self.logger, cfg=self.cfg, readoutMode=3)
        sdc.set_number_of_samples(12, sv='s', logger=self.logger, cfg=self.cfg, readoutMode=None)
        sdc.set_number_of_samples(13, sv='s', logger=self.logger, cfg=self.cfg, readoutMode=1)

        sdc.set_number_of_samples(None, sv='s', logger=self.logger, cfg=self.cfg, readoutMode=1)
        sdc.set_number_of_samples(None, sv='s', logger=self.logger, cfg=self.cfg, readoutMode=3)


    @patch('nires.shared.set_detector_configuration.ktl')
    def test_perform(self, mock_ktl):
        mock_ktl.read = Mock()
        mock_ktl.read.side_effect = ktl_side_effects
        sdc.check_integration_time = Mock()
        args = {}
        args['nCoadd'] = 1 
        args['numreads'] = 2 
        args['readoutMode'] = 1 
        args['itime'] = 10 
        args['sv'] = 's'
        sdc.perform(args=args, logger=self.logger, cfg=self.cfg)

if __name__ == "__main__":
    unittest.main()

