from .product import Product, make_implements_decorator

import os

class Beam(Product):

    implementedmethods = []
    implements = make_implements_decorator(implementedmethods)
    
    def __init__(self, **kwargs):
        product_tag = os.path.splitext(os.path.basename(__file__))[0]
        setattr(self, f'{product_tag}_path', kwargs.pop(f'{product_tag}_path'))
        setattr(self, f'{product_tag}_dict', kwargs.pop(f'{product_tag}_dict'))
        super().__init__(**kwargs)

    @implements(Product.get_fn)
    def get_beam_fn(self):
        fn = self.beam_dict['beam_info']
        return os.path.join(self.beam_path, fn)

    @implements(Product.read_product)
    def read_beam(self):
        fn = self.get_beam_fn()
        print(f'Loading {fn} from disk')
        return None