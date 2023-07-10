from nires.shared.set_detector_configuration import SetDetectorConfig as sdc
import unittest
import pdb
from unittest.mock import MagicMock, Mock
import time
try:
    import ktl
except ImportError:
    ktl = "" 


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
        self.logger = MagicMock(side_effect=logger_side_effect)
        self.logger.info.side_effect = logger_side_effect
        self.logger.debug.side_effect = logger_side_effect
        sdc._minimum_integration_time = Mock(return_value=1)
        self.cfg = {
            'ob_keys': {
                'n_read_padding': 1.5,
                'extra_wait': 1
            },
            'operation_mode': {
                'operation_mode': 'production'
            }
        }

    def test_set_integration_time(self):
        sdc.set_integration_time(5, sv="s", logger=self.logger, cfg=self.cfg)
        itime = ktl.read('nsds', 'itime')
        self.assertEqual(itime, 5)
        sdc.set_integration_time(4, sv="v", logger=self.logger, cfg=self.cfg)
        itime = ktl.read('nids', 'itime')
        self.assertEqual(itime, 4)
        sdc.set_integration_time(0, sv="s", logger=self.logger, cfg=self.cfg)
        itime = ktl.read('nsds', 'itime')
        mintime = sdc._minimum_integration_time('s')
        self.assertEqual(itime, mintime)

    def test_set_coadd(self):
        ktl.write('nsds', 'coadds', 2)
        sdc.set_coadd(1, sv='s', logger=self.logger, cfg=self.cfg)
        coadds = ktl.read('nsds', 'coadds')
        self.assertEqual(coadds, 1)
        sdc.set_coadd(0, sv='s', logger=self.logger, cfg=self.cfg)
        coadds = ktl.read('nsds', 'coadds')
        self.assertEqual(coadds, 1)
        sdc.set_coadd(-1, sv='s', logger=self.logger, cfg=self.cfg)
        coadds = ktl.read('nsds', 'coadds')
        self.assertEqual(coadds, 1)

    def test_set_readout_mode(self):
        ktl.write('nsds', 'sampmode', 2)
        ktl.write('nsds', 'numfs', 1)
        sdc.set_readout_mode(1, sv='s', logger=self.logger, cfg=self.cfg)
        sampmode = ktl.read('nsds', 'sampmode')
        self.assertEqual(sampmode, 1)
        sdc.set_readout_mode(2, sv='s', logger=self.logger, cfg=self.cfg)
        sampmode = ktl.read('nsds', 'sampmode')
        self.assertEqual(sampmode, 2)
        ktl.write('nsds', 'numfs', 1)
        sdc.set_readout_mode(3, sv='s', logger=self.logger, cfg=self.cfg, nSamp=5)
        sampmode = ktl.read('nsds', 'sampmode')
        numfs = ktl.read('nsds', 'numfs')
        self.assertEqual(sampmode, 3)
        self.assertEqual(numfs, 5)
        sdc.set_readout_mode(4, sv='s', logger=self.logger, cfg=self.cfg)
        sampmode = ktl.read('nsds', 'sampmode')
        self.assertEqual(sampmode, 4)

    def test_minimum_integration_time(self):

        # function uses nsds.numreads
        ktl.write('nsds', 'sampmode', 4)
        numreads = 2
        readtime = 2
        ktl.write('nsds', 'numreads', numreads)
        ktl.write('nsds', 'readtime', readtime)
        itime = sdc._minimum_integration_time('s')
        self.assertEqual(itime, numreads * readtime)

        # function uses numreads=1
        ktl.write('nsds', 'sampmode', 2)
        itime = sdc._minimum_integration_time('s')
        self.assertEqual(itime, readtime )


    def test_check_integration_time(self):

        ktl.write('nsds', 'sampmode', 4)
        numreads = 2
        readtime = 2
        itime = 1
        ktl.write('nsds', 'numreads', numreads)
        ktl.write('nsds', 'readtime', readtime)
        ktl.wait(f'$nsds.readtime == {readtime}', timeout=2)
        ktl.write('nsds', 'itime', itime)
        ktl.wait(f'$nsds.itime == {itime}', timeout=2)

        # integration time should be set by minimumTime 
        sdc.check_integration_time(sv='s', logger=self.logger, cfg=self.cfg)
        itime = ktl.read('nsds', 'itime')
        self.assertEqual(itime, numreads * readtime)

        # integration time should be set by itime
        time = 8
        ktl.write('nsds', 'itime', time)
        ktl.wait(f'$nsds.itime == {time}', timeout=2)
        sdc.check_integration_time(sv='s', logger=self.logger, cfg=self.cfg)
        itime = ktl.read('nsds', 'itime')
        self.assertEqual(itime, time)

    def test_set_number_of_samples(self):
        service = 'nsds'
        sv = 's'
        sdc.set_number_of_samples(11, sv=sv, logger=self.logger, cfg=self.cfg, readoutMode=3)
        numfs = ktl.read(service, 'numfs')
        self.assertEqual(numfs, 11)
        ktl.write(service, 'sampmode', 4)
        sdc.set_number_of_samples(12, sv=sv, logger=self.logger, cfg=self.cfg, readoutMode=None)
        numreads = ktl.read(service, 'numreads')
        self.assertEqual(numreads, 12)
        sdc.set_number_of_samples(13, sv=sv, logger=self.logger, cfg=self.cfg, readoutMode=1)
        numreads = ktl.read(service, 'numreads')
        self.assertEqual(numreads, 13)

    def test_perform(self):
        args = {}
        args['det_exp_number'] = 1
        args['det_exp_read_pairs'] = 2
        args['det_samp_mode'] = 1
        args['det_exp_time'] = 10
        args['sv'] = 's'
        service = 'nsds'
        sdc.perform(args=args, logger=self.logger, cfg=self.cfg)

        sampmode = ktl.read(service, 'sampmode')
        self.assertEqual(args['det_samo_mode'], sampmode)
        numreads = ktl.read(service, 'numreads')
        self.assertEqual(args['det_exp_read_pairs'], numreads)
        itime = ktl.read(service, 'itime')
        self.assertEqual(args['det_exp_time'], itime)
        coadds = ktl.read(service, 'coadds')
        self.assertEqual(args['det_exp_number'], coadds)


if __name__ == "__main__":
    unittest.main()

