from sofind import utils
from sofind.products import Product

import os


class DataModel(*Product.__subclasses__()):

    def __init__(self, name, **kwargs):
        """A wrapper class that mixes in all Product subclasses. Also grabs any
        qid-related information to be used in subclass methods, e.g., if a
        product's filenames are labeled by particular array, frequency, etc.

        Parameters
        ----------
        name : str
            Name of the DataModel instance.

        Notes
        -----
        This class is the only class a user should need. It exposes all product
        methods implemented in this package.
        """
        super().__init__(**kwargs)

        self._name = name

    @property
    def name(self):
        return self._name

    @classmethod
    def from_config(cls, config_name):
        """Build a DataModel instance from configuration files distributed in
        the sofind package.

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

        Raises
        ------
        AssertionError
            If the qids_config for the data model is not allowed by a
            subproduct in the data model.
        """
        dm_kwargs = {}
        
        # first get the datamodel dictionary and system path dictionary
        if not config_name.endswith('.yaml'):
            config_name += '.yaml'
        basename = f'datamodels/{config_name}'
        datamodel_fn = utils.get_package_fn('sofind', basename)
        datamodel_dict = utils.config_from_yaml_file(datamodel_fn)

        sofind_fn = os.path.join(os.environ['HOME'], '.sofind_config.yaml')
        sofind_config = utils.config_from_yaml_file(sofind_fn)
        system_path_dict = sofind_config[os.path.splitext(config_name)[0]]

        # evaluate the (sub)product dicts and add in the system paths.
        # handle special case of qids_dict separately

        # qids_config: the config basename
        qids_config = datamodel_dict.pop('qids_config')
        if not qids_config.endswith('.yaml'):
            qids_config += '.yaml'

        # qids_fn: the actual config full filename
        basename = f'qids/{qids_config}'
        qids_fn = utils.get_package_fn('sofind', basename)

        # qids_dict: the contents of the filename
        qids_dict = utils.config_from_yaml_file(qids_fn)
        dm_kwargs['qids'] = qids_dict

        # next get the paths, configs, and config info
        dm_kwargs['paths'] = {}
        dm_kwargs['configs'] = {}
        for product in datamodel_dict:
            dm_kwargs[product] = {}
            dm_kwargs['paths'][product] = {}
            dm_kwargs['configs'][product] = {}
            for subproduct, subproduct_config in datamodel_dict[product].items():
                # subproduct_config: the config basename
                if not subproduct_config.endswith('.yaml'):
                    subproduct_config += '.yaml'

                # subproduct_fn: the actual config full filename
                basename = f'products/{product}/{subproduct_config}'
                subproduct_fn = utils.get_package_fn('sofind', basename)

                # subproduct_dict: the contents of the filename
                subproduct_dict = utils.config_from_yaml_file(subproduct_fn)

                # NOTE: check for compatibility of this subproduct with the
                # data_model, meaning the requested qids_dict is allowed
                subproduct = subproduct.split('_config')[0] # remove _config

                try:
                    if qids_config not in subproduct_dict['allowed_qids_configs']:
                        assert subproduct_dict['allowed_qids_configs'] == 'all', \
                            f'qids_config {qids_config} not allowed by product {product}, ' + \
                            f'subproduct {subproduct} configuration file'
                except TypeError as e:
                    raise AssertionError(
                         f'No allowed_qids_configs for product {product}, subproduct {subproduct}'
                         ) from e

                # if compatible, add to the dm_kwargs. also add config name for the record
                dm_kwargs[product][subproduct] = subproduct_dict
                dm_kwargs['configs'][product][subproduct] = subproduct_config

                # if in user .sofind_config.yaml file, add subproduct path
                if product in system_path_dict:
                    if f'{subproduct}_path' in system_path_dict[product]:
                        subproduct_path = system_path_dict[product][f'{subproduct}_path']
                        dm_kwargs['paths'][product][subproduct] = subproduct_path

        return cls(os.path.splitext(config_name)[0], **dm_kwargs)

    @classmethod
    def from_productdb(cls, config_name):
        raise NotImplementedError("Not yet connected to productdb")