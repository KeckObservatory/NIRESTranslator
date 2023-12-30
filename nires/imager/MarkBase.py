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
        dcs = args['dcs']
        cls._write_to_ktl(dcs, 'mark', True, logger, cfg)

    @classmethod
    def post_condition(cls, pc_args, logger, cfg):
       pass
