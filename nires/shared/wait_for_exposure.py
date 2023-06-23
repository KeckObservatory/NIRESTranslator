"""
Waits for exposure to finish (blocking)

Arguments:
- sv (required, enum(s, v, sv) )

Replaces:
wfg(s/v)
"""

from NIRESTranslatorFunction import NIRESTranslatorFunction

class WaitForExposure(NIRESTranslatorFunction):

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        pass

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass