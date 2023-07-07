"""
Set the dome lamps to on/off

Arguments:
- lamp_state (required, enum(on, off) )

Replaces:
domelamps
"""

from NIRESTranslatorFunction import NIRESTranslatorFunction
try:
    import ktl
except ImportError:
    ktl = "" 

class ToggleDomeLamp(NIRESTranslatorFunction):

    @classmethod
    def _toggle_dome_lamps(cls, status, logger, cfg):
        """domelamps -- turn spectral or imaging dome lamps on or off.
        Set the lamps to the specififed mode. Each set of lamps may be 
        turned on or off by issuing the appropriate command.

        Args:
            status (str):  Can be 'imaging', 'spectral', 'both', or 'off'
            logger (class): Logger object
            cfg (class): Config object
        """        
        status = status.lower()

        if 'spec' in status:
            cls._write_to_ktl('dcs2', 'flimagin', 0, logger, cfg)
            cls._write_to_ktl('dcs2', 'flspectr', 1, logger, cfg)
        elif 'im' in status:
            cls._write_to_ktl('dcs2', 'flimagin', 1, logger, cfg)
            cls._write_to_ktl('dcs2', 'flspectr', 0, logger, cfg)
        elif 'both' in status:
            cls._write_to_ktl('dcs2', 'flimagin', 1, logger, cfg)
            cls._write_to_ktl('dcs2', 'flspectr', 1, logger, cfg)
        elif 'off' in status:
            cls._write_to_ktl('dcs2', 'flimagin', 0, logger, cfg)
            cls._write_to_ktl('dcs2', 'flspectr', 0, logger, cfg)
        else:
            logger.debug('Invalid lamp status. Not setting lamps.')

    @classmethod
    def _show_lamp_status(cls, logger):
        """shows status of lamps.

        Args:
            logger (class): Logger object
        """        
        flimagin = ktl.read('dcs', 'flimagin')
        flspectr = ktl.read('dcs', 'flspectr')
        if flimagin=="on" and flspectr=="off":
            mode = "imaging"
        elif flimagin=="off" and flspectr=="on":
            mode = "spectral"
        elif flimagin=="on" and flspectr=="on":
            mode = "both"
        elif flimagin=="off" and flspectr=="off":
            mode = "off"
        else:
            logger.warning("Error invalid lamp mode")
            mode = "invalid"
        logger.info(f"Lamp mode: {mode}")

    @classmethod
    def _simulate_toggle_dome_lamps(cls, status, logger, cfg):
        if 'spec' in status:
            logger.info('spec lamps simulation "turned on')
        elif 'im' in status:
            logger.info('img lamps simulation "turned on')
        elif 'both' in status:
            logger.info('both lamps simulation "turned on')
        elif 'off' in status:
            logger.info('lamps simulation "turned off')
        else:
            logger.debug('Invalid lamp status. Not setting lamps.')

    
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        status = args.get('status', False)
        opMode = cfg['operation_mode']['operation_mode']
        if not status: # With no arguements, report the current status of the dome flatfield
            cls._show_lamp_status(logger)
        elif opMode == 'production':
            cls._toggle_dome_lamps(status, logger, cfg)
        else:
            cls._simulate_toggle_dome_lamps(status, logger, cfg)

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass