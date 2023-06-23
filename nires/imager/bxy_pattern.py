"""
Takes a box dither pattern in DETECTOR COORDINATES

Arguments:
- num_pos (required, enum(4, 5, 8, 9) )
- x (required, int)
- y (required, int)

Replaces:
bxy(4,5,8,9)
"""

from NIRESTranslatorFunction import NIRESTranslatorFunction

class BoxXYPattern(NIRESTranslatorFunction):

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        pass

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass