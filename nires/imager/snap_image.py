"""
Takes a target/sky subtracted image

Replaces:
snapi
"""

from astropy.io import fits
import os
from datetime import datetime

from NIRESTranslatorFunction import NIRESTranslatorFunction

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
        # Get lastfile
        # Offset
        # Take sky frame
        # Get lastfile
        # Use the lastfiles to generate subtracted image, save to tempdri
        pass

    @classmethod
    def post_condition(cls, args, logger, cfg):
        pass

    def subtract_fits(cls, file1, file2, outfile):
        with fits.open(file1) as f1:
            with fits.open(file2) as f2:
                outdata = f1[0].data - f2[0].data
                hdu = fits.PrimaryHDU(outdata)
                hdu.writeto(outfile, overwrite=True)

