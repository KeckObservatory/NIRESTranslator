"""
Takes an arbitrary dither pattern along the slit

Arguments:
- pattern (required, string)

Replaces:
abba
sp(2,3,5,7)
"""

from NIRESTranslatorFunction import NIRESTranslatorFunction

class Dither(NIRESTranslatorFunction):

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        pass

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass