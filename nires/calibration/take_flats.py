"""
Takes dome flat frames

Arguments:
- num_exposures (optional, default in config)

Replaces:
goflats
"""

from NIRESTranslatorFunction import NIRESTranslatorFunction

class TakeFlats(NIRESTranslatorFunction):

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        pass

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass