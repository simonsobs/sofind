# If you are adding a product you can use the following template
# in your module.

### PRODUCT TEMPLATE in module file hotdogs.py ###

from ..products import Product, get_implements_decorator
    
import numpy as np
import os
import healpy as hp

# # All products must inherit from Product and implement its productmethods,
# # which one does by decorating a subclass method, e.g. get_hotdog_fn with
# # the decorator @implements(Product.get_fn), for each method tagged with the
# # @productmethod decorator in the Product class.
class MapsHealpix(Product):

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
    # in order to access the subproduct_dict and subproduct_path, subproduct
    # must be passed as a kwarg. for consistency, please set the default 
    # value of subproduct to 'default'
    def get_map_healpix_fn(self, qid, subproduct='default',
                      basename=False, **kwargs):
        # use subprod_dict to get the filename template for this (sub)product,
        # as well as any other info in the (sub)product configuration file
        subprod_dict = self.get_subproduct_dict(__name__, subproduct)

        # get the appropriate filename template
        fn_template = subprod_dict['map_file_template']

        # get info about the requested array and add kwargs passed to this
        # method call. use this info to format the file template
        fn_kwargs = self.get_qid_kwargs_by_subproduct(__name__, subproduct, qid)
        fn_kwargs.update(**kwargs)
        fn = fn_template.format(**fn_kwargs)

        if basename:
            return fn
        else:
            # subprod_path is the system path to the directory holding this (sub)product
            subprod_path = self.get_subproduct_path(__name__, subproduct)
            return os.path.join(subprod_path, fn)

    @implements(Product.read_product)
    # in order to access the subproduct_dict and subproduct_path, subproduct
    # must be passed as a kwarg. for consistency, please set the default 
    # value of subproduct to 'default'
    def read_map_healpix(self, qid, subproduct='default', 
                    read_map_kwargs=None, **kwargs):
        # use get_hotdog_fn and some external library to load the data
        fn = self.get_map_healpix_fn(qid, subproduct=subproduct, 
                                basename=False, **kwargs)

        if read_map_kwargs is None:
            read_map_kwargs = {}

        return hp.read_map(fn, **read_map_kwargs)
    
    


# Feel free to add stuff here