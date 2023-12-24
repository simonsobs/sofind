from ..products import Product, get_implements_decorator

import os
import numpy as np

class Beam(Product):

    implementedmethods = []
    implements = get_implements_decorator(implementedmethods)
    
    def __init__(self, **kwargs):
        self.set_attrs(__name__, kwargs)
        super().__init__(**kwargs)
        self.check_product_config_internal_consistency(__name__)

    @implements(Product.get_fn)
    def get_beam_fn(self,  qid, beam_name = None, split_num=0, coadd=False, 
                    subproduct='default', basename=False, **kwargs):
    
        """Get the full path to a beam product.

        Parameters
        ----------
        qid : str
            Dataset identification string.
        beam_name: str
            Name of beam
            Defaults None sets beam_name = subproduct
        split_num : int, optional
            Split index of the map product, by default 0.
        coadd : bool, optional
            If True, load the corresponding product for the on-disk coadd map,
            by default False. If True, split_num is neglected.
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
            beam product.
        """
        if beam_name is None:
            beam_name = subproduct

        subprod_dict = self.get_subproduct_dict(__name__, subproduct)[beam_name]

        # get the appropriate filename template
        if coadd:
            fn_template = subprod_dict['coadd_beam_file_template']
        else:
            fn_template = subprod_dict['split_beam_file_template']

        # get info about the requested array and add kwargs passed to this
        # method call. use this info to format the file template
        fn_kwargs = self.get_qid_kwargs_by_subproduct(__name__, subproduct, qid)
        fn_kwargs.update(split_num = split_num, **kwargs)
        fn = fn_template.format(**fn_kwargs)

        if not fn.endswith('.txt'): 
                fn += '.txt'

        if basename:
            return fn
        else:
            subprod_path = self.get_subproduct_path(__name__, subproduct)
            return os.path.join(subprod_path, fn)

    @implements(Product.read_product)
    def read_beam(self, qid, beam_name = None, split_num=0, coadd=False, 
                  subproduct='default', loadtxt_kwargs=None, **kwargs):

        """Read a map product from disk.

        Parameters
        ----------
        qid : str
            Dataset identification string.
        beam_name: str
            Name of beam
            Defaults None sets beam_name = subproduct
        split_num : int, optional
            Split index of the map product, by default 0.
        coadd : bool, optional
            If True, load the corresponding product for the on-disk coadd map,
            by default False. If True, split_num is neglected.
        subproduct : str, optional
            Name of mask subproduct to load raw products from, by default 
            'default'.
        basename : bool, optional
            Only return file basename, by default False.
        kwargs : dict, optional
            Any additional keyword arguments used to format the mask filename.
        loadtxt_kwargs : dict, optional
            Any keyword arguments to pass to np.loadtxt
        kwargs : dict, optional
            Any additional keyword arguments used to format the beam filename.

        Returns
        -------
        np.array
            The requested beam = [ells, bells]
        """
        fn = self.get_beam_fn(qid, beam_name = beam_name, split_num=split_num, coadd=coadd,
                              subproduct=subproduct, basename=False, 
                              **kwargs)
        print(f'Loading {fn} from disk')

        if loadtxt_kwargs is None:
            loadtxt_kwargs = {'unpack': True, 'usecols': [0,1]}

        return np.loadtxt(fn, **loadtxt_kwargs)