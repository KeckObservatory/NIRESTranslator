"""
Takes on/off dome flat frames

Arguments:
- num_exposures (optional, default in config)

Replaces:
goflatonoff
"""
import ktl
import time
from NIRESTranslatorFunction import NIRESTranslatorFunction
from ..shared.take_exposures import TakeExposures
from .toggle_dome_lamps import ToggleDomeLamp

class TakeFlatsOnOff(NIRESTranslatorFunction):

    @classmethod
    def _take_flats_on_off(cls, logger, cfg, nFrames=1):
        """takes nFrames flats with lamps on and nFrames off
        using the NIRES spec server.

        Args:
            logger (class): Logger object
            cfg (class): Config object
            nFrames (int, optional): number of flat frames to take. Defaults to 1.
        """        


        cls._write_to_ktl('nsds', 'obstype', 'domeflat', logger, cfg)
        cls._write_to_ktl('nsds', 'sampmode', 3, logger, cfg)
        cls._write_to_ktl('nsds', 'itime', 100, logger, cfg)
        cls._write_to_ktl('nsds', 'numfs', 1, logger, cfg)
        cls._write_to_ktl('nsds', 'coadds', 1, logger, cfg)

        ToggleDomeLamp.execute({'status': 'off'})
        ToggleDomeLamp.execute({'status': 'spec'})

        # Take one frame with dome lamps on and then one frame with dome lamps off for nFrames times.
        logger.info(f"Taking {nFrames} flats and {nFrames} darks each.")
        maxFrames = nFrames
        while nFrames > 0:
            ToggleDomeLamp.execute({'status': 'off'})
            ToggleDomeLamp.execute({'status': 'spec'})
            cls._write_to_ktl('nsds', 'obstype', 'domeflat', logger, cfg)
            TakeExposures.expose('nsds', 's', logger, cfg)
            fileName = ktl.read('nsds', 'filename')
            if (nFrames > 0):
                logger.info(f'Took file {fileName}, {nFrames} left out of {maxFrames} light flats')
                time.sleep(1)

            ToggleDomeLamp.execute({'status': 'off'})
            cls._write_to_ktl('nsds', 'obstype', 'dark', logger, cfg)
            TakeExposures.expose('nsds', 's', logger, cfg)
            fileName = ktl.read('nsds', 'filename')
            if (nFrames > 0):
                logger.info(f'Took file {fileName}, {nFrames} left out of {maxFrames} dark flats')
                time.sleep(1)

        ToggleDomeLamp.execute({'status': 'off'})
        cls._write_to_ktl('nsds', 'obstype', 'object', logger, cfg)

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        nFrames = args.get('nFrames', None)
        cls._take_flats_on_off(cls, logger, cfg, nFrames)

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass