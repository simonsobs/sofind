from ..products import Product, get_implements_decorator
import numpy as np
import os
from pixell import enmap

class ClusterModel(Product):
    #################################
    ### DO NOT CHANGE THESE LINES ###
    implementedmethods = []
    implements = get_implements_decorator(implementedmethods)

    def __init__(self, **kwargs):
        self.set_attrs(__name__, kwargs)
        super().__init__(**kwargs)
        self.check_product_config_internal_consistency(__name__)
    #################################

    @implements(Product.get_fn)
    def get_cluster_model_fn(self, frequency='150', SNR=5, downgrade=2, subproduct='default',
                             basename=False, **kwargs):
        """
        Construct the file path for the cluster model based on the provided parameters.

        Args:
            frequency (str, optional): Frequency of observation (default '150').
            SNR (int, optional): Signal-to-noise ratio threshold (default 5).
            downgrade (int, optional): Downsampling level as an integer. This will be converted internally
                to a string in the format 'down{integer}' (default 2).
            subproduct (str, optional): Identifier for the subproduct (default 'default').
            basename (bool, optional): If True, returns only the filename instead of the full path (default False).
            **kwargs: Additional keyword arguments.

        Returns:
            str: The full file path to the cluster model, or just the filename if basename is True.
        """
        if not isinstance(downgrade, int):
            raise TypeError("downgrade must be an integer")
        downgrade_str = f"down{downgrade}"

        # Access the subproduct dictionary and retrieve the filename template
        subprod_dict = self.get_subproduct_dict(__name__, subproduct)
        fn_template = subprod_dict['cluster_fn_template']

        fn_kwargs = dict(frequency=frequency, SNR=SNR, downgrade=downgrade_str, **kwargs)
        fn = fn_template.format(**fn_kwargs)

        if basename:
            return fn
        else:
            subprod_path = self.get_subproduct_path(__name__, subproduct)
            return os.path.join(subprod_path, fn)

    @implements(Product.read_product)
    def read_cluster_model(self, frequency='150', SNR=5, downgrade=2, subproduct='default', 
                           loadtxt_kwargs=None, **kwargs):
        """
        Read and load the cluster model data from file.

        Args:
            frequency (str, optional): Frequency of observation (default '150').
            SNR (int, optional): Signal-to-noise ratio threshold (default 5).
            downgrade (int, optional): Downsampling level as an integer. This will be converted internally
                to a string in the format 'down{integer}' (default 2).
            subproduct (str, optional): Identifier for the subproduct (default 'default').
            loadtxt_kwargs (dict, optional): Additional keyword arguments for np.loadtxt (default None).
            **kwargs: Additional keyword arguments.

        Returns:
            np.ndarray: The loaded cluster model data.
        """
        fn = self.get_cluster_model_fn(frequency=frequency, SNR=SNR, downgrade=downgrade, 
                                       subproduct=subproduct, basename=False, **kwargs)

        if loadtxt_kwargs is None:
            loadtxt_kwargs = {}

        return enmap.read_map(fn, **loadtxt_kwargs)