import ktl
import time
"""
Takes exposure(s)

Arguments:
- sv (required, enum(s, v, sv) )
- num_exposures (required, int)

Replaces:
goi(s/v)
goisv
"""

from NIRESTranslatorFunction import NIRESTranslatorFunction

class TakeExposures(NIRESTranslatorFunction):

    @classmethod
    def _take_an_exposure(cls, logger, cfg, nFrames=1, sv='s'):
        """Takes an exposure to on
        the H2RG detector (spectrograph), 
        H1 imaging detector, or both

        Args:
            nFrames (int): Number of frames to take
            sv (int): spec 's', imager 'v', or both 'sv' 
            logger (class): Logger object
        """

        if 'sv' in sv:
            cls._take_an_sv_exposure(logger, cfg, nFrames)
            # run take an exposure on both in parallel
            return
        service = cls._determine_nires_service(sv)
        framenum = ktl.read(service, 'framenum')
        logger.info(f'Taking {service} frame # {framenum}')

        while nFrames > 0:
            cls._write_to_ktl(service, 'GO', 0, logger, cfg)
            cls._write_to_ktl(service, 'GO', 1, logger, cfg)
            fileName = ktl.read(service, 'filename')
            cls.wait_for_exposure()
            cls._write_to_ktl(service, 'GO', 0, logger, cfg)
            nFrames = nFrames - 1
            if (nFrames > 0):
                logger.info(f'Took file {fileName}, {nFrames} left')
                time.sleep(1)

    @classmethod
    def _take_an_sv_exposure(cls, logger, cfg, nFrames):
        """Takes an exposure to on both
        the H2RG detector (spectrograph) and
        H1 imaging detector

        Args:
            nFrames (int): Number of frames to take
            logger (class): Logger object
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

            cls.wait_for_exposure('s') # Wait for spec exposure to take, assume imager takes just as long.

            cls._write_to_ktl('nsds', 'GO', 0, logger, cfg)
            cls._write_to_ktl('nids', 'GO', 0, logger, cfg)
            nFrames = nFrames - 1
            if (nFrames > 0):
                logger.info(f'Took file {fileNames}, {nFrames} left')
                logger.info(f'Took file {fileNamev}, {nFrames} left')
                time.sleep(1)


    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        pass

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass