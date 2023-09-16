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

class SltMov(NIRESTranslatorFunction):

   
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        cls.sltmov(args, logger, cfg)

    @classmethod
    def post_condition(cls, pc_args, logger, cfg):
       pass

    @classmethod
    def sltmov(cls, args, logger, cfg):

        dcs = args['dcs']
        offset = args['offset']

        # Call to sltmov
        angle = -2.02
        dx = offset * math.sin(math.radians(angle))
        dy = offset * math.cos(math.radians(angle))


        # Which calls mxy...
        autoresum = ktl.read('dcs2', 'autresum')

        cls._write_to_ktl(dcs, 'instxoff', dx, logger, cfg)
        cls._write_to_ktl(dcs, 'instyoff', dy, logger, cfg)
        cls._write_to_ktl(dcs, 'rel2curr', 't', logger, cfg)

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

        serv_auto_resume = ktl.cache(dcs, 'autresum')
        serv_auto_go = ktl.cache(dcs, 'autgo')

        # # set the value for the current autpause
        # if not autoresum:
        #     autoresum = serv_auto_resume.read()

        wftel_wait = 20

        success = False
        for i in range(0, wftel_wait):
            value = serv_auto_resume.read()
            if value != autoresum:
                success = True
                break
        
        if not success:
            logger.error("Timeout exceeded waiting for AUTRESUM to increment")
            raise Exception("KTL timeout reached for AUTRESUM")
        
        success = False
        for i in range(0, wftel_wait):
            value = serv_auto_go.read()
            if value == "RESUMEACK" or value == "GUIDE":
                success = True
                break

        if not success:
            logger.error("Timeout exceeded waiting for AUTGO to reach RESUMEACK or GUIDE")
            raise Exception("KTL timeout reached for AUTGO")

        end = time.time()
        elapsed = end - start
        logger.info(f"wftel elapsed in {elapsed} sec")
