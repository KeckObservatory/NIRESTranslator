"""
Set the dome lamps to on/off

Arguments:
- lamp_state (required, enum(on, off) )

Replaces:
domelamps
"""

from NIRESTranslatorFunction import NIRESTranslatorFunction
import ktl

class ToggleDomeLamp(NIRESTranslatorFunction):

    @classmethod
    def toggle_dome_lamps(cls, status, logger, cfg):
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
            cls._write_to_ktl('dcs2', 'flimagin', 0)
            cls._write_to_ktl('dcs2', 'flspectr', 1)
        elif 'im' in status:
            cls._write_to_ktl('dcs2', 'flimagin', 1)
            cls._write_to_ktl('dcs2', 'flspectr', 0)
        elif 'both' in status:
            cls._write_to_ktl('dcs2', 'flimagin', 1)
            cls._write_to_ktl('dcs2', 'flspectr', 1)
        elif 'off' in status:
            cls._write_to_ktl('dcs2', 'flimagin', 0)
            cls._write_to_ktl('dcs2', 'flspectr', 0)
        else:
            logger.debug('Invalid lamp status. Not setting lamps.')

    @classmethod
    def show_lamp_status(cls, logger):
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
        elif flimagin=="off" and flspectr=="off":
            mode = "off"
        elif flimagin=="on" and flspectr=="on":
            mode = "both"
        else:
            logger.warning("Error invalid lamp mode")
        logger.info(f"Lamp mode: {mode}")

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        status = args.get('status', False)
        if not status: # With no arguements, report the current status of the dome flatfield
            cls.show_lamp_status(logger)
        else:
            cls.toggle_dome_lamps(status, logger, cfg)

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass