# If you are adding a product you can use the following template
# in your module. Please only define the product class in this 
# module.

### PRODUCT TEMPLATE in module file hotdogs.py ###

from ..products import Product, get_implements_decorator
    
import numpy as np
import os

# # All products must inherit from Product and implement its productmethods,
# # which one does by decorating a subclass method, e.g. get_hotdog_fn with
# # the decorator @implements(Product.get_fn), for each method tagged with the
# # @productmethod decorator in the Product class.
class HotDog(Product):

    #################################
    ### DO NOT CHANGE THESE LINES ###
    implementedmethods = []
    implements = get_implements_decorator(implementedmethods)

    def __init__(self, **kwargs):
        self.set_attrs(__name__, kwargs)
        super().__init__(**kwargs)
    #################################

    @implements(Product.get_fn)
    # in order to access the subproduct_dict and subproduct_path, subproduct
    # must be passed as a kwarg. for consistency, please set the default 
    # value of subproduct to 'default'
    def get_hotdog_fn(self, qid, condiment='mustard', subproduct='default',
                      **subproduct_kwargs):
        # use subprod_dict to get the filename template for this (sub)product,
        # as well as any other info in the (sub)product configuration file
        subprod_dict = self.get_subproduct_dict(__name__, subproduct)

        # get the appropriate filename template
        fn_template = subprod_dict['hotdog_file_template']

        # get info about the requested array and add kwargs passed to this
        # method call. use this info to format the file template
        fn_kwargs = self.get_qid_kwargs_by_subproduct(qid, __name__, subproduct)
        fn_kwargs.update(condiment=condiment, **subproduct_kwargs)
        fn = fn_template.format(**fn_kwargs)

        # return the full system path to the file
        # subprod_path is the system path to the directory holding this (sub)product
        subprod_path = self.get_subproduct_path(__name__, subproduct)
        return os.path.join(subprod_path, fn)

    @implements(Product.read_product)
    # in order to access the subproduct_dict and subproduct_path, subproduct
    # must be passed as a kwarg. for consistency, please set the default 
    # value of subproduct to 'default'
    def read_hotdog(self, qid, condiment='mustard', subproduct='default', 
                    loadtxt_kwargs=None, **subproduct_kwargs):
        # use get_hotdog_fn and some external library to load the data
        fn = self.get_hotdog_fn(qid, condiment=condiment, subproduct=subproduct, 
                                **subproduct_kwargs)

        if loadtxt_kwargs is None:
            loadtxt_kwargs = {}

        return np.loadtxt(fn, **loadtxt_kwargs)