"""
Takes arc frames

Arguments:
- num_exposures (optional, default in config)

Replaces:
goarcs
niresarcs
"""
import ktl
import os
import time
from subprocess import Popen

from NIRESTranslatorFunction import NIRESTranslatorFunction
from ..shared.take_exposures import TakeExposures
from ..shared.wait_for_exposure import WaitForExposure 

class TakeArcs(NIRESTranslatorFunction):

    @classmethod
    def _take_arcs(cls, logger, cfg, nFrames=None, manual=True):
        """take nFrames arcs using the NIRES spec server.

        Args:
            nFrames (int): number of coadds 
            manual (bool): if True, does not set ktl kws sampmode, itime, numfs, coadds
            sv (int): spec 's' or imager 'v'
            cfg (class): Config object
            logger (class): Logger object
        """

        framenum = ktl.read('nsds', 'framenum')
        logger.info(f'taking frame # {framenum}')

        cls._write_to_ktl('nsds', 'obstype', 'domearc', logger, cfg)
        if manual:
            cls._write_to_ktl('nsds', 'sampmode', 3, logger, cfg)
            cls._write_to_ktl('nsds', 'itime', 120, logger, cfg)
            cls._write_to_ktl('nsds', 'numfs', 1, logger, cfg)
            cls._write_to_ktl('nsds', 'coadds', 1, logger, cfg)

        Popen(["ssh", "nireseng@niresserver1", "power", "on", "8"])
        if nFrames == None:
            nFrames = framenum
            teArgs = {'nFrames': nFrames, 'sv': 's'}
            TakeExposures.execute(teArgs, logger, cfg)
        else:
            fileName = ktl.read('nsds', 'filename')
            logger.info(f'File {fileName}')
            teArgs = {'nFrames': nFrames, 'sv': 's'}
            TakeExposures.execute(teArgs, logger, cfg)
            cls._write_to_ktl('nsds', 'GO', 0, logger, cfg, True)
            
        Popen(["ssh", "nireseng@niresserver1", "power", "off", "8"])
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