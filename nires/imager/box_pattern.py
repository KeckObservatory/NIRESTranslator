"""
Takes a box dither pattern in SKY COORDINATES

Arguments:
- num_pos (required, enum(4, 5, 8, 9) )
- x (required, float)
- y (required, float)

Replaces:
box(4,5,8,9)
"""

from NIRESTranslatorFunction import NIRESTranslatorFunction
from en import en
from mxy import mxy
from MarkBase import MarkBase
from shared.take_exposures import TakeExposures

import ktl

from astropy.coordinates import SkyCoord
from astropy import units as u


class BoxPattern(NIRESTranslatorFunction):

    known_patterns = {
        "box4" : {
            "lateral" : [1, -2, 0, 2, -1],
            "vertical" : [1, 0, -2, 0, 1]
        },
        "box5" : {
            "lateral" : [0, 1, -2, 0, 2, -1],
            "vertical" : [0, 1, 0, -2, 0, 1]
        },
        "box8" : {
            "lateral" : [1, 0, -2, 0, 2, -2, 1, 0, 0],
            "vertical" : [-1, 2, -2, 2, -1, 0, -1, 2, -1]
        },
        "box9" : {
            "lateral" : [0, 1, 0, -2, 0, 2, -2, 1, 0, 0],
            "vertical" : [0, -1, 2, -2, 2, -1, 0, -1, 2, -1]
        }
    }

    @classmethod
    def pre_condition(cls, args, logger, cfg):
        if args['pattern'] not in cls.known_patterns.keys():
            logger.error("Unknown pattern entered.")
            raise ValueError

        raStr = ktl.read('dcs2', 'ra')
        decStr = ktl.read('dcs2', 'dec')
        coords = SkyCoord(ra = raStr, dec = decStr, unit=(u.hourangle, u.deg))
        
        starting_pos = { 'ra': coords.ra.degree, 'dec': coords.dec.degree}
        args['starting_pos'] = starting_pos
        return args

    @classmethod
    def perform(cls, args, logger, cfg):
        if args['coord_frame'] == 'en':
            frame = "RA/DEC"
        elif args['coord_frame'] == 'det':
            frame = "Detector"
        for i in range(args['num_repeats']):
            logger.info(f"Executing box pattern {i}/{args['num_repeats']}")
            logger.info(f"Box pattern will be in {frame} space.")
            cls.execute_box(args['offset'], args['pattern'], args['coord_frame'])

    @classmethod
    def post_condition(cls, args, logger, cfg):
        
        raStr = ktl.read('dcs2', 'ra')
        decStr = ktl.read('dcs2', 'dec')
        end_coords = SkyCoord(ra=raStr, dec=decStr, unit=(u.hourangle, u.deg))
        dra = end_coords.ra.degree - args['starting_pos']['ra']
        ddec = end_coords.dec.degree - args['starting_pos']['dec']
        ditherDelta = float(cfg['dither_delta']['dither_delta'])
        logger.info(f"Dither complete. dra:ddec={dra}:{ddec}")
        if dra > ditherDelta  or ddec > ditherDelta:
            logger.error(f"Dither did not return to starting position {args['starting_pos']['ra']}:{args['starting_pos']['dec']}")
        return args

    @classmethod
    def execute_box(cls, offset, pattern, coord):
        for i in range(len(pattern)):
            if coord == 'en':
                en.execute(pattern['lateral'] * offset, pattern['vertical'] * offset)
            elif coord == 'det':
                mxy.execute({'x' : pattern['lateral'] * offset, 'y' : pattern['vertical'] * offset})
            TakeExposures.execute({'nFrames' : 1, 'sv' : 'v'})
