try:
    import ktl
except ImportError as err:
    ktl = ""

from nires.NiresTranslatorFunction import NiresTranslatorFunction


class waitfor_configure_science(NiresTranslatorFunction):
    '''
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        return True

    @classmethod
    def _wait_for_params(cls, args, logger, cfg, sv):
        service = cls._determine_nires_service(sv)
        for key, val in args.get('wait_for_params', {}).items():
            ktl.wait(f'${service}.{key}={val}', timeout=2)


    @classmethod
    def perform(cls, args, logger, cfg):
        sequence = args.get('sequence')
        params = sequence.get('parameters')
        detType = params.get('det_type_mode')

        coadds = params.get('det_exp_number')
        itime = params.get('det_exp_time')
        sampmode = params.get('det_samp_mode')
        numreads = params.get('det_exp_read_pairs')
        numfs = params.get('det_num_fs')

        waitforparams = {'coadds': coadds, 'sampmode': sampmode, 'itime': itime}
        if 'MCDS' in sampmode:
            waitforparams['numfs'] = numfs 
        else:
            waitforparams['numreads'] = numreads 
        args['wait_for_params'] = waitforparams 

        if 'spectrograph' in detType.lower():
            cls._wait_for_params(args, logger, cfg, 's')
        elif 'imager' in detType.lower():
            cls._wait_for_params(args, logger, cfg, 's')
        elif 'both' in detType.lower():
            cls._wait_for_params(args, logger, cfg, 's')
            cls._wait_for_params(args, logger, cfg, 's')
        else:
            logger.error(f'det_type_mode value {detType} not Spectrograph, Imager, or Both')
            raise(f'det_type_mode value {detType} not Spectrograph, Imager, or Both')
        raise NotImplementedError()

    @classmethod
    def post_condition(cls, args, logger, cfg):
        return True
