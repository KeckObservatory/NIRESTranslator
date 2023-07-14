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
from nires.NIRESTranslatorFunction import NIRESTranslatorFunction
from ..shared.take_exposures import TakeExposures as te
from .toggle_dome_lamps import ToggleDomeLamp as tdl

class TakeFlats(NIRESTranslatorFunction):

    @classmethod
    def _take_flats(cls, logger, cfg, nFrames=1):
        """takes nFrames flats using the NIRES spec server

        Args:
            logger (class): Logger object
            cfg (class): Config object
            nFrames (int, optional): number of flat frames to take. Defaults to 1.
        """        

        cls._write_to_ktl('nsds', 'obstype', 'domeflat', logger, cfg)

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
        nFrames = args.get('nFrames', 1)
        cls._take_flats(logger=logger, cfg=cfg, nFrames=nFrames)

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass