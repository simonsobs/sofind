
from ..products import Product, get_implements_decorator
    
import numpy as np
import os
import pickle

class Calibration(Product):

    implementedmethods = []
    implements = get_implements_decorator(implementedmethods)

    def __init__(self, **kwargs):
        self.set_attrs(__name__, kwargs)
        super().__init__(**kwargs)
        self.check_product_config_internal_consistency(__name__)


    @implements(Product.get_fn)
    def get_calibration_fn(self, qid, which='cals', subproduct='default',
                      basename=False, **kwargs):
        
        """Get the full path to a calibration product.

        Parameters
        ----------
        qid : str
            Dataset identification string.
        which : str, optional
            Whether to load from the available 'cals' or 'poleffs', by default
            'cals'.
        subproduct : str, optional
            Name of calibration subproduct to load raw products from, by default 
            'default'.
        basename : bool, optional
            Only return file basename, by default False.
        kwargs : dict, optional
            Any additional keyword arguments used to format the calibration filename.

        Returns
        -------
        str
            If basename, basename of requested product. Else, full path to
            requested product.
        """
        subprod_dict = self.get_subproduct_dict(__name__, subproduct)

        # get the appropriate filename template
        cals_file_template = subprod_dict['cals_file_template']
        poleffs_file_template = subprod_dict['poleffs_file_template']

        # get info about the requested array and add kwargs passed to this
        # method call. use this info to format the file template
        fn_kwargs = self.get_qid_kwargs_by_subproduct(__name__, subproduct, qid)
        fn_kwargs.update(**kwargs)

        if which == 'cals':
            fn = cals_file_template.format(**fn_kwargs)
        elif which == 'poleffs':
            fn = poleffs_file_template.format(**fn_kwargs)      
        else:
            raise ValueError(f"which must be 'cals' or 'poleffs', got {which}")
        
        if basename:
            return fn
        else:
            # subprod_path is the system path to the directory holding this (sub)product
            subprod_path = self.get_subproduct_path(__name__, subproduct)
            return os.path.join(subprod_path, fn)

    @implements(Product.read_product)
    def read_calibration(self, qid, which='cals', subproduct='default', **kwargs):       
        """
        Read a calibration product from disk.

        Parameters
        ----------
        qid : str
            Dataset identification string.
        which : str, optional
            Whether to load from the available 'cals' or 'poleffs', by default
            'cals'.
        subproduct : str, optional
            Name of calibration subproduct to load raw products from, by default 
            'default'.
        basename : bool, optional
            Only return file basename, by default False.
        kwargs : dict, optional
            Any additional keyword arguments used to format the calibration key.

        Returns
        -------
        np.float
            The requested calibration value
        """
        subprod_dict = self.get_subproduct_dict(__name__, subproduct)

        # get the appropriate dictionary key template
        key_template = subprod_dict['key_template']

        # get info about the requested array and add kwargs passed to this
        # method call. use this info to format the key template
        qid_kwargs = self.get_qid_kwargs_by_subproduct(__name__, subproduct, qid)
        qid_kwargs.update(**kwargs)
        key = key_template.format(**qid_kwargs)

        # calibration & polarization efficies are stored in a dictionary
        # like {'dr6_pa4_f220': {'calibs': [0.9111]}}, annoyingly
        fn = self.get_calibration_fn(qid, which=which, subproduct=subproduct, 
                                basename=False, **kwargs)

        with open(fn, 'rb') as f:
            d = pickle.load(f)

        return d[key]['calibs'][0]
