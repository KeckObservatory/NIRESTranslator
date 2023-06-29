"""
Take a test exposure

Arguments:
- sv (required, enum(s, v, sv) )
- num_exposures (required, int)

Replaces:
test(s/v)
"""

from NIRESTranslatorFunction import NIRESTranslatorFunction
from ..shared.wait_for_exposure import WaitForExposure 
import ktl

class TakeTests(NIRESTranslatorFunction):

    @classmethod
    def take_test(cls, nFrames, sv, logger, cfg):
        """Takes a test exposure.

        Args:
            nFrames (int): number of frames 
            sv (int): spec 's' or imager 'v'
            logger (class): Logger object
            cfg (class): cfg object
        """        

        service = cls._determine_nires_service(sv)
        if nFrames>0:
            while nFrames > 0:
                cls._write_to_ktl(service, 'test', 0)
                cls._write_to_ktl(service, 'test', 1)
                WaitForExposure.execute({'sv', sv}, logger, cfg)
                nFrames = nFrames - 1
                logger.info(f"nFrames left: {nFrames}")
        else:
            cls._write_to_ktl(service, 'test', 1)
            WaitForExposure.execute({'sv', sv}, logger, cfg)
            cls._write_to_ktl(service, 'test', 0)

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        nFrames = args.get('nFrames', False)
        sv = args['sv']
        logger.info(f'taking {nFrames} test exposure(s)')
        cls.take_tests(nFrames, sv, logger, cfg)

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass