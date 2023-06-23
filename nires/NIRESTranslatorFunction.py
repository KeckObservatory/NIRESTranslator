import os

from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction

try:
    import ktl
except:
    print("KTL could not be imported!")
    ktl = ""


class NIRESTranslatorFunction(TranslatorModuleFunction):

    def _cfg_location(cls, args):
        """
        Return the fullpath + filename of default configuration file.

        :param args: <dict> The OB (or portion of OB) in dictionary form

        :return: <list> fullpath + filename of default configuration
        """
        cfg_path_base = os.path.dirname(os.path.abspath(__file__))

        inst = 'nires'
        cfg = f"{cfg_path_base}/ddoi_configurations/{inst}_inst_config.ini"
        config_files = [cfg]

        return config_files

    @classmethod
    def abort_execution(cls, args, logger, cfg):
        if cls.abortable != True:
            logger.warning('Abort recieved, but this method is not aboratble.')
            return False

    # @classmethod
    # def pre_condition(cls, args, logger, cfg):
    #     pass

    # @classmethod
    # def post_condition(cls, args, logger, cfg):
    #     pass