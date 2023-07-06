import os
import logging 
from DDOILoggerClient import DDOILogger as dl
from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
try:
    import ktl
except ImportError:
    ktl = ''


class NIRESTranslatorFunction(TranslatorModuleFunction):

    @classmethod
    def _write_to_ktl(cls, service, keyword, value, logger, cfg, wait=None, timeout=None):
        if cfg['operation_mode']['operation_mode'].lower()=='production':
            wait = wait if wait is not None else cfg['ob_keys']['ktl_wait']
            timeout = timeout if timeout is not None else cfg['ob_keys']['ktl_timeout']
            ktl.write(service, keyword, value, wait=wait, timeout=timeout)
        else:
            logger.write('testing ktl.write({service}, {keyword}, {value})')
    
    @classmethod
    def _determine_nires_service(cls, sv):
        """determines if use spectrograph (nsds) or imager server (nids)

        Args:
            sv (int): spec 's' or imager 'v'

        Returns:
            str:  
        """
        if sv == 's':
            service = 'nsds'
        elif sv == 'v':
            service = 'nids'
        else:
            raise(f"input variable sv={sv} not 's' or 'v'")
        return service

    @classmethod
    def _minimum_integration_time(cls, sv):
        """Calculates the minimum integration time for the NIRES imaging detector.

        Args:
            sv (int): spec 's' or imager 'v'

        Returns:
            int: minimum integration time for NIRES 
        """        
        service = cls._determine_nires_service(sv)
        sampmode = ktl.read(service, 'sampmode')
        readtime = ktl.read(service, 'readtime')
        if sampmode==1 or sampmode==2:
            nsamp = ktl.read(service, 'numreads')
        else:
            nsamp = 1
        minTime = nsamp * readtime
        return minTime
        

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