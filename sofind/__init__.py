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
        
        # first get the datamodel dictionary
        if not config_name.endswith('.yaml'):
            config_name += '.yaml'
        basename = f'datamodels/{config_name}'
        datamodel_fn = utils.get_package_fn('sofind', basename)
        datamodel_dict = utils.config_from_yaml_file(datamodel_fn)

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
        dm_kwargs['configs'] = {}
        for product in datamodel_dict:
            dm_kwargs[product] = {}
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
                            f'subproduct {subproduct} (config {subproduct_config})'
                except TypeError as e:
                    raise AssertionError(
                         f'No allowed_qids_configs for product {product}, subproduct {subproduct} '
                         f'(config {subproduct_config})') from e

                # if compatible, add to the dm_kwargs. also add config name for the record
                dm_kwargs[product][subproduct] = subproduct_dict
                dm_kwargs['configs'][product][subproduct] = subproduct_config

        return cls(os.path.splitext(config_name)[0], **dm_kwargs)

    @classmethod
    def from_productdb(cls, config_name):
        raise NotImplementedError("Not yet connected to productdb")