"""
Takes a target/sky subtracted image

Replaces:
snapi
"""

from astropy.io import fits
import os
import shutil
from datetime import datetime

from NIRESTranslatorFunction import NIRESTranslatorFunction
from nires.shared.take_exposures import TakeExposures
from nires.shared.wait_for_exposure import WaitForExposure

try:
    import ktl
except ImportError:
    ktl = ''

class SnapImage(NIRESTranslatorFunction):

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        # Check if we are able to read/write to sdata
        date_dir = datetime.today().strftime("%y%b%d").lower()
        if not os.path.exists(f"{cfg['sdata_path']}/{date_dir}"):
            pass
        return

    @classmethod
    def perform(cls, args, logger, cfg):

        # Take object frame
        cls._write_to_ktl('nids', 'comment', 'Object image for snapi', logger, cfg)
        TakeExposures.execute({'nFrames' : 1, 'sv' : 'v'})
        WaitForExposure.execute({'sv' : 'v'})
        # Get lastfile
        object_file = ktl.read('nids', 'lastfile')
        shutil.copyfile(object_file, cfg['image_display']['object_temp_path'])
        os.chmod(cfg['image_display']['object_temp_path'], 666)

        # Offset

        nod_east = ktl.read('nires', 'node')
        nod_north = ktl.read('nires', 'nodn')
        cls._write_to_ktl('dcs', 'raoff', nod_east, logger, cfg)
        cls._write_to_ktl('dcs', 'decoff', nod_north, logger, cfg)
        cls._write_to_ktl('dcs', 'rel2curr', 't', logger, cfg)
        cls.wait_for_tel(cfg, logger)


        # Take sky frame
        cls._write_to_ktl('nids', 'comment', 'Sky image for snapi', logger, cfg)
        TakeExposures.execute({'nFrames' : 1, 'sv' : 'v'})
        WaitForExposure.execute({'sv' : 'v'})
        # Get lastfile
        sky_file = ktl.read('nids', 'lastfile')
        shutil.copyfile(sky_file, cfg['image_display']['sky_temp_path'])
        os.chmod(cfg['image_display']['sky_temp_path'], 666)
        # Use the lastfiles to generate subtracted image, save to tempdr
        cls.subtract_fits(cfg['image_display']['object_temp_path'], cfg['image_display']['sky_temp_path'])

        # move back
        nod_east = ktl.read('nires', 'node') * -1
        nod_north = ktl.read('nires', 'nodn') * -1
        cls._write_to_ktl('dcs', 'raoff', nod_east, logger, cfg)
        cls._write_to_ktl('dcs', 'decoff', nod_north, logger, cfg)
        cls._write_to_ktl('dcs', 'rel2curr', 't', logger, cfg)
        cls.wait_for_tel(cfg, logger)

        cls.display_subtracted_image(cfg['image_display']['object_temp_path'], cfg['image_display']['sky_temp_path'], cfg, logger)


    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass

    def display_subtracted_image(cls, file1, file2, cfg, logger, outfile=None):

        if outfile == None:
            outfile = cfg['image_display']['default_snapi']

        with fits.open(file1) as f1:
            with fits.open(file2) as f2:
                outdata = f1[0].data - f2[0].data
                # Overwrite f1's header info with the subtracted data and save it
                # We cannot create a new HDU, since we need the headers.
                f1[0].data = outdata
                f1.writeto(outfile, overwrite=True)
                os.chmod(outfile, 666)
                cls.send_fits_to_display(outfile, logger, cfg)

        

