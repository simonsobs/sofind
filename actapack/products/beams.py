from .products import Product, set_attrs_by_filename, get_implements_decorator

import os

class Beam(Product):

    implementedmethods = []
    implements = get_implements_decorator(implementedmethods)
    
    def __init__(self, **kwargs):
        set_attrs_by_filename(self, __file__, kwargs)
        super().__init__(**kwargs)

    @implements(Product.get_fn)
    def get_beam_fn(self):
        fn = self.beams_dict['beam_info']
        return os.path.join(self.beams_path, fn)

    @implements(Product.read_product)
    def read_beam(self):
        fn = self.get_beam_fn()
        print(f'Loading {fn} from disk')
        return None