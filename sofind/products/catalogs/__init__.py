from ..products import Product, get_implements_decorator

import numpy as np

import os

class Catalog(Product):

    implementedmethods = []
    implements = get_implements_decorator(implementedmethods)
    
    def __init__(self, **kwargs):
        self.set_attrs(__name__, kwargs)
        super().__init__(**kwargs)
        self.check_product_config_internal_consistency(__name__)

    @implements(Product.get_fn)
    def get_catalog_fn(self, cat_fn, subproduct='default', basename=False,
                       **kwargs):
        """Get the full path to a catalog product.

        Parameters
        ----------
        cat_fn : str
            The filename for a source catalog. The source catalog must have the
            following features:
                * A row-major list of coordinates
                * The first column is RA (in degrees)
                * The second column is DEC (in degrees)
                * Columns are comma-separated
        subproduct : str, optional
            Name of catalog subproduct to load raw products from, by default 
            'default'.
        basename : bool, optional
            Only return file basename, by default False.
        kwargs : dict, optional
            Any additional keyword arguments used to format the catalog filename.

        Returns
        -------
        str
            If basename, basename of requested product. Else, full path to
            requested product.

        Raises
        ------
        LookupError
            If basename is False and the product, subproduct dirname is not
            known to the datamodel.
        """
        subprod_dict = self.get_subproduct_dict(__name__, subproduct)

        if basename:
            return cat_fn
        else:
            subprod_path = self.get_subproduct_path(__name__, subproduct)
            return os.path.join(subprod_path, cat_fn)

    @implements(Product.read_product)
    def read_catalog(self, cat_fn, subproduct='default', **kwargs):
        """Read a catalog product from disk.

        Parameters
        ----------
        cat_fn : str
            The filename for a source catalog. The source catalog must have the
            following features:
                * A row-major list of coordinates
                * The first column is RA (in degrees)
                * The second column is DEC (in degrees)
                * Columns are comma-separated
        subproduct : str, optional
            Name of catalog subproduct to load raw products from, by default 
            'default'.
        kwargs : dict, optional
            Any additional keyword arguments used to format the catalog filename.

        Returns
        -------
        catalog : (2, N) array
            DEC and RA values (in radians) for each point source.

        Notes
        -----
        Expects RA, DEC columns (degrees), returns DEC, RA rows (radians).
        """
        fn = self.get_catalog_fn(cat_fn, subproduct=subproduct, basename=False,
                              **kwargs)
        ra, dec = np.loadtxt(fn, unpack=True, usecols=[0, 1], delimiter=',')
        return np.radians(np.vstack([dec, ra]))