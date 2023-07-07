"""
Takes dome flat frames

Arguments:
- num_exposures (optional, default in config)

Replaces:
goflats
"""

try:
    import ktl
except ImportError:
    ktl=""
from NIRESTranslatorFunction import NIRESTranslatorFunction
from ..shared.take_exposures import TakeExposures as te
from .toggle_dome_lamps import ToggleDomeLamp as tdl

class TakeFlats(NIRESTranslatorFunction):

    @classmethod
    def _take_flats(cls, logger, cfg, nFrames=1, manual=False):
        """takes nFrames flats using the NIRES spec server

        Args:
            logger (class): Logger object
            cfg (class): Config object
            nFrames (int, optional): number of flat frames to take. Defaults to 1.
            manual (bool): if True, does not automatically set ktl kws sampmode, itime, numfs, coadds
        """        

        cls._write_to_ktl('nsds', 'obstype', 'domeflat', logger, cfg)
        if not manual:
            cls._write_to_ktl('nsds', 'sampmode', 3, logger, cfg)
            cls._write_to_ktl('nsds', 'itime', 100, logger, cfg)
            cls._write_to_ktl('nsds', 'numfs', 1, logger, cfg)
            cls._write_to_ktl('nsds', 'coadds', 1, logger, cfg)


        tdl.execute({'status': 'off'})
        tdl.execute({'status': 'spec'})

        
        teArgs = {'nFrames': nFrames, 'sv': 's'}
        te.execute(teArgs, logger, cfg)
        cls._write_to_ktl('nsds', 'go', 0, logger, cfg)

        tdl.execute({'status': 'off'})
        cls._write_to_ktl('nsds', 'obstype', 'object', logger, cfg)

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        pass

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass