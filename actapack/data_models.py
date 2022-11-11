from actapack import utils

from pixell import enmap
import numpy as np
import yaml

import os, sys


class DataModel(dict):

    def __init__(self, name, config_dict):
        """Helper class for interfacing with raw, distributed data products on disk,
        e.g. a map release. Allows minimal, flexible loading of maps. Implemented as
        thin wrapper around a dictionary.

        Parameters
        ----------
        name : str
            Name of this data model.
        config_dict : dict
            Dictionary holding special data model items. They are: 
                * split_maps_file_template
                * coadd_maps_file_template
                * dtype
                * noise_seed
                * qid blocks
            Each qid block must map to another dictionary holding:
                * array
                * freq
                * num_splits
                * qid_name_template

        Notes
        -----
        A user's mnms_config must contain a block with the same 'name' as this data
        model. That block must contain an item 'maps_path' indicating the directory
        under which map products are held.
        """
        super().__init__(self)

        self._name = os.path.splitext(name)[0]

        self._split_maps_file_template = config_dict.pop('split_maps_file_template')
        self._coadd_maps_file_template = config_dict.pop('coadd_maps_file_template')
        self._maps_path = get_system_fn(
            '.actapack_config', '', config_keys=[self._name, 'maps_path']
            )

        # format each qid's name template (or set it equal to qid if not provided)
        # also check for required keys
        for qid in config_dict:
            qid_kwargs = config_dict[qid]
            qid_name_template = qid_kwargs.pop('qid_name_template', qid)
            for key in ['array', 'freq', 'num_splits']:
                assert key in qid_kwargs, \
                    f'qid {qid} missing required item under key {key}'
            qid_kwargs['qid_name'] = qid_name_template.format(**qid_kwargs)
        
        self.update(**config_dict)

    @classmethod
    def from_config(cls, config_name):
        """Load a DataModel instance from an existing configuration file.

        Parameters
        ----------
        config_name : str
            Name of file, which will become name of the data model.

        Returns
        -------
        DataModel
            DataModel instance built from dictionary read from configuration file.

        Notes
        -----
        Only supports loading files with a yaml extension.
        """
        if not config_name.endswith('.yaml'):
            config_name = config_name + '.yaml'

        private_fn = get_system_fn('.actapack_config', config_name, config_keys=['user_configs'])
        package_fn = get_package_fn('mnms', os.path.join('configs', config_name))
        config_fn = get_protected_fn([private_fn, package_fn])
        config_dict = config_from_yaml_file(config_fn)
        return cls(config_name, config_dict)
    
    @property
    def name(self):
        return self._name

    def get_map_fn(self, qid, split_num=0, coadd=False, maptag='map',
                   fmt='fits'):
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
        fmt : str, optional
            The file extension, by default fits.

        Returns
        -------
        str
            Full path to requested product, including its directory.
        """
        qid_kwargs = self[qid].copy()
        qid_kwargs.update(dict(
            split_num=split_num,
            maptag=maptag
        ))

        if coadd:
            maps_file_template = self._coadd_maps_file_template
        else:
            maps_file_template = self._split_maps_file_template
        maps_file_template = maps_file_template.format(**qid_kwargs)
        maps_file_template += f'.{fmt}'

        return os.path.join(self._maps_path, maps_file_template)

# adapted from soapack.interfaces
def config_from_yaml_file(filename):
    """Returns a dictionary from a yaml file given by absolute filename.
    """
    with open(filename) as f:
        config = yaml.safe_load(f)
    return config

def get_from_mnms_config(block, key):
    """Get value from user mnms_config file.

    Parameters
    ----------
    block : any
        Block within mnms_config to fetch.
    key : any
        Key within block to fetch.

    Returns
    -------
    any
        Value at mnms_config[block][key]
    """
    home_fn = os.environ['HOME']
    mnms_config = config_from_yaml_file(os.path.join(home_fn, '.mnms_config.yaml'))
    return mnms_config[block][key]

def get_package_fn(package, basename):
    """Get a filename from within a given package. Useful for accessing
    data that is distributed within the package.

    Parameters
    ----------
    package : str
        Name of package.
    basename : str
        Path relative to package.

    Returns
    -------
    str
        Full path to basename.
    """
    package_path = os.path.dirname(sys.modules[package].__file__)
    return os.path.join(package_path, basename)

def get_system_fn(home_config, basename, config_keys=None):
    """Get a filename on the system according to a user configuration file.
    The configuration file must be located in the user's home directory and
    be a yaml file. 

    Parameters
    ----------
    home_config : str
        Config name. Must be a yaml file.
    basename : str
        Additional path to append to the returned filename.
    config_keys : iterable, optional
        Keys to iteratively access information in the configuration file, by 
        default None. 

    Returns
    -------
    str
        Full path to basename.

    Examples
    --------
    If a configuration file '.mnms_config.yaml' has the following contents:

    '''
    mnms:
        private_path: "/scratch/gpfs/zatkins/data/ACTCollaboration/mnms/"
        public_path: "/projects/ACT/zatkins/data/ACTCollaboration/mnms/"
    '''

    then the following demonstrates the usage of this function:

    >>> from actapack.utils import get_sytem fn
    >>> home_config = '.mnms_config' # could also use full name, '.mnms_config.yaml'
    >>> basename = 'sims/sim_001.fits' # this file lives inside the the private_path, for example
    >>> config_keys=('mnms', 'private_path') # get the private_path
    >>> fn = get_system_fn(home_config, basename, config_keys=config_keys)
    >>> print(fn)
    >>> '/scratch/gpfs/zatkins/data/ACTCollaboration/mnms/sims/sim_001.fits'
    """
    if not home_config.endswith('.yaml'):
        home_config = home_config + '.yaml'

    if config_keys is None:
        config_keys = []

    home_config_dict = config_from_yaml_file(
        os.path.join(os.environ['HOME'], home_config)
        )
    
    out = home_config_dict
    for key in config_keys:
        out = out[key]

    return os.path.join(out, basename)

def get_protected_fn(fns, no_fn_collisions=True, write_to_fn_idx=None):
    """Get one filename from a list of filenames, with restrictions on whether
    all or None of the possibilities exist.

    Parameters
    ----------
    fns : iterable of str
        Full filenames that could possibly be returned.
    no_fn_collisions : bool, optional
        If write_to_fn_idx is not supplied: enforce that at most one of the
        supplied fns exists if True, and return the first fn that exists in fns 
        if False. If write_to_fn_idx is supplied, then enforce that none of the fns
        other than the write_fn exists.
    write_to_fn_idx : int, optional
        If supplied, return the filename at this index in the list of
        possibilities.

    Returns
    -------
    str
        Full path to a file.

    Raises
    ------
    FileExistsError
        If write_to_fn_idx is not supplied:
            If no_fn_collisions is True and more than one of fns exists.

        Or if write_to_fn_idx is supplied:
            If no_fn_collisions is True and more than zero of the other
            fns exists.
    FileNotFoundError
        If write_to_fn_idx is not supplied and none of fns exists.
    """
    fns = list(fns)

    if write_to_fn_idx is not None:
        write_fn = fns.pop(write_to_fn_idx)
        fns_exists = np.array([os.path.isfile(f) for f in fns])
        num_exists = fns_exists.sum()

        if no_fn_collisions and num_exists > 0:
            err_str = '\n'.join(fns) 
            raise FileExistsError(
                f'Want to write to {write_fn}\n\nbut more than one of the following exists:\n{err_str}'
                )
        else:
            return write_fn

    else:
        fns_exists = np.array([os.path.isfile(f) for f in fns])
        num_exists = fns_exists.sum()         
        
        err_str = '\n'.join(fns) 
        if no_fn_collisions and num_exists > 1:
            raise FileExistsError(
                f'More than one of the following exists:\n{err_str}'
                )

        if num_exists == 0:
            raise FileNotFoundError(
                f'None of the following exists:\n{err_str}'
            )
    
        out_idx = np.min(np.where(fns_exists)[0])
        return fns[out_idx]

def get_data_model(name=None):
    """Load a DataModel instance from an existing configuration file.

    Parameters
    ----------
    name : str, optional
        Name of file, which will become name of the data model, by default None.
        If None, name grabbed from the user's mnms_config 'default_data_model'.

    Returns
    -------
    DataModel
        DataModel instance built from dictionary read from configuration file.
    """
    if name is None:
        name = get_from_mnms_config('mnms', 'default_data_model')
    return DataModel.from_config(name)

def read_map(data_model, qid, split_num=0, coadd=False, ivar=False):
    """Read a map from disk according to the data_model filename conventions.

    Parameters
    ----------
    data_model : DataModel
         DataModel instance to help load raw products.
    qid : str
        Dataset identification string.
    split_num : int, optional
        The 0-based index of the split to simulate, by default 0.
    coadd : bool, optional
        If True, load the corresponding product for the on-disk coadd map,
        by default False.
    ivar : bool, optional
        If True, load the inverse-variance map for the qid and split. If False,
        load the source-free map for the same, by default False.

    Returns
    -------
    enmap.ndmap
        The loaded map product, with at least 3 dimensions.
    """
    if ivar:
        map_fn = data_model.get_map_fn(qid, split_num=split_num, coadd=coadd, maptag='ivar')
        omap = enmap.read_map(map_fn)
    else:
        try:
            map_fn = data_model.get_map_fn(qid, split_num=split_num, coadd=coadd, maptag='map_srcfree')
            omap = enmap.read_map(map_fn)
        except FileNotFoundError:
            map_fn = data_model.get_map_fn(qid, split_num=split_num, coadd=coadd, maptag='map')
            srcs_fn = data_model.get_map_fn(qid, split_num=split_num, coadd=coadd, maptag='srcs')
            omap = enmap.read_map(map_fn) - enmap.read_map(srcs_fn)

    if omap.ndim == 2:
        omap = omap[None]
    return omap

def read_map_geometry(data_model, qid, split_num=0, coadd=False, ivar=False):
    """Read a map geometry from disk according to the data_model filename
    conventions.

    Parameters
    ----------
    data_model : DataModel
         DataModel instance to help load raw products.
    qid : str
        Dataset identification string.
    split_num : int, optional
        The 0-based index of the split to simulate, by default 0.
    coadd : bool, optional
        If True, load the corresponding product for the on-disk coadd map,
        by default False.
    ivar : bool, optional
        If True, load the inverse-variance map for the qid and split. If False,
        load the source-free map for the same, by default False.

    Returns
    -------
    tuple of int, astropy.wcs.WCS
        The loaded map product geometry, with at least 3 dimensions, and its wcs.
    """
    if ivar:
        map_fn = data_model.get_map_fn(qid, split_num=split_num, coadd=coadd, maptag='ivar')
        shape, wcs = enmap.read_map_geometry(map_fn)
    else:
        try:
            map_fn = data_model.get_map_fn(qid, split_num=split_num, coadd=coadd, maptag='map_srcfree')
            shape, wcs = enmap.read_map_geometry(map_fn)
        except FileNotFoundError:
            map_fn = data_model.get_map_fn(qid, split_num=split_num, coadd=coadd, maptag='map')
            shape, wcs = enmap.read_map_geometry(map_fn)

    if len(shape) == 2:
        shape = (1, *shape)
    return shape, wcs

def get_mult_fact(data_model, qid, ivar=False):
    raise NotImplementedError('Currently do not support loading calibration factors')
#     """Get a map calibration factor depending on the array and 
#     map type.

#     Parameters
#     ----------
#     data_model : soapack.DataModel
#          DataModel instance to help load raw products
#     qid : str
#         Map identification string.
#     ivar : bool, optional
#         If True, load the factor for the inverse-variance map for the
#         qid and split. If False, load the factor for the source-free map
#         for the same, by default False.

#     Returns
#     -------
#     float
#         Calibration factor.
#     """
#     if ivar:
#         return 1/data_model.get_gain(qid)**2
#     else:
#         return data_model.get_gain(qid)
