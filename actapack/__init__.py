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
        methods implemented in this package.
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
            Instance corresponding to the collection of products and subproducts
            indicated in the named configuration file.
        """
        dm_kwargs = {}
        
        # first get the datamodel dictionary and system path dictionary
        if not config_name.endswith('.yaml'):
            config_name += '.yaml'
        basename = f'datamodels/{config_name}'
        datamodel_fn = utils.get_package_fn('actapack', basename)
        datamodel_dict = utils.config_from_yaml_file(datamodel_fn)

        actapack_fn = os.path.join(os.environ['HOME'], '.actapack_config.yaml')
        actapack_config = utils.config_from_yaml_file(actapack_fn)
        system_path_dict = actapack_config[os.path.splitext(config_name)[0]]

        # evaluate the (sub)product dicts and add in the system paths.
        # handle special case of qids_dict separately
        for product_name in datamodel_dict:

            if product_name == 'qids_dict':
                # qids_name: the config basename
                qids_name = datamodel_dict[product_name]
                if not qids_name.endswith('.yaml'):
                    qids_name += '.yaml'

                # qids_fn: the actual config full filename
                basename = f'qids/{qids_name}'
                qids_fn = utils.get_package_fn('actapack', basename)

                # qids_dict: the contents of the filename
                qids_dict = utils.config_from_yaml_file(qids_fn)
                dm_kwargs[product_name] = qids_dict
            else:
                dm_kwargs[product_name] = {}
                for subproduct_name, subproduct_dict in datamodel_dict[product_name].items():
                    # subproduct_dict: the config basename
                    if not subproduct_dict.endswith('.yaml'):
                        subproduct_dict += '.yaml'

                    # subproduct_fn: the actual config full filename
                    basename = f'products/{product_name}/{subproduct_dict}'
                    subproduct_fn = utils.get_package_fn('actapack', basename)

                    # subproduct_dict: the contents of the filename
                    subproduct_dict = utils.config_from_yaml_file(subproduct_fn)
                    dm_kwargs[product_name][subproduct_name] = subproduct_dict

                    # default_dict --> default_path
                    subproduct_name = subproduct_name.split('_dict')[0]
                    subproduct_name = f'{subproduct_name}_path'

                    # if in user .actapack_config.yaml file, add subproduct path
                    if product_name in system_path_dict:
                        if subproduct_name in system_path_dict[product_name]:
                            subproduct_path = system_path_dict[product_name][subproduct_name]
                            dm_kwargs[product_name][subproduct_name] = subproduct_path

        return cls(**dm_kwargs)

    @classmethod
    def from_productdb(cls, config_name):
        raise NotImplementedError("Not yet connected to productdb")