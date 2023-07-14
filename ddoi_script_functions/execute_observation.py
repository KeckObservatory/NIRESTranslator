import ktl

from nires.shared.take_exposures import TakeExposures as te 
from nires.calibration.take_arcs import TakeArcs
from ddoitranslatormodule.KPFTranslatorFunction import KPFTranslatorFunction


class ExecuteObservation(KPFTranslatorFunction):
    '''
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        return True

    @classmethod
    def single_exposure(cls, args, logger, cfg):

        sequence = args.get('sequence')
        params = sequence.get('parameters')
        nFrames = params.get('det_exp_number')
        detType = params.get('det_type_mode')

        if 'spectrograph' in detType.lower():
            sv = 's'
        elif 'imager' in detType.lower():
            sv = 'v'
        elif 'both' in detType.lower():
            sv = 'sv'
        else:
            logger.error(f'det_type_mode value {detType} not Spectrograph, Imager, or Both')
            raise(f'det_type_mode value {detType} not Spectrograph, Imager, or Both')

        args = {
            'nFrames': nFrames,
            'sv': sv
        }
        te.execute(args, logger, cfg)

    @classmethod
    def arcs_exposure(cls, args, logger, cfg):

        sequence = args.get('sequence')
        params = sequence.get('parameters')
        nFrames = params.get('det_exp_number')
        args = {
            'nFrames': nFrames,
            'manuel': False 
        }
        TakeArcs.execute(args, logger, cfg)

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
            raise NotImplementedError 
        elif 'nires_arcs' in seqName:
            cls.arcs_exposure(args, logger, cfg)
        else:
            raise NotImplementedError
            
        


    @classmethod
    def post_condition(cls, args, logger, cfg):
        return True
