"""
Takes dark frames

Arguments:
- num_exposures (optional, default in config)

Replaces:
godarks
"""

import pdb
try:
    import ktl
except ImportError:
    ktl=""
from nires.NIRESTranslatorFunction import NIRESTranslatorFunction
from .toggle_dome_lamps import ToggleDomeLamp as tdl
from ..shared.take_exposures import TakeExposures as te

class TakeDarks(NIRESTranslatorFunction):

    @classmethod
    def _take_darks(cls, nFrames, logger, cfg):
        """takes nFrames darks using the NIRES spec server with 
        the exp time and Fowler mode defined before

        Args:
            nFrames (int): number of frames 
            logger (class): Logger object
            cfg (class): Config object
        """
        
        cls._write_to_ktl('nsds', 'obstype', 'dark', logger, cfg)
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
        cls._take_darks(nFrames, logger, cfg)
        pass

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass