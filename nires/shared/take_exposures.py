"""
Takes exposure(s)

Arguments:
- sv (required, enum(s, v, sv) )
- num_exposures (required, int)

Replaces:
goi(s/v)
goisv
"""
import pdb
try:
    import ktl
except ImportError:
    ktl=""
import time

from nires.NIRESTranslatorFunction import NIRESTranslatorFunction
from .wait_for_exposure import WaitForExposure 

class TakeExposures(NIRESTranslatorFunction):

    @classmethod
    def _take_an_exposure(cls, logger, cfg, nFrames=1, sv='s'):
        """Takes an exposure to on
        the H2RG detector (spectrograph), 
        H1 imaging detector, or both

        Args:
            logger (class): Logger object
            cfg (class): cfg object
            nFrames (int): Number of frames to take
            sv (int): spec 's', imager 'v', or both 'sv' 
        """

        if 'sv' in sv:
            cls._take_an_sv_exposure(logger, cfg, nFrames)
            # run take an exposure on both in parallel
            return
        service = cls._determine_nires_service(sv)
        framenum = int(ktl.read(service, 'framenum'))
        logger.info(f'Taking {nFrames} using service {service}. Starting on frame # {framenum}')

        maxFrames = nFrames
        while nFrames > 0:
            nFrames = nFrames - 1
            cls.expose(service, sv, logger, cfg)
            fileName = ktl.read(service, 'filename')
            if (nFrames > 0):
                logger.info(f'Took file {fileName}, {nFrames} left out of {maxFrames}')
                time.sleep(1)
    
    @classmethod
    def expose(cls, service, sv, logger, cfg):
        cls._write_to_ktl(service, 'GO', 0, logger, cfg)
        cls._write_to_ktl(service, 'GO', 1, logger, cfg)
        WaitForExposure.execute({'sv': sv}, logger, cfg)
        cls._write_to_ktl(service, 'GO', 0, logger, cfg)

    @classmethod
    def _take_an_sv_exposure(cls, logger, cfg, nFrames):
        """Takes an exposure to on both
        the H2RG detector (spectrograph) and
        H1 imaging detector

        Args:
            logger (class): Logger object
            cfg (class): cfg object
            nFrames (int): Number of frames to take
        """

        framenums = ktl.read('nsds', 'framenum')
        framenumv = ktl.read('nids', 'framenum')
        logger.info(f'Taking nsds frame # {framenums}')
        logger.info(f'Taking nids frame # {framenumv}')

        while nFrames > 0:
            cls._write_to_ktl('nsds', 'GO', 0, logger, cfg)
            cls._write_to_ktl('nids', 'GO', 0, logger, cfg)
            cls._write_to_ktl('nsds', 'GO', 1, logger, cfg)
            cls._write_to_ktl('nids', 'GO', 1, logger, cfg)

            fileNames = ktl.read('nsds', 'filename')
            fileNamev = ktl.read('nids', 'filename')

            WaitForExposure.execute({'sv': 's'}, logger, cfg)

            cls._write_to_ktl('nsds', 'GO', 0, logger, cfg)
            cls._write_to_ktl('nids', 'GO', 0, logger, cfg)
            nFrames = nFrames - 1
            if (nFrames > 0):
                logger.info(f'Took file {fileNames}, {nFrames} left')
                time.sleep(1)


    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        nFrames = args['nFrames']
        sv = args['sv']
        cls._take_an_exposure(logger, cfg, nFrames=nFrames, sv=sv)

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass