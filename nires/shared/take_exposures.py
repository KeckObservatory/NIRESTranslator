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
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        pass

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass