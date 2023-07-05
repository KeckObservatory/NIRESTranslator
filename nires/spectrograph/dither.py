"""
Takes an arbitrary dither pattern along the slit

Arguments:
- pattern (required, string)
- offsets (required, float)
- num repeats

Replaces:
abba
sp(2,3,5,7)

Precondition:
if len(pattern) != len(offsets), complain
if dither_pattern_stops * offset > slit length, complain

Perform:

Postcondition:
if end location != current location, our dither failed

Set the detector configuration
- tint
- nsamps
- sampmode
- coadds

Decode the dither pattern:
    Loop over the string char by char, making a dict entry for each spot
    Create an offset/exp list to execute

do that list num_repeats times

"""

# TODO: Update args keys to match OB keys


from TelescopeTranslator.SlitMove import SlitMove
from TelescopeTranslator.MarkBase import MarkBase
from shared.take_exposures import TakeExposures

from NIRESTranslatorFunction import NIRESTranslatorFunction

class Dither(NIRESTranslatorFunction):

    known_dithers = {
        """Stores the known dither patterns (could be in cfg?)
        Format is:
        pattern_name : {
            "offsets" : list of offsets to apply AFTER each frame
        }
        
        The last number must be the return move, that is, it should return the
        telescope to where we started (sum(pattern[:-1]) == -1*pattern[-1]). 
        Also expressable as sum(pattern) = 0

        For example, sp5 will do the following:

        Take a 

        """
        "sp2" : {
            "offsets" : [0, 1, -1],
        },
        "sp3" : {
            "offsets" : [0, 1, -2, 1]
        },
        "sp5" : {
            "offsets" : [0, 2, -3, 2, -3, 2]
        },
        "sp7" : {
            "offsets" : [0, 2, -4, 5, -4, 2, -4, 3]
        },
        "ABBA" : {
            "offsets" : [0, -1, 0, 1, 0]
        },
        "AB" : {
            "offsets" : [0, 1, -1]
        }
    }

    @classmethod
    def pre_condition(cls, args, logger, cfg):

        if args['pattern'] not in cls.known_dithers.keys():
            logger.error("Unknown pattern entered.")
            raise ValueError

        net_move = sum(args.pattern[:-1]) + args.pattern[-1]

        # Raise an error if the whole pattern leaves the telescope in a new position
        if net_move != 0:
            net_offset = net_move * args.offset
            logger.error(f"Invalid pattern: {','.join(args.pattern)} results in offset of {net_offset} arcseconds!")
            raise ValueError
        
        # Raise a warning if the total range > slit length
        min = 0
        max = 0
        absolute_location = 0
        for location in args.pattern:
            absolute_location += location
            if absolute_location > max   : max = absolute_location
            elif absolute_location < min : min = absolute_location
        total_range = (max - min) * args.offset
        if total_range > cfg.slit_length:
            logger.warning(f"Target will not always be in slit.")
        pass

        starting_pos = MarkBase() # This isn't actually mark base -> need to add?
        args.starting_pos = starting_pos
        return args

    @classmethod
    def perform(cls, args, logger, cfg):
        cls.execute_dither(args['offset'], args['pattern'])

    @classmethod
    def post_condition(cls, args, logger, cfg):

        current_location = MarkBase()
        if current_location.ra - args.starting_pos.ra > cfg['dither_delta'] or current_location.dec - args.starting_pos.dec > cfg['dither_delta']:
            logger.error(f"Dither did not return to starting position of {args.starting_pos.ra}:{args.starting_pos.dec}")
        return args

    @classmethod
    def execute_dither(cls, offset, pattern):

        for location in pattern:
            local_offset = location * offset # How far to move this time
            SlitMove(local_offset)
            TakeExposures(1)

        reset_offset = sum(pattern) * offset * -1 # How far to get back to where we started
        SlitMove(reset_offset)

