"""
Takes on/off dome flat frames

Arguments:
- num_exposures (optional, default in config)

Replaces:
goflatonoff
"""

from NIRESTranslatorFunction import NIRESTranslatorFunction

class TakeFlatsOnOff(NIRESTranslatorFunction):

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        pass

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass