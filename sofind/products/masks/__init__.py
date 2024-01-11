from ..products import Product, get_implements_decorator

from pixell import enmap

import os

class Mask(Product):

    implementedmethods = []
    implements = get_implements_decorator(implementedmethods)
    
    def __init__(self, **kwargs):
        self.set_attrs(__name__, kwargs)
        super().__init__(**kwargs)
        self.check_product_config_internal_consistency(__name__)

    @implements(Product.get_fn)
    def get_mask_fn(self, mask_fn=None, mask_type=None, subproduct='default',
                    basename=False, **kwargs):
        """Get the full path to a mask product.

        Parameters
        ----------
        mask_fn : str
            The filename for a mask (set to None if unknown)
        mask_type: str
            The type of mask to load (if mask_fn set to None because unknown)
        subproduct : str, optional
            Name of mask subproduct to load raw products from, by default 
            'default'.
        basename : bool, optional
            Only return file basename, by default False.
        kwargs : dict, optional
            Any additional keyword arguments used to format the mask filename.

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

        if mask_fn is None:
            mask_fn = subprod_dict[mask_type]['mask_fn']
        if basename:
            return mask_fn
        else:
            subprod_path = self.get_subproduct_path(__name__, subproduct)
            return os.path.join(subprod_path, mask_fn)

    @implements(Product.read_product)
    def read_mask(self, mask_fn=None, mask_type=None, subproduct='default',
                  read_map_kwargs=None, **kwargs):
        """Read a mask product from disk.

        Parameters
        ----------
        mask_fn : str
            The filename for a mask (set to None if unknown)
        mask_type: str
            The type of mask to load (if mask_fn set to None because unknown)
        subproduct : str, optional
            Name of mask subproduct to load raw products from, by default 
            'default'.
        read_map_kwargs : dict, optional
            Any keyword arguments to pass to enmap.read_map.
        kwargs : dict, optional
            Any additional keyword arguments used to format the mask filename.

        Returns
        -------
        enmap.ndmap
            The requested mask.
        """
        fn = self.get_mask_fn(mask_fn=mask_fn, mask_type=mask_type, 
                              subproduct=subproduct, basename=False, **kwargs)
        
        if read_map_kwargs is None:
            read_map_kwargs = {}
        
        return enmap.read_map(fn, **read_map_kwargs)