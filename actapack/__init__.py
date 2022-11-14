from actapack import utils
from actapack.products import Product

import os

class DataModel(*Product.__subclasses__()):

    def __init__(self, qid_dict, **kwargs):
        self.qid_dict = qid_dict
        super().__init__(**kwargs)

    @classmethod
    def from_config(cls, config_name):
        dm_kwargs = {}
        
        # first get the config dictionary
        if not config_name.endswith('.yaml'):
            config_name += '.yaml'
        basename = f'configs/datamodel_configs/{config_name}'
        config_fn = utils.get_package_fn('actapack', basename)
        config_dict = utils.config_from_yaml_file(config_fn)

        # then get the system paths
        actapack_fn = os.path.join(os.environ['HOME'], '.actapack_config.yaml')
        actapack_config = utils.config_from_yaml_file(actapack_fn)
        system_path_dict = actapack_config[os.path.splitext(config_name)[0]]
        dm_kwargs.update(system_path_dict)

        # then get the qid dict
        qid_dict = config_dict.pop('qid_dict')
        if isinstance(qid_dict, str):
            if not qid_dict.endswith('.yaml'):
                qid_dict += '.yaml'
            basename = f'configs/qid_configs/{qid_dict}'
            qid_fn = utils.get_package_fn('actapack', basename)
            qid_dict = utils.config_from_yaml_file(qid_fn)
        dm_kwargs.update(dict(qid_dict=qid_dict))

        # finally get the product dicts
        for dict_name, product_dict in config_dict.items():
            if isinstance(product_dict, str):
                if not product_dict.endswith('.yaml'):
                    product_dict += '.yaml'
                subdir = dict_name.split('_')[0]
                basename = f'configs/product_configs/{subdir}/{product_dict}'
                product_fn = utils.get_package_fn('actapack', basename)
                product_dict = utils.config_from_yaml_file(product_fn)
            dm_kwargs.update({f'{dict_name}': product_dict})

        return cls(**dm_kwargs)

    @classmethod
    def from_productdb(cls, config_name):
        raise NotImplementedError("Not yet connected to productdb")