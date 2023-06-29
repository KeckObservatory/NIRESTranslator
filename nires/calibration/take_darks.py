"""
Takes dark frames

Arguments:
- num_exposures (optional, default in config)

Replaces:
godarks
"""

from NIRESTranslatorFunction import NIRESTranslatorFunction
from .toggle_dome_lamps import ToggleDomeLamp
from ..shared.take_exposures import TakeExposures
from ..shared.wait_for_exposure import WaitForExposure

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
        
        cls._write_to_ktl('nsds', 'obstype', 'dark')
        ToggleDomeLamp.execute({'status': 'off'})
        ToggleDomeLamp.execute({'status': 'spec'})

        teArgs = {'nFrames': nFrames, 'sv': 's'}
        TakeExposures.execute(teArgs, logger, cfg)
        cls._write_to_ktl('nsds', 'go', 0)

        ToggleDomeLamp.execute({'status': 'off'})
        cls._write_to_ktl('nsds', 'obstype', 'object')

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