import pdb
import math
import time
from unittest.mock import Mock 
from astropy.coordinates import SkyCoord
from astropy import units as u

try:
    import ktl
except ImportError:
    ktl = Mock()
from nires.shared.take_exposures import TakeExposures

from nires.NIRESTranslatorFunction import NIRESTranslatorFunction

class en(NIRESTranslatorFunction):

   
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        cls.en(args, logger, cfg)

    @classmethod
    def post_condition(cls, pc_args, logger, cfg):
       pass

    @classmethod
    def en(cls, args, logger, cfg):

        dcs = args['dcs']

        ra = args['ra']
        dec = args['dec']

        autoresum = ktl.read('dcs2', 'autresum')
        guiding = True
        if ktl.read(dcs, 'AUTACTIV') == "no":
            logger.info(f"Wait for telescope (wftel): guider not currently active")
            guiding = False

        cls._write_to_ktl(dcs, 'raoff', ra, logger, cfg)
        cls._write_to_ktl(dcs, 'decoff', dec, logger, cfg)
        cls._write_to_ktl(dcs, 'rel2curr', 't', logger, cfg)
        
        if guiding:
            # Which calls wftel...
            start = time.time()

            try:
                for i in range(0, 20):
                    value = ktl.read('dcs2', 'axestat')
                    if value == 'tracking':
                        waited = True
                        break
                    time.sleep(1)
                # waited = ktl.waitfor('axestat=tracking', service=dcs,
                #                      timeout=cfg['ob_keys']['ktl_wait'])
            except:
                waited = False

            if not waited:
                msg = f'tracking was not established! Exiting'
                logger.error(msg)
                raise ValueError(msg)

            if ktl.read(dcs, 'autactiv') == 'no':
                msg = 'guider not currently active! Exiting'
                logger.error(msg)
                raise ValueError(msg)

            # serv_auto_resume = ktl.cache(dcs, 'autresum')
            # serv_auto_go = ktl.cache(dcs, 'autgo')

            # # set the value for the current autpause
            # if not autoresum:
            #     autoresum = serv_auto_resume.read()

            wftel_wait = 20

            success = False
            logger.info(f'Waiting for autresum to not equal {autoresum}')
            for i in range(0, wftel_wait):
                # value = serv_auto_resume.read()
                value = ktl.read('dcs2', 'autresum')
                if value != autoresum:
                    success = True
                    break
                time.sleep(1)
            
            if not success:
                logger.error("Timeout exceeded waiting for AUTRESUM to increment")
                raise Exception("KTL timeout reached for AUTRESUM")
            
            success = False
            for i in range(0, wftel_wait):
                # value = serv_auto_go.read()
                value = ktl.read('dcs2', 'autgo')
                if value == "resumeack" or value == "guide":
                    success = True
                    break
                time.sleep(1)

            if not success:
                logger.error("Timeout exceeded waiting for AUTGO to reach RESUMEACK or GUIDE")
                raise Exception("KTL timeout reached for AUTGO")

            end = time.time()
            elapsed = end - start
            logger.info(f"wftel elapsed in {elapsed} sec")
        else:
            logger.info("Not guiding, so not waiting for tracking to be established")
