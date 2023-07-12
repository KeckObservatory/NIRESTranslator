from nires.shared.set_detector_configuration import SetDetectorConfig as sdc
import unittest
import pdb
from unittest.mock import MagicMock, Mock
import time
import ktl


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
                'operation_mode': 'operational'
            }
        }

    def test_set_integration_time(self):

        service = 'nsds'
        sdc.set_integration_time(5, sv="s", logger=self.logger, cfg=self.cfg)
        itime = ktl.read(service, 'itime')
        self.assertEqual(itime, 5)
        sdc.set_integration_time(4, sv="v", logger=self.logger, cfg=self.cfg)
        itime = ktl.read(service, 'itime')
        self.assertEqual(itime, 4)

        ktl.write(service, 'sampmode', 2)
        ktl.write(service, 'readtime', 3)
        sdc.set_integration_time(0, sv="s", logger=self.logger, cfg=self.cfg)
        itime = ktl.read(service, 'itime')
        mintime = sdc._minimum_integration_time('s')
        self.assertEqual(itime, mintime)

    def test_set_coadd(self):
        service = 'nsds'
        ktl.write(service, 'coadds', 2)
        ktl.wait(f'${service}.coadds=={2}', timeout=2)
        sdc.set_coadd(1, sv='s', logger=self.logger, cfg=self.cfg)
        coadds = ktl.read(service, 'coadds')
        self.assertEqual(coadds, 1)

        ktl.write(service, 'coadds', 2)
        ktl.wait(f'${service}.coadds=={2}', timeout=2)
        sdc.set_coadd(0, sv='s', logger=self.logger, cfg=self.cfg)
        coadds = ktl.read(service, 'coadds')
        self.assertEqual(coadds, 1)

        ktl.write(service, 'coadds', 2)
        ktl.wait(f'${service}.coadds=={2}', timeout=2)
        sdc.set_coadd(-1, sv='s', logger=self.logger, cfg=self.cfg)
        coadds = ktl.read(service, 'coadds')
        self.assertEqual(coadds, 1)

    def test_set_readout_mode(self):
        service = 'nsds'
        ktl.write(service, 'sampmode', 2)
        ktl.wait(f'${service}.sampmode==2', timeout=2)
        ktl.write(service, 'numfs', 1)
        ktl.wait(f'${service}.numfs=={1}', timeout=2)

        sdc.set_readout_mode(1, sv='s', logger=self.logger, cfg=self.cfg)
        sampmode = ktl.read(service, 'sampmode')
        self.assertEqual(sampmode, 1)

        sdc.set_readout_mode(2, sv='s', logger=self.logger, cfg=self.cfg)
        sampmode = ktl.read(service, 'sampmode')
        self.assertEqual(sampmode, 2)

        sdc.set_readout_mode(3, sv='s', logger=self.logger, cfg=self.cfg, nSamp=5)
        sampmode = ktl.read(service, 'sampmode')
        numfs = ktl.read(service, 'numfs')
        self.assertEqual(sampmode, 3)
        self.assertEqual(numfs, 5)

        sdc.set_readout_mode(4, sv='s', logger=self.logger, cfg=self.cfg)
        sampmode = ktl.read(service, 'sampmode')
        self.assertEqual(sampmode, 4)

    def test_minimum_integration_time(self):

        # function uses nsds.numreads
        sampmode = 2
        service = 'nsds'
        ktl.write(service, 'sampmode', sampmode)
        ktl.wait(f'${service}.sampmode=={sampmode}', timeout=2)
        numreads = 2
        readtime = 2
        ktl.write(service, 'numreads', numreads)
        ktl.wait(f'${service}.numreads=={numreads}', timeout=2)
        ktl.write(service, 'readtime', readtime)
        ktl.wait(f'${service}.readtime=={readtime}', timeout=2)

        itime = sdc._minimum_integration_time('s')
        self.assertEqual(itime, numreads * readtime)

        # function uses numreads=1
        sampmode = 4
        ktl.write(service, 'sampmode', sampmode)
        ktl.wait(f'${service}.sampmode=={sampmode}', timeout=2)
        itime = sdc._minimum_integration_time('s')
        self.assertEqual(itime, readtime )


    def test_check_integration_time(self):

        service = 'nsds'
        sampmode = 4
        numreads = 2
        readtime = 2
        itime = 1

        ktl.write(service, 'sampmode', sampmode)
        ktl.wait(f'${service}.sampmode=={sampmode}', timeout=2)
        ktl.write(service, 'numreads', numreads)
        ktl.wait(f'${service}.numreads=={numreads}', timeout=2)
        ktl.write(service, 'readtime', readtime)
        ktl.wait(f'${service}.readtime == {readtime}', timeout=2)
        ktl.write(service, 'itime', itime)
        ktl.wait(f'${service}.itime == {itime}', timeout=2)

        # integration time should be set by minimumTime 
        sdc.check_integration_time(sv='s', logger=self.logger, cfg=self.cfg)
        itime = ktl.read(service, 'itime')
        self.assertEqual(itime, numreads * readtime)

        # integration time should be set by itime
        time = 8
        ktl.write(service, 'itime', time)
        ktl.wait(f'${service}.itime == {time}', timeout=2)
        sdc.check_integration_time(sv='s', logger=self.logger, cfg=self.cfg)
        itime = ktl.read(service, 'itime')
        self.assertEqual(itime, time)

    def test_set_number_of_samples(self):
        service = 'nsds'
        sv = 's'
        sampmode = 3 # Fowler
        ktl.write(service, 'sampmode', sampmode)
        ktl.wait(f'$nsds.sampmode=={sampmode}', timeout=2)

        sdc.set_number_of_samples(11, sv=sv, logger=self.logger, cfg=self.cfg, readoutMode=3)
        numfs = ktl.read(service, 'numfs')
        self.assertEqual(numfs, 11)
        sampmode = 4
        ktl.write(service, 'sampmode', sampmode)
        ktl.wait(f'$nsds.sampmode=={sampmode}', timeout=2)
        sdc.set_number_of_samples(12, sv=sv, logger=self.logger, cfg=self.cfg, readoutMode=None)
        numreads = ktl.read(service, 'numreads')
        self.assertEqual(numreads, 12)
        sdc.set_number_of_samples(13, sv=sv, logger=self.logger, cfg=self.cfg, readoutMode=1)
        numreads = ktl.read(service, 'numreads')
        self.assertEqual(numreads, 13)

    def test_execute(self):
        args = {}

        args['nCoadd'] = 1 
        args['numreads'] = 2 
        args['readoutMode'] = 1 
        args['itime'] = 10 
        args['sv'] = 's'
        service = 'nsds'
        sdc.execute(args=args, logger=self.logger, cfg=self.cfg)

        sampmode = ktl.read(service, 'sampmode')
        self.assertEqual(args['readoutMode'], sampmode)
        numreads = ktl.read(service, 'numreads')
        self.assertEqual(args['numreads'], numreads)
        itime = ktl.read(service, 'itime')
        self.assertEqual(args['itime'], itime)
        coadds = ktl.read(service, 'coadds')
        self.assertEqual(args['nCoadds'], coadds)



if __name__ == "__main__":
    unittest.main()

