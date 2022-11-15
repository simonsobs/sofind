from .product import Product, set_attrs_by_filename, get_implements_decorator

from pixell import enmap
import os

class Map(Product):

    implementedmethods = []
    implements = get_implements_decorator(implementedmethods)
    
    def __init__(self, **kwargs):
        set_attrs_by_filename(self, __file__, kwargs)
        super().__init__(**kwargs)

    @implements(Product.get_fn)
    def get_map_fn(self, qid, split_num=0, coadd=False, maptag='map'):
        """Get the full path to a map product.

        Parameters
        ----------
        qid : str
            Dataset identification string.
        split_num : int, optional
            Split index of the map product, by default 0.
        coadd : bool, optional
            If True, load the corresponding product for the on-disk coadd map,
            by default False.
        maptag : str, optional
            The type of product to load, by default 'map.' E.g. 'map_srcfree', 
            'srcs', 'ivar', 'xlink', 'hits', etc.

        Returns
        -------
        str
            Full path to requested product, including its directory.
        """
        if coadd:
            fn_template = self.map_dict['coadd_map_file_template']
        else:
            fn_template = self.map_dict['split_map_file_template']

        fn_kwargs = {}
        fn_kwargs.update(self.qid_dict[qid]) # add info about the requested array
        fn_kwargs.update(dict(               # add args passed to this method
            split_num=split_num,
            maptag=maptag
        ))
            
        fn = fn_template.format(**fn_kwargs) # format the file string

        return os.path.join(self.map_path, fn)

    @implements(Product.read_product)
    def read_map(self, qid, split_num=0, coadd=False, maptag='map', **kwargs):
        """Read a map product from disk.

        Parameters
        ----------
        qid : str
            Dataset identification string.
        split_num : int, optional
            Split index of the map product, by default 0.
        coadd : bool, optional
            If True, load the corresponding product for the on-disk coadd map,
            by default False.
        maptag : str, optional
            The type of product to load, by default 'map.' E.g. 'map_srcfree', 
            'srcs', 'ivar', 'xlink', 'hits', etc.
        kwargs : dict
            Any keyword arguments to pass to enmap.read_map

        Returns
        -------
        enmap.ndmap
            The requested map.
        """
        fn = self.get_map_fn(qid, split_num=split_num, coadd=coadd, maptag=maptag)
        return enmap.read_map(fn, **kwargs)