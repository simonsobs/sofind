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

    # Feel free to add stuff here

    @implements(Product.get_fn)
    def get_cluster_model_fn(self, frequency='150', SNR=5, downgrade="down2", subproduct='default',
                             basename=False, **kwargs):
        """
        Generate the filename for the cluster model file based on the qid and other parameters.

        Parameters:
        - frequency (str): Frequency of observation (default: '150').
        - SNR (int): Signal-to-noise ratio threshold (default: 5).
        - downgrade (str): Downsampling level (default: 'down2').
        - subproduct (str): Subproduct identifier (default: 'default').
        - basename (bool): Whether to return only the filename (default: False).
        - kwargs: Additional keyword arguments.

        Returns:
        - str: Full path to the cluster model file, or just the filename if basename=True.
        """
        # Access the subproduct dictionary and retrieve the filename template
        subprod_dict = self.get_subproduct_dict(__name__, subproduct)

        # Retrieve the appropriate filename template for the cluster model
        fn_template = subprod_dict['cluster_fn_template']

        fn_kwargs = dict(frequency=frequency, SNR=SNR, downgrade=downgrade, **kwargs)


        # Format the filename template with the parameters
        fn = fn_template.format(**fn_kwargs)

        if basename:
            return fn
        else:
            # Retrieve the system path to the directory holding the (sub)product files
            subprod_path = self.get_subproduct_path(__name__, subproduct)
            return os.path.join(subprod_path, fn)

    @implements(Product.read_product)
    def read_cluster_model(self, frequency='150', SNR=5, downgrade="down2", subproduct='default', 
                           loadtxt_kwargs=None, **kwargs):
        """
        Read the cluster model data from the file.

        Parameters:
        - frequency (str): Frequency of observation (default: '150').
        - SNR (int): Signal-to-noise ratio threshold (default: 5).
        - downgrade (str): Downsampling level (default: 'down2').
        - subproduct (str): Subproduct identifier (default: 'default').
        - loadtxt_kwargs (dict): Additional arguments for `np.loadtxt`.
        - kwargs: Additional keyword arguments.

        Returns:
        - np.ndarray: Loaded cluster model data.
        """
        # Generate the filename using the provided parameters
        fn = self.get_cluster_model_fn(frequency=frequency, SNR=SNR, downgrade=downgrade, 
                                       subproduct=subproduct, basename=False, **kwargs)

        # Default arguments for `np.loadtxt` if none are provided
        if loadtxt_kwargs is None:
            loadtxt_kwargs = {}

        # Read and return the data
        return enmap.read_map(fn, **loadtxt_kwargs)