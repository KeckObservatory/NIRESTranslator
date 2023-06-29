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
    def take_arcs(cls, logger, cfg, nFrames=None, manual=True):
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
            while nFrames > 0:
                teArgs = {'nFrames': nFrames, 'sv': 's'}
                TakeExposures.execute(teArgs, logger, cfg)
                fileName = ktl.read('nsds', 'filename')
                wfeArgs = {'sv': 's'}
                WaitForExposure.execute(wfeArgs, logger, cfg)
                nFrames = nFrames - 1
                if (nFrames>0):
                    logger.info(f'Took file {fileName}, {nFrames} left')
                    time.sleep(1)
        else:
            fileName = ktl.read('nsds', 'filename')
            logger.info(f'File {fileName}')
            wfeArgs = {'sv': 's'}
            WaitForExposure.execute(wfeArgs, logger, cfg)
            cls._write_to_ktl('nsds', 'GO', 0, logger, cfg, True)
            
        Popen(["ssh", "nireseng@niresserver1", "power", "off", "8"])
        cls._write_to_ktl('nsds', 'obstype', 'object', logger, cfg)
        

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):
        pass

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass