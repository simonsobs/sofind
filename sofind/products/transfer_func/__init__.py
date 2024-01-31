from ..products import Product, get_implements_decorator
    
import numpy as np
import os

class TransferFunc(Product):

    implementedmethods = []
    implements = get_implements_decorator(implementedmethods)

    def __init__(self, **kwargs):
        self.set_attrs(__name__, kwargs)
        super().__init__(**kwargs)
        self.check_product_config_internal_consistency(__name__)

    @implements(Product.get_fn)

    def get_tf_fn(self, qid, subproduct='default',
                      basename=False, **kwargs):
        """Get the full path to a transfer function.

        Parameters
        ----------
        qid : str
            Dataset identification string.
        subproduct : str, optional
            Name of transfer function subproduct to load raw products from, by default 
            'default'.
        basename : bool, optional
            Only return file basename, by default False.
        kwargs : dict, optional
            Any additional keyword arguments used to format the tf filename.

        Returns
        -------
        str
            If basename, basename of requested product. Else, full path to
            requested product.

        Raises
        ------
        TypeError
            If basename is False and the product, subproduct dirname is not
            known to the datamodel.
        """
        
        subprod_dict = self.get_subproduct_dict(__name__, subproduct)
        # get the appropriate filename template
        fn_template = subprod_dict['tf_template']

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
    def read_tf(self, qid, subproduct='default', 
                    loadtxt_kwargs=None, **kwargs):
        """Read transfer function product from disk.

        Parameters
        ----------
        qid : str
            Dataset identification string.
        subproduct : str, optional
            Name of transfer function subproduct to load raw products from, by default 
            'default'.
        basename : bool, optional
            Only return file basename, by default False.
        loadtxt_kwargs: dict, optional
            Any additional kwargs to pass to np.loadtxt, by default 
            {'unpack': True}.
        kwargs : dict, optional
            Any additional keyword arguments used to format the tf filename.

        Returns
        -------
        np.array
            The requested transfer function [ell, tf(ell)]
        """

        # use get_tf_fn and some external library to load the data
        fn = self.get_tf_fn(qid, subproduct=subproduct, 
                                basename=False, **kwargs)
        if loadtxt_kwargs is None:
            loadtxt_kwargs = {'unpack': True}

        return np.loadtxt(fn, **loadtxt_kwargs)