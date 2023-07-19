import ktl

from nires.NIRESTranslatorFunction import NIRESTranslatorFunction
from nires.shared.set_detector_configuration import SetDetectorConfig 


class configure_science(NIRESTranslatorFunction):
    '''
    '''

    @classmethod
    def set_detector_config(cls, args, logger, cfg, sv):
        sequence = args.get('sequence')
        params = sequence.get('parameters')
        nFrames = params.get('det_exp_number')
        coadds = params.get('det_coadd_number')
        itime = params.get('det_exp_time')
        readoutMode = params.get('det_samp_mode')
        readPairs = params.get('det_exp_read_pairs')
        nSamp = params.get('det_num_fs')
        args = {
            'nFrames': nFrames,
            'itime': itime,
            'coadds': coadds,
            'readoutMode': readoutMode,
            'numreads': readPairs,
            'nSamp': nSamp,
            'sv': sv
        }

        SetDetectorConfig.execute(args, logger, cfg)


    @classmethod
    def pre_condition(cls, args, logger, cfg):
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        sequence = args.get('sequence')
        params = sequence.get('parameters')
        detType = params.get('det_type_mode')

        if 'spectrograph' in detType.lower():
            cls.set_detector_config(args, logger, cfg, 's')
        elif 'imager' in detType.lower():
            cls.set_detector_config(args, logger, cfg, 'v')
        elif 'both' in detType.lower():
            cls.set_detector_config(args, logger, cfg, 's')
            cls.set_detector_config(args, logger, cfg, 'v')
        else:
            logger.error(f'det_type_mode value {detType} not Spectrograph, Imager, or Both')
            raise(f'det_type_mode value {detType} not Spectrograph, Imager, or Both')
        
        


    @classmethod
    def post_condition(cls, args, logger, cfg):
        return True
