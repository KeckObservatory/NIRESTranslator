try:
    import ktl
except:
    print("KTL could not be imported!")
    ktl = ""
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

from NIRESTranslatorFunction import NIRESTranslatorFunction

class SetDetectorConfig(NIRESTranslatorFunction):

    @classmethod
    def set_integration_time(cls, requestTime, sv, logger):
        """Sets the integration time to n seconds for either the NIRES spectrographic or imager detector.

        Args:
            requestTime (float): time in seconds.
            sv (int): spec 's' or imager 'v'
            logger (class): Logger object
        """
        minimumTime = cls.minimum_integration_time()
        timeTooSmall = requestTime-minimumTime < 0
        
        time = minimumTime if (timeTooSmall) else requestTime
        if timeTooSmall: logger.debug(f'Request for integration less than the minimum {minimumTime}')
        service = cls.determine_nires_service(sv) 
        ktl.write(service, 'itime', time, wait=True, timeout=2)
        msg = f'Integration time set to {time}'
        logger.info(msg)

    @classmethod
    def set_coadd(cls, nCoadd, sv, logger):
        """will configure the NIRES spec/imaging server to 
        coadd n integrations into one frame.

        Args:
            n (int): number of coadds 
            sv (int): spec 's' or imager 'v'
            logger (class): Logger object
        """

        if nCoadd<1:
            nCoadd=1
            logger.info('Attempt to set coadds to zero; coadds will be set to 1.')
        service = cls.determine_nires_service(sv) 
        ktl.write(service, 'coadds', nCoadd, wait=True, timeout=2)

    @classmethod
    def set_readout_mode(cls, readoutMode, sv, logger, nSamp=None):
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
        """

        if readoutMode == 1:
            msg = "Sampling mode = 1 (up the Ramp sampling)"
        elif readoutMode == 2:
            msg = "Sampling mode = 2 (pseudo-correlated double sampling)"
        elif readoutMode == 3:
            msg = "Sampling mode = 3 (multiple correlated double (Fowler) sampling)"
        elif readoutMode == 4:
            msg = "Sampling mode = 4 (single sample)"
        else:
            logger.warn("Do not understand sampling mode. Not going to set.")
            return
            

        logger.info(msg)
        service = cls.determine_nires_service(sv) 
        ktl.write(service, 'sampmode', readoutMode, wait=True, timeout=2)

        if readoutMode==3 and nSamp:
            logger.info(f'Setting number of Fowler mode samples to {nSamp}')
            cls.set_number_of_samples(nSamp, sv, logger, readoutMode)

        cls.check_integration_time(sv, logger)
    
    @classmethod
    def check_integration_time(cls, sv, logger):
        """Compare integration time with minimum time and reset if nessessary

        Args:
            sv (int): spec 's' or imager 'v'
            logger (class): Logger object
        """
        service = cls.determine_nires_service(sv) 
        integrationTime = ktl.read(service, 'itime')
        minimumTime = cls.minimum_integration_time(sv)
        iTimeTooSmall = integrationTime-minimumTime < 0
        if iTimeTooSmall:
            logger.debug("setting itime to zero")
            cls.set_integration_time(minimumTime, sv, logger)

    @classmethod
    def set_number_of_samples(cls, nSamp, sv, logger, readoutMode=None):
        """Sets the number of MCDS (multiple double-correlated sampling) mode
        reads to nSamp for the NIRES spectrograph/imager server.

        Args:
            nSamp (int): number of Fowler Samples 
            sv (int): spec 's' or imager 'v'
            logger (class): Logger object
            readoutMode (int): Optional. Use if you dont want to read sampmode. 
                               Known modes are:
                                1 (or "UTR") Up The Ramp sampling 
                                2 (or "PCDS") Pseudo Correlated Double Sampling
                                3 (or "MCDS") Multiple-read Correlated Double (Fowler) Sampling
                                4 (or "single") Single exposure
        """        

        service = cls.determine_nires_service(sv) 

        if not readoutMode:
            readoutMode = ktl.read(service, 'sampmode')

        if readoutMode==3: # Fowler mode
            ktl.write(service, 'numfs', nSamp)
        else:
            ktl.write(service, 'numreads', nSamp)
        # Check to make sure minumum 
        # integration time is consitant with old
        cls.check_integration_time(sv, logger) 
             
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        pass

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass