import ktl

from nires.NIRESTranslatorFunction import NIRESTranslatorFunction


class test_function(NIRESTranslatorFunction):
    '''
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        raise NotImplementedError()

    @classmethod
    def post_condition(cls, args, logger, cfg):
        return True
