from ..products import Product, get_implements_decorator

from mnms import io

import os


class NoiseModel(Product):

    implementedmethods = []
    implements = get_implements_decorator(implementedmethods)
    
    def __init__(self, **kwargs):
        self.set_attrs(__name__, kwargs)
        super().__init__(**kwargs)

    @implements(Product.get_fn)
    def get_noise_fn(self, noise_model_name, *qids, which='sims',
                     subproduct='default', alm=False, basename=False, 
                     **kwargs):
        subprod_dict = self.get_subproduct_dict(__name__, subproduct)
        param_dict = subprod_dict[noise_model_name]

        # check compatibility with data model and parent product/subproduct
        # (e.g., maps)
        data_model_name = os.path.splitext(param_dict['data_model_name'])[0]
        assert data_model_name == self.name, \
            f'Inconsistent data_model_name: {data_model_name} and {self.name}'
        subproduct_from_config = param_dict['subproduct']
        assert subproduct_from_config == subproduct, \
            f'Inconsistent subproduct: {subproduct_from_config} and {subproduct}'
        
        parent_product, parent_subproduct = param_dict['maps_product'], param_dict['maps_subproduct']
        parent_subprod_dict = self.get_subproduct_dict(
            parent_product, parent_subproduct
            )
        self.check_subproduct_config_is_subset(
            __name__, subproduct, subprod_dict, parent_product,
            parent_subproduct, parent_subprod_dict
            )

        # param_dict is deepcopy :) also _noise_model_class now lives in the object
        # as a class attribute
        nm_cls = param_dict.pop('noise_model_class') 
        ioobj = io.BaseIO.get_subclass(nm_cls)(**param_dict)
        
        # don't worry about updating param_dict because ioobj only in this scope
        param_dict = ioobj.param_formatted_dict 
        model_file_template = param_dict['model_file_template']
        sim_file_template = param_dict['sim_file_template']
        qid_names_template = param_dict['qid_names_template']
        param_dict.update(
            config_name=os.path.splitext(
                self.get_subproduct_config(__name__, subproduct)
                )[0],
            noise_model_name=noise_model_name,
            qids='_'.join(qids),
            qid_names=self.get_qid_names_by_subproduct(
                __name__, subproduct, *qids, qid_names_template=qid_names_template
            ),
            **self.get_equal_qid_kwargs_by_subproduct(
                __name__, subproduct, *qids
            ),
            alm_str='alm' if alm else 'map',
            **kwargs
        )

        # only sims or models supported
        if which == 'sims':
            fn = sim_file_template.format(**param_dict)
            if not fn.endswith('.fits'): 
                fn += '.fits'
        elif which == 'models':
            fn = model_file_template.format(**param_dict)
            if not fn.endswith('.hdf5'):
                fn += '.hdf5'        
        else:
            raise ValueError(f"which must be 'sims' or 'models', got {which}")

        if basename:
            return fn
        else:
            subprod_path = self.get_subproduct_path(__name__, subproduct)
            return os.path.join(subprod_path, which, fn)

    @implements(Product.read_product)
    def read_noise(self, noise_model_name, *qids, which='sims',
                   subproduct='default', alm=False, read_noise_kwargs=None,
                   **kwargs):
        subprod_dict = self.get_subproduct_dict(__name__, subproduct)
        param_dict = subprod_dict[noise_model_name]

        nm_cls = param_dict.pop('noise_model_class') # param_dict is deepcopy :)
        ioobj = io.BaseIO.get_subclass(nm_cls)(**param_dict)
    
        fn = self.get_noise_fn(
            noise_model_name, *qids, which=which, subproduct=subproduct,
            alm=alm, basename=False, **kwargs
            )
        
        if read_noise_kwargs is None:
            read_noise_kwargs = {}

        # only sims or models supported
        if which == 'sims':
            return ioobj.read_sim(fn, alm=alm, **read_noise_kwargs) 
        elif which == 'models':
            return ioobj.read_model(fn, **read_noise_kwargs)
        else:
            raise ValueError(f"which must be 'sims' or 'models', got {which}")