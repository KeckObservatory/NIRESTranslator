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
    def _take_arcs(cls, logger, cfg, nFrames=None, manual=False):
        """take nFrames arcs using the NIRES spec server.

        Args:
            nFrames (int): number of frames 
            manual (bool): if True, does not automatically set ktl kws sampmode, itime, numfs, coadds
            sv (int): spec 's' or imager 'v'
            cfg (class): Config object
            logger (class): Logger object
        """

        framenum = ktl.read('nsds', 'framenum')
        logger.info(f'taking frame # {framenum}')

        isoperational = cfg['operation_mode']['operation_mode'] == 'operational'
        cls._write_to_ktl('nsds', 'obstype', 'domearc', logger, cfg)
        if not manual:
            cls._write_to_ktl('nsds', 'sampmode', 3, logger, cfg)
            cls._write_to_ktl('nsds', 'itime', 120, logger, cfg)
            cls._write_to_ktl('nsds', 'numfs', 1, logger, cfg)
            cls._write_to_ktl('nsds', 'coadds', 1, logger, cfg)

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
        manual = args.get('manual', False)
        cls._take_arcs(logger, cfg, nFrames, manual)

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass