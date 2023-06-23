"""
Take a test exposure

Arguments:
- sv (required, enum(s, v, sv) )
- num_exposures (required, int)

Replaces:
test(s/v)
"""

from NIRESTranslatorFunction import NIRESTranslatorFunction

class TakeTests(NIRESTranslatorFunction):

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        pass

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass