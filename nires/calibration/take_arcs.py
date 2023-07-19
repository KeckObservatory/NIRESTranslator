"""
Takes arc frames

Arguments:
- num_exposures (optional, default in config)

Replaces:
goarcs
niresarcs
"""
import pdb
try:
    import ktl
except ImportError:
    ktl=""
from subprocess import Popen

from nires.NIRESTranslatorFunction import NIRESTranslatorFunction
from ..shared.take_exposures import TakeExposures
from ..shared.wait_for_exposure import WaitForExposure 

class TakeArcs(NIRESTranslatorFunction):

    @classmethod
    def _take_arcs(cls, logger, cfg, nFrames=None):
        """take nFrames arcs using the NIRES spec server.

        Args:
            nFrames (int): number of frames 
            sv (int): spec 's' or imager 'v'
            cfg (class): Config object
            logger (class): Logger object
        """

        framenum = int(ktl.read('nsds', 'framenum'))
        logger.info(f'taking frame # {framenum}')

        isoperational = cfg['operation_mode']['operation_mode'] == 'operational'
        cls._write_to_ktl('nsds', 'obstype', 'domearc', logger, cfg)

        if isoperational:
            userserver = cfg['operation_mode']['arclamp_user_server']
            Popen(["ssh", userserver, "power", "on", "8"])
        else:
            logger.debug('simulating turning arclamps on.')
        if nFrames:
            fileName = ktl.read('nsds', 'filename')
            logger.info(f'Writing {nFrames} starting on File {fileName}')
            teArgs = {'nFrames': nFrames, 'sv': 's'}
            TakeExposures.execute(teArgs, logger, cfg)
            cls._write_to_ktl('nsds', 'GO', 0, logger, cfg, True)
        else:
            teArgs = {'nFrames': 1, 'sv': 's'}
            # TODO: verify that original script has gois commented out intentionally! 
            # TakeExposures.execute(teArgs, logger, cfg)
            
        if isoperational:
            userserver = cfg['operation_mode']['arclamp_user_server']
            Popen(["ssh", userserver, "power", "off", "8"])
        else:
            logger.debug('simulating turning arclamps off.')
        cls._write_to_ktl('nsds', 'obstype', 'object', logger, cfg)
        

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        nFrames = args.get('nFrames', None)
        cls._take_arcs(logger, cfg, nFrames)

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass