"""
Waits for exposure to finish (blocking)

Arguments:
- sv (required, enum(s, v, sv) )

Replaces:
wfg(s/v)
"""
import pdb
try:
    import ktl
except ImportError:
    ktl=""
import time

from nires.NIRESTranslatorFunction import NIRESTranslatorFunction

class WaitForExposure(NIRESTranslatorFunction):

    @classmethod
    def wait_for_exposure(cls, sv, logger, cfg):
        """Waits for an exposure to finsih on either
        the H2RG detector (spectrograph) or 
        H1 imaging detector

        Args:
            sv (int): spec 's' or imager 'v'
            logger (class): Logger object
            cfg (class): cfg object
        """
        service = cls._determine_nires_service(sv)
        itime = float(ktl.read(service, 'itime'))
        coadds = int(ktl.read(service, 'coadds'))
        nread = int(ktl.read(service, 'numreads'))
        waitForEndReads = float(cfg['ob_keys']['n_read_padding']) * nread
        extra = float(cfg['ob_keys']['extra_wait']) # add some extra to "wait" to allow for miscalculations
        wait = int(itime) * waitForEndReads * int(coadds) + extra

        logger.info(f'wait_for_exposure: Time estimate: {wait} seconds (includes {extra} seconds for overhead)')

        logger.info('wait_for_exposure: Waiting for exposure to end.')
        count = 0
        imageDone = int(ktl.read(service, 'imagedone'))

        logPeriod = cfg['logger']['ping_period']
        sleepLength = cfg['exposure']['sleep_length']
        countPeriod = int(logPeriod) / int(sleepLength)
        while (imageDone != 1) and (count <= wait):
            count = count + 1
            time.sleep(sleepLength)
            imageDone = int(ktl.read(service, 'imagedone'))
            if countPeriod % count == 0:
                percComplete = round( 100 * count * sleepLength / wait )
                timeRemaining = wait - count * sleepLength
                logger.info(f'exposure {percComplete}% completed. Time remaining: {timeRemaining}')
        if imageDone: logger.info('image done: OK')
        else:
            logger.info('wait_for_exposure: exposure timed out.')
        return wait
        

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        pass

    @classmethod
    def perform(cls, args, logger, cfg):

        sv = args['sv']
        cls.wait_for_exposure(sv, logger, cfg)

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass