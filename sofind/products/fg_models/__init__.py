import os

import numpy as np

from ..products import Product, get_implements_decorator


class FGModel(Product):
    implementedmethods = []
    implements = get_implements_decorator(implementedmethods)

    def __init__(self, **kwargs):
        self.set_attrs(__name__, kwargs)
        super().__init__(**kwargs)
        self.check_product_config_internal_consistency(__name__)

    @implements(Product.get_fn)
    def get_fg_model_fn(self, subproduct="default", basename=False, **kwargs):
        """Get the full path to a foreground model file.

        Parameters
        ----------
        subproduct : str, optional
            Name of foreground model subproduct, by default 'default'.
        basename : bool, optional
            Only return file basename, by default False.
        kwargs : dict, optional
            Keywords used to format the subproduct's 'fg_model_fn' template,
            e.g. fsky=70.

        Returns
        -------
        str
            If basename, basename of requested product. Else, full path to
            requested product.
        """
        subprod_dict = self.get_subproduct_dict(__name__, subproduct)
        fn = subprod_dict["fg_model_fn"].format(**kwargs)
        if basename:
            return fn
        return os.path.join(self.get_subproduct_path(__name__, subproduct), fn)

    @implements(Product.read_product)
    def read_fg_model(
        self, qids=None, subproduct="default", qid_aliases=None, **kwargs
    ):
        """Read a foreground covariance cube from disk.

        The file is an npz holding one spectrum C_ell (uK^2, starting at
        ell = 0) per unordered qid pair under keys 'spec:{qid1}{sep}{qid2}'
        with qid1 <= qid2, plus the stored qids ('meta:qids') and separator
        ('meta:sep').

        Parameters
        ----------
        qids : list of str, optional
            Order of the first two axes of the cube. Every pair must be in the
            file. By default, all qids in the file, sorted alphabetically.
        subproduct : str, optional
            Name of foreground model subproduct, by default 'default'.
        qid_aliases : dict, optional
            Maps requested qids to qids in the file whose spectra they take,
            e.g. {'pa5a_dd': 'pa5a'} for a qid without its own model. By
            default, every qid is read as itself.
        kwargs : dict, optional
            Keywords used to format the filename, e.g. fsky=70.

        Returns
        -------
        np.ndarray
            Covariance cube of shape (nqid, nqid, nell).
        """
        fn = self.get_fg_model_fn(subproduct=subproduct, **kwargs)
        alias = qid_aliases or {}
        with np.load(fn, allow_pickle=True) as z:
            sep = str(z["meta:sep"][0])
            qids = list(z["meta:qids"]) if qids is None else qids
            names = [alias.get(q, q) for q in qids]
            key = lambda a, b: sep.join(sorted((a, b)))
            pairs = {key(a, b) for a in names for b in names}
            spec = {k: z[f"spec:{k}"] for k in pairs}  # each spectrum read once
            return np.array([[spec[key(a, b)] for b in names] for a in names])
