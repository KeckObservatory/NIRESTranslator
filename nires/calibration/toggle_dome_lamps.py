"""
Set the dome lamps to on/off

Arguments:
- lamp_state (required, enum(on, off) )

Replaces:
domelamps
"""

from NIRESTranslatorFunction import NIRESTranslatorFunction

class ToggleDomeLamp(NIRESTranslatorFunction):

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        pass

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass