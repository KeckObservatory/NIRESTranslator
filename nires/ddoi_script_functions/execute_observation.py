import ktl

from nires.shared.take_exposures import TakeExposures as te 
from nires.spectrograph.dither import Dither
from nires.calibration.take_arcs import TakeArcs
from nires.calibration.take_darks import TakeDarks
from nires.calibration.take_flats import TakeFlats
from nires.calibration.take_flats_on_off import TakeFlatsOnOff
from nires.NIRESTranslatorFunction import NIRESTranslatorFunction


class execute_observation(NIRESTranslatorFunction):
    '''
    '''

    @classmethod
    def determine_spec_or_imager(cls, detType, logger):
        if 'spectrograph' in detType.lower():
            sv = 's'
        elif 'imager' in detType.lower():
            sv = 'v'
        elif 'both' in detType.lower():
            sv = 'sv'
        else:
            logger.error(f'det_type_mode value {detType} not Spectrograph, Imager, or Both')
            raise(f'det_type_mode value {detType} not Spectrograph, Imager, or Both')
        return sv
        

    @classmethod
    def single_exposure(cls, args, logger, cfg):
        sequence = args.get('sequence')
        params = sequence.get('parameters')
        nFrames = params.get('det_exp_number')
        detType = params.get('det_type_mode')
        sv = cls.determine_spec_or_imager(detType, logger)

        args = {
            'nFrames': nFrames,
            'sv': sv
        }
        te.execute(args, logger, cfg)

    @classmethod
    def dither_exposure(cls, args, logger, cfg):
        sequence = args.get('sequence')
        params = sequence.get('parameters')
        offset = params.get('sequence_dither_offset')
        pattern = params.get('sequence_dither_type')
        detType = params.get('det_type_mode')
        sv = cls.determine_spec_or_imager(detType, logger)
        ditherArgs = {'pattern': pattern, 'offset': offset, 'sv': sv}
        Dither.execute(ditherArgs, logger, cfg)


    @classmethod
    def pre_condition(cls, args, logger, cfg):
        return True

    @classmethod
    def perform(cls, args, logger, cfg):

        sequence = args.get('sequence')
        metadata = sequence.get('metadata')
        seq_num = metadata.get('sequence_number')
        logger.info(f'excuting observation for seq {seq_num}')
        seqName = metadata.get('name')

        if 'nires_stare_sci' in seqName:
            cls.single_exposure(args, logger, cfg)
        elif 'nires_dither_sci' in seqName:
            cls.dither_exposure(args, logger, cfg)
        elif 'nires_slit_scan_sci' in seqName:
            raise NotImplementedError
        elif 'nires_cals' in seqName:
            parameters = sequence.get('parameters')
            calType = parameters.get('det_cal_type')

            nFrames = parameters.get('det_exp_number')
            args = {
                'nFrames': nFrames,
            }
            if 'arcs' in calType.lower():
                TakeArcs.execute(args, logger, cfg)
            elif 'darks' in calType.lower():
                TakeDarks.execute(args, logger, cfg)
            elif 'flats on flats off' in calType.lower():
                TakeFlatsOnOff.execute(args, logger, cfg)
            elif 'flats' == calType.lower():
                TakeFlats.execute(args, logger, cfg)
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError
            
    @classmethod
    def post_condition(cls, args, logger, cfg):
        return True
