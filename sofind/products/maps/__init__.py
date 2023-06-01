from ..products import Product, get_implements_decorator

from pixell import enmap
import os

class Map(Product):

    implementedmethods = []
    implements = get_implements_decorator(implementedmethods)
    
    def __init__(self, **kwargs):
        self.set_attrs(__name__, kwargs)
        super().__init__(**kwargs)

    @implements(Product.get_fn)
    def get_map_fn(self, qid, split_num=0, coadd=False, maptag='map',
                   subproduct='default', basename=False, **kwargs):
        """Get the full path to a map product.

        Parameters
        ----------
        qid : str
            Dataset identification string.
        split_num : int, optional
            Split index of the map product, by default 0.
        coadd : bool, optional
            If True, load the corresponding product for the on-disk coadd map,
            by default False. If True, split_num is neglected.
        maptag : str, optional
            The type of product to load, by default 'map.' E.g. 'map_srcfree', 
            'srcs', 'ivar', 'xlink', 'hits', etc.
        subproduct : str, optional
            Name of map subproduct to load raw products from, by default 'default'.
        basename : bool, optional
            Only return file basename, by default False.
        kwargs : dict, optional
            Any additional keyword arguments used to format the map filename.

        Returns
        -------
        str
            Full path to requested product, including its directory.

        Raises
        ------
        LookupError
            If basename is False and the product, subproduct dirname is not
            known to the datamodel.
        """
        subprod_dict = self.get_subproduct_dict(__name__, subproduct)

        # get the appropriate filename template
        if coadd:
            fn_template = subprod_dict['coadd_map_file_template']
        else:
            fn_template = subprod_dict['split_map_file_template']

        # get info about the requested array and add kwargs passed to this
        # method call. use this info to format the file template
        fn_kwargs = self.get_qid_kwargs_by_subproduct(__name__, subproduct, qid)
        fn_kwargs.update(split_num=split_num, maptag=maptag, **kwargs)
        fn = fn_template.format(**fn_kwargs)

        if basename:
            return fn
        else:
            subprod_path = self.get_subproduct_path(__name__, subproduct)
            return os.path.join(subprod_path, fn)

    @implements(Product.read_product)
    def read_map(self, qid, split_num=0, coadd=False, maptag='map',
                 subproduct='default', read_map_kwargs=None,
                 **kwargs):
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
            Name of map subproduct to load raw products from, by default 'default'.
        read_map_kwargs : dict, optional
            Any keyword arguments to pass to enmap.read_map.
        kwargs : dict, optional
            Any additional keyword arguments used to format the map filename.

        Returns
        -------
        enmap.ndmap
            The requested map.
        """
        fn = self.get_map_fn(
            qid, split_num=split_num, coadd=coadd, maptag=maptag,
            subproduct=subproduct, basename=False, **kwargs
            )
        
        if read_map_kwargs is None:
            read_map_kwargs = {}

        return enmap.read_map(fn, **read_map_kwargs)