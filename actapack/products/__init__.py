# Add an import statement for your module
from .map import *
from .beam import *

# If you are adding a product you can use the following template
# in your module. Please only define the product class in this 
# module.

### PRODUCT TEMPLATE in module file hotdog.py ###

# from .product import Product, set_attrs_by_filename, get_implements_decorator

# import numpy as np

# All products must inherit from Product and implement its productmethods,
# which one does by decorating a subclass method, e.g. get_hotdog_fn, with
# the decorator @implements(Product.get_fn), for each productmethod in
# the Product class.
# class HotDog(Product):

#     implementedmethods = []
#     implements = get_implements_decorator(implementedmethods)

#     def __init__(self, **kwargs):
#         set_attrs_by_filename(self, __file__, kwargs)
#         super().__init__(**kwargs)

#     @implements(Product.get_fn)
#     def get_hotdog_fn(self, qid, condiment='mustard'):
#         # use arguments, and possibly info coming from a qid, to populate a 
#         # "filename_template" coming from the self.hotdog_dict
#         fn_template = self.hotdog_dict['hotdog_file_template']

#         fn_kwargs = {}
#         fn_kwargs.update(self.qid_dict[qid]) # add info about the requested array
#         fn_kwargs.update(dict(               # add args passed to this method
#             condiment=condiment
#         ))

#         fn = fn_template.format(**fn_kwargs) # format the file string

#         # finally, tack on the self.hotdog_path (along with self.hotdog_dict,
#         # this attribute is assigned for you in set_attrs_by_filename(...))
#         return os.path.join(self.hotdog_path, fn)

#     @implements(Product.read_product)
#     def read_hotdog(self, qid, condiment='mustard', *args, **kwargs):
#         # use get_hotdog_fn and some external library to load the data
#         fn = self.get_hotdog_fn(qid, condiment=condiment)
#         return np.loadtxt(fn, *args, **kwargs)