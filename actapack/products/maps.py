from .products import Product, get_implements_decorator

from pixell import enmap
import os

class Map(Product):

    implementedmethods = []
    implements = get_implements_decorator(implementedmethods)
    
    def __init__(self, **kwargs):
        self.set_attrs(__file__, kwargs)
        super().__init__(**kwargs)

    @implements(Product.get_fn)
    def get_map_fn(self, qid, null_split=None, split_num=0, coadd=False, 
                   maptag='map', subproduct='default'):
        """Get the full path to a map product.

        Parameters
        ----------
        qid : str
            Dataset identification string.
        null_split : str, optional
            If subproduct refers to a null test map, e.g. 'pwv_split', then
            the particular desired split, e.g. 'low_pwv'. By default None.
        split_num : int, optional
            Split index of the map product, by default 0.
        coadd : bool, optional
            If True, load the corresponding product for the on-disk coadd map,
            by default False. If True, split_num is neglected.
        maptag : str, optional
            The type of product to load, by default 'map.' E.g. 'map_srcfree', 
            'srcs', 'ivar', 'xlink', 'hits', etc.
        subproduct : str, optional
            The maps subproduct, by default the 'default' maps subproduct. 

        Returns
        -------
        str
            Full path to requested product, including its directory.

        Notes
        -----
        The list of possible null_split arguments is given below for each
        subproduct:

        * default: []
        * pwv_split: ['low_pwv', 'high_pwv']
        """
        subprod_dict = self.get_subproduct_dict(__file__, subproduct)

        # get the appropriate filename template
        if coadd:
            fn_template = subprod_dict['coadd_map_file_template']
        else:
            fn_template = subprod_dict['split_map_file_template']

        # get info about the requested array and add kwargs passed to this
        # method call. use this info to format the file template
        fn_kwargs = self.get_qid_kwargs_by_suproduct(qid, __file__, subproduct)
        fn_kwargs.update(null_split=null_split, split_num=split_num, maptag=maptag)
        fn = fn_template.format(**fn_kwargs)

        # return the full system path to the file
        subprod_path = self.get_subproduct_path(__file__, subproduct)
        return os.path.join(subprod_path, fn)

    @implements(Product.read_product)
    def read_map(self, qid, null_split=None, split_num=0, coadd=False, 
                 maptag='map', subproduct='default', **kwargs):
        """Read a map product from disk.

        Parameters
        ----------
        qid : str
            Dataset identification string.
        null_split : str, optional
            If subproduct refers to a null test map, e.g. 'pwv_split', then
            the particular desired split, e.g. 'low_pwv'. By default None.
        split_num : int, optional
            Split index of the map product, by default 0.
        coadd : bool, optional
            If True, load the corresponding product for the on-disk coadd map,
            by default False. If True, split_num is neglected.
        maptag : str, optional
            The type of product to load, by default 'map.' E.g. 'map_srcfree', 
            'srcs', 'ivar', 'xlink', 'hits', etc.
        subproduct : str, optional
            The maps subproduct, by default the 'default' maps subproduct. 
        kwargs : dict
            Any keyword arguments to pass to enmap.read_map.

        Returns
        -------
        enmap.ndmap
            The requested map.

        Notes
        -----
        The list of possible null_split arguments is given below for each
        subproduct:

        * default: []
        * pwv_split: ['low_pwv', 'high_pwv']
        """
        fn = self.get_map_fn(
            qid, null_split=null_split, split_num=split_num, coadd=coadd,
            maptag=maptag, subproduct=subproduct
            )
        return enmap.read_map(fn, **kwargs)