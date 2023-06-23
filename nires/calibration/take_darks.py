"""
Takes dark frames

Arguments:
- num_exposures (optional, default in config)

Replaces:
godarks
"""

from NIRESTranslatorFunction import NIRESTranslatorFunction

class TakeDarks(NIRESTranslatorFunction):

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        pass

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass