# If you are adding a product you can use the following template
# in your module.

### PRODUCT TEMPLATE in module file hotdogs.py ###

from ..products import Product, get_implements_decorator
    
import numpy as np
import os

# # All products must inherit from Product and implement its productmethods,
# # which one does by decorating a subclass method, e.g. get_hotdog_fn with
# # the decorator @implements(Product.get_fn), for each method tagged with the
# # @productmethod decorator in the Product class.
class Calibration(Product):

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
    def get_calibration_fn(self, qid, **kwargs):
        raise NotImplementedError('Cals live in sofind configs, not files on disk!')

    @implements(Product.read_product)
    # in order to access the subproduct_dict and subproduct_path, subproduct
    # must be passed as a kwarg. for consistency, please set the default 
    # value of subproduct to 'default'
    def read_calibration(self, qid, subproduct='default', key=None):
        subprod_dict = self.get_subproduct_dict(__name__, subproduct)
        qid_info = subprod_dict[qid]

        if key is None:
            return qid_info
        else:
            return qid_info[key]