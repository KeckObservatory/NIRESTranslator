"""
Takes arc frames

Arguments:
- num_exposures (optional, default in config)

Replaces:
goarcs
niresarcs
"""

from NIRESTranslatorFunction import NIRESTranslatorFunction

class TakeArcs(NIRESTranslatorFunction):

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        pass

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass