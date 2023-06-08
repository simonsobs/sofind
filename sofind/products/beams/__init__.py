from ..products import Product, get_implements_decorator

import os

class Beam(Product):

    implementedmethods = []
    implements = get_implements_decorator(implementedmethods)
    
    def __init__(self, **kwargs):
        self.set_attrs(__name__, kwargs)
        super().__init__(**kwargs)
        self.check_product_config_internal_consistency(__name__)

    @implements(Product.get_fn)
    def get_beam_fn(self, qid, subproduct='default', basename=False, **kwargs):
        subprod_dict = self.get_subproduct_dict(__name__, subproduct)

        # get the appropriate filename template
        fn_template = subprod_dict['beam_file_template']

        # get info about the requested array and add kwargs passed to this
        # method call. use this info to format the file template
        fn_kwargs = self.get_qid_kwargs_by_subproduct(__name__, subproduct, qid)
        fn_kwargs.update(**kwargs)
        fn = fn_template.format(**fn_kwargs)

        if basename:
            return fn
        else:
            subprod_path = self.get_subproduct_path(__name__, subproduct)
            return os.path.join(subprod_path, fn)

    @implements(Product.read_product)
    def read_beam(self, qid, subproduct='default', **kwargs):
        fn = self.get_beam_fn(qid, subproduct=subproduct, basename=False, 
                              **kwargs)
        print(f'Loading {fn} from disk')
        return None