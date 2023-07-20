import os
import logging 
from DDOILoggerClient import DDOILogger as dl
from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
try:
    import ktl
except ImportError:
    ktl = ''
import time

class NIRESTranslatorFunction(TranslatorModuleFunction):

    @classmethod
    def send_fits_to_display(cls, fitspath, logger, cfg):
        
        # Keeping this here because it is in the original script.
        # Not sure if it is actually needed
        cls._write_to_ktl(service='nids', keyword='display2', value=0, logger=logger, cfg=cfg)


        cls._write_to_ktl(service='nids', keyword='dispname2', value=fitspath, logger=logger, cfg=cfg)
        time.sleep(cfg['image_display']['display_sleep_time'])
        cls._write_to_ktl(service='nids', keyword='display2', value=0, logger=logger, cfg=cfg)
        cls._write_to_ktl(service='nids', keyword='display2', value=1, logger=logger, cfg=cfg)
        cls._write_to_ktl(service='nids', keyword='comment', value=" ", logger=logger, cfg=cfg)

    @classmethod
    def _write_to_ktl(cls, service, keyword, value, logger, cfg, wait=None, timeout=None):
        if cfg['operation_mode']['operation_mode'].lower()=='operational':
            wait = wait if wait is not None else cfg['ob_keys']['ktl_wait']
            timeout = timeout if timeout is not None else cfg['ob_keys']['ktl_timeout']
            ktl.write(service, keyword, value, wait=wait, timeout=timeout)
        else:
            logger.debug(f'testing ktl.write({service}, {keyword}, {value})')
    
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
        sampmode = int(ktl.read(service, 'sampmode'))
             
        readtime = float(ktl.read(service, 'readtime'))
        if sampmode==1 or sampmode==2:
            nsamp = int(ktl.read(service, 'numreads'))
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

    @classmethod
    def wait_for_tel(cls, cfg, logger):
        # wait for slew to end...
        ktl.waitfor('dcs', 'axestat=tracking')
        # waitfor -s dcs axestat=tracking

        # check whether autoguider is active...
        if ktl.read('dcs' 'AUTACTIV') == "no":
            logger.error(f"Wait for telescope (wftel): guider not currently active")
            raise Exception
        
        # wait for AUTPAUSE to increment...

        initial_autresum = ktl.read('dcs', 'autresum')

        count = 0
        timeout = 20 # max guider exposure time

        while(True):
            new_autresum = ktl.read('dcs', 'autresum')
            if initial_autresum != new_autresum:
                break
            
            count += 1

            if count >= timeout:
                logger.error(f"Wait for telescope (wftel): timeout waiting for AUTRESUM to increment")
                break

            time.sleep(1)

          
        # monitor the keyword AUTGO to change to RESUMEACK, which is issued by the guider 

        count = 0
        timeout = 20 # max guider exposure time

        autgo_desired_values = ["RESUMEACK", "GUIDE"]


        while(True):
            autgo = str(ktl.read('dcs', 'autgo')).upper()

            if autgo in autgo_desired_values:
                break

            count += 1
            
            if count >= timeout:
                logger.error(f"Wait for telescope (wftel): timeout waiting for AUTGO to be [{','.join(autgo_desired_values)}]")
                break

            time.sleep(1)