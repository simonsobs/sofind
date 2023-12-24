from ..products import Product, get_implements_decorator
    
import numpy as np
import os

class Calibration(Product):

    implementedmethods = []
    implements = get_implements_decorator(implementedmethods)

    def __init__(self, **kwargs):
        self.set_attrs(__name__, kwargs)
        super().__init__(**kwargs)
        self.check_product_config_internal_consistency(__name__)

    @implements(Product.get_fn)
    def get_calibration_fn(self, qid, **kwargs):

        """
        Get the full path to calibration product.

        Raises
        ------
        NotImplementedError
            Calibration factors live in sofind configs, not on disk
        """
        
        raise NotImplementedError('Cals live in sofind configs, not files on disk!')

    @implements(Product.read_product)
    def read_calibration(self, qid, subproduct='default', key=None):

        """Read calibration product from sofind config.

        Parameters
        ----------
        qid: str
            Dataset identification string.
        subproduct : str, optional
            Name of mask subproduct to load raw products from, by default 
            'default'.
        key: str
            Type of calibration product ('cal' or 'poleff')

        Returns
        -------
        if key == None
            dict
                The requested calibrations for qid
        else
            np.float
                The requested calibration (cal, poleff) for qid
        """
        subprod_dict = self.get_subproduct_dict(__name__, subproduct)
        qid_info = subprod_dict[qid]

        if key is None:
            return qid_info
        else:
            return qid_info[key]