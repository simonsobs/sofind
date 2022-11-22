from actapack import utils
from actapack.products import Product

import os

class DataModel(*Product.__subclasses__()):

    def __init__(self, **kwargs):
        """A wrapper class that mixes in all Product subclasses. Also grabs any
        qid-related information to be used in subclass methods, e.g., if a
        product's filenames are labeled by particular array, frequency, etc.

        Notes
        -----
        This class is the only class a user should need. It exposes all product
        methods implemented in this repo.
        """
        super().__init__(**kwargs)

    @classmethod
    def from_config(cls, config_name):
        """Build a DataModel instance from configuration files distributed in
        the actapack package.

        Parameters
        ----------
        config_name : str
            The name of the configuration file. If does not end in '.yaml', 
            '.yaml' will be appended.

        Returns
        -------
        DataModel
            Instance corresponding to the collection of products and subroducts
            indicated in the named configuration file.

        Raises
        ------
        KeyError
            If a subproduct in a user's .actapack_config.yaml file is not a
            member the datamodel's product type.
        """
        dm_kwargs = {}

        # first get the system paths
        actapack_fn = os.path.join(os.environ['HOME'], '.actapack_config.yaml')
        actapack_config = utils.config_from_yaml_file(actapack_fn)
        system_path_dict = actapack_config[os.path.splitext(config_name)[0]]
        dm_kwargs.update(system_path_dict)
        
        # then get the datamodel dictionary
        if not config_name.endswith('.yaml'):
            config_name += '.yaml'
        basename = f'configs/datamodels/{config_name}'
        datamodel_fn = utils.get_package_fn('actapack', basename)
        datamodel_dict = utils.config_from_yaml_file(datamodel_fn)

        # get the product dicts
        # need to iterate over lists because dm_kwargs updated during iteration
        for product_name in list(dm_kwargs):
            for subproduct_name in list(dm_kwargs[product_name]):
                # default_path --> default_dict
                subproduct_name = subproduct_name.split('_path')[0]
                subproduct_name = f'{subproduct_name}_dict'

                # the actual config basename
                try:
                    subproduct_dict = datamodel_dict[product_name][subproduct_name]
                except KeyError:
                    raise KeyError(
                        f'Product {product_name}, subproduct {subproduct_name} '
                        'not in datamodel configuration file'
                    )
                if not subproduct_dict.endswith('.yaml'):
                    subproduct_dict += '.yaml'

                # the actual config full filename
                basename = f'configs/products/{product_name}/{subproduct_dict}'
                subproduct_fn = utils.get_package_fn('actapack', basename)

                # the contents of the filename
                subproduct_dict = utils.config_from_yaml_file(subproduct_fn)

                # dm_kwargs already populated by the system_path_dict
                dm_kwargs[product_name].update({f'{subproduct_name}': subproduct_dict})
        
        # add the qids
        qids_name = datamodel_dict['qids_dict']
        if not qids_name.endswith('.yaml'):
            qids_name += '.yaml'
        basename = f'configs/qids/{qids_name}'
        qids_fn = utils.get_package_fn('actapack', basename)
        qids_dict = utils.config_from_yaml_file(qids_fn)
        dm_kwargs.update(qids_dict=qids_dict)

        return cls(**dm_kwargs)

    @classmethod
    def from_productdb(cls, config_name):
        raise NotImplementedError("Not yet connected to productdb")