"""
Sets the following detector parameters:
- integration time
- number of coadds
- readout mode (what type of sampling)
- number of samples

Arguments:
- sv (required, enum(s, v, sv) )
- Integration time (optional, float)
- Co-adds (optional, int)
- sampmode (UTR/1, PCDS/2, MCDS/3, Single/4)
- nsamp (optional, int)

Replaces:
tint(s/v)
coadd(s/v)
sampmode(s/v)
nsamp(s/v)
"""
import ktl

from NIRESTranslatorFunction import NIRESTranslatorFunction

class SetDetectorConfig(NIRESTranslatorFunction):

    @classmethod
    def set_integration_time(cls, requestTime, sv, logger, cfg):
        """Sets the integration time to n seconds for either the NIRES spectrographic or imager detector.

        Args:
            requestTime (float): time in seconds.
            sv (int): spec 's' or imager 'v'
            cfg (class): Config object
            logger (class): Logger object
        """

        service = cls._determine_nires_service(sv) 
        if not requestTime:
            iTime = ktl.read(service, 'itime')
            logger.info(f'{service} itime set to: {iTime}')
            return

        if requestTime:
            minimumTime = cls._minimum_integration_time()
            timeTooSmall = requestTime-minimumTime < 0
            
            time = minimumTime if (timeTooSmall) else requestTime
            if timeTooSmall: logger.debug(f'Request for integration less than the minimum {minimumTime}')
            cls._write_to_ktl(service, 'itime', time, logger, cfg)
            msg = f'Integration time set to {time}'
            logger.info(msg)
        else:
            itime = ktl.read(service, 'itime')
            logger.info(f'itime={itime}')

    @classmethod
    def set_coadd(cls, nCoadd, sv, logger, cfg):
        """will configure the NIRES spec/imaging server to 
        coadd nCoadd integrations into one frame.

        Args:
            nCoadd (int): number of coadds 
            sv (int): spec 's' or imager 'v'
            cfg (class): Config object
            logger (class): Logger object
        """

        service = cls._determine_nires_service(sv) 
        if not nCoadd:
            nCoadd = ktl.read(service, 'coadds')
            logger.info(f'{service} coadds set to: {nCoadd}')
            return

        if nCoadd<1:
            nCoadd=1
            logger.info('Attempt to set coadds to zero; coadds will be set to 1.')
        cls._write_to_ktl(service, 'coadds', nCoadd, logger, cfg)

    @classmethod
    def set_readout_mode(cls, readoutMode, sv, logger, cfg, nSamp=None):
        """For the NIRES imaging/spec detector, sets the readout mode to
        one of four types. If MCDS is chosen, a second parameter can be used to set
        the number of samples. 

        Args:
            readoutMode (int): Known modes are:
                                1 (or "UTR") Up The Ramp sampling 
                                2 (or "PCDS") Pseudo Correlated Double Sampling
                                3 (or "MCDS") Multiple-read Correlated Double (Fowler) Sampling
                                4 (or "single") Single exposure
            sv (int): spec 's' or imager 'v'
            logger (class): Logger object
            cfg (class): Config object
        """
        service = cls._determine_nires_service(sv) 

        if not readoutMode: # reading out keyword
            readoutMode = ktl.read(service, 'sampmode')
            cls.log_readout_mode(readoutMode, logger)
            return

        if isinstance(readoutMode, str): # readout mode can be a string!
            if 'UTR' in readoutMode:
                readoutMode = 1
            elif 'PCDS' in readoutMode or 'pcds' in readoutMode:
                readoutMode = 2
            elif any([x in readoutMode for x in ['MCDS', 'mcds', 'Fowler', 'fowler']]):
                readoutMode = 3
            elif 'single' in readoutMode or 'Single' in readoutMode:
                readoutMode = 4
            else:
                logger.warn(f"Do not understand sampling mode {readoutMode}. Not going to set.")
                return
            
            readoutModeValid = cls.log_readout_mode(readoutMode, logger)
            if not readoutModeValid:
                return

        cls._write_to_ktl(service, 'sampmode', readoutMode, logger, cfg)

        if readoutMode==3 and nSamp:
            logger.info(f'Setting number of Fowler mode samples to {nSamp}')
            cls.set_number_of_samples(nSamp, sv, logger, readoutMode)

        cls.check_integration_time(sv, logger)

    @classmethod
    def log_readout_mode(cls, readoutMode, logger):
        if readoutMode == 1:
            msg = "Sampling mode = 1 (up the Ramp sampling)"
        elif readoutMode == 2:
            msg = "Sampling mode = 2 (pseudo-correlated double sampling)"
        elif readoutMode == 3:
            msg = "Sampling mode = 3 (multiple correlated double (Fowler) sampling)"
        elif readoutMode == 4:
            msg = "Sampling mode = 4 (single sample)"
        else:
            logger.warn(f"Do not understand sampling mode {readoutMode}. Not going to set.")
            return False
        logger.info(msg)
        return True
    
    @classmethod
    def check_integration_time(cls, sv, logger, cfg):
        """Compare integration time with minimum time and reset if nessessary

        Args:
            sv (int): spec 's' or imager 'v'
            logger (class): Logger object
            cfg (dict): Config object
        """
        service = cls._determine_nires_service(sv) 
        integrationTime = ktl.read(service, 'itime')
        minimumTime = cls._minimum_integration_time(sv)
        iTimeTooSmall = integrationTime - minimumTime < 0
        if iTimeTooSmall:
            logger.debug(f"setting itime to minimum itime {minimumTime}")
            cls.set_integration_time(minimumTime, sv, logger, cfg)

    @classmethod
    def set_number_of_samples(cls, nSamp, sv, logger, cfg, readoutMode=None):
        """Sets the number of MCDS (multiple double-correlated sampling) mode
        reads to nSamp for the NIRES spectrograph/imager server.

        Args:
            nSamp (int): number of Fowler Samples 
            sv (int): spec 's' or imager 'v'
            cfg (dict): Config object
            logger (class): Logger object
            readoutMode (int): Optional. Use if you dont want to read sampmode. 
                               Known modes are:
                                1 (or "UTR") Up The Ramp sampling 
                                2 (or "PCDS") Pseudo Correlated Double Sampling
                                3 (or "MCDS") Multiple-read Correlated Double (Fowler) Sampling
                                4 (or "single") Single exposure
        """        

        service = cls._determine_nires_service(sv) 

        if nSamp:
            if not readoutMode:
                readoutMode = ktl.read(service, 'sampmode')

            if readoutMode==3: # Fowler mode
                cls._write_to_ktl(service, 'numfs', nSamp, logger, cfg)
            else:
                cls._write_to_ktl(service, 'numreads', nSamp, logger, cfg)
            # Check to make sure minumum 
            # integration time is consitant with old
            cls.check_integration_time(sv, logger, cfg) 
        else: # If nSamp is not included
            keyword = 'numfs' if readoutMode==3 else 'numreads'
            nSamp = ktl.read(service, keyword)
            logger.info('{service} {keyword}: {}')
             
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        nCoadd = args['det_exp_number']
        nSamp = args['det_exp_read_pairs'] # is nSamp == readPairs?
        readoutMode = args['det_samp_mode']
        requestTime = args['det_exp_time']

        sv = args['sv']
        logger.info('setting coadd')
        cls.set_coadd(nCoadd, sv, logger, cfg)
        logger.info('setting integration time')
        cls.set_integration_time(requestTime, sv, logger, cfg)
        logger.info('setting readout mode')
        cls.set_readout_mode(readoutMode, sv, logger, cfg, nSamp) 
        logger.info('set_dectector_configuration complete')
        

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass