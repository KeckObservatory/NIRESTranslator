"""
Takes a box dither pattern in SKY COORDINATES

Arguments:
- num_pos (required, enum(4, 5, 8, 9) )
- x (required, float)
- y (required, float)

Replaces:
box(4,5,8,9)
"""

from NIRESTranslatorFunction import NIRESTranslatorFunction

class BoxPattern(NIRESTranslatorFunction):

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        pass

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass