from pixell import enmap
import numpy as np
import yaml
import h5py

import io
import os, sys
from itertools import product

# adapted from soapack.interfaces
def config_from_yaml_file(filename):
    """Return a yaml file contents as a dictionary.

    Parameters
    ----------
    filename : io.TextIOBase or path-like
        Either an io.TextIOBase stream or a system path.

    Returns
    -------
    dict
        Contents of file.
    """
    if not isinstance(filename, io.TextIOBase):
        with open(filename, 'r') as f:
            return config_from_yaml_file(f)
    
    filename.seek(0)
    return yaml.safe_load(filename)

def config_from_hdf5_file(filename, address='/', op=lambda x: x):
    """Return a dictionary of the attributes at hfile[address].attrs.

    Parameters
    ----------
    filename : h5py.Group or path-like
        Either an h5py.Group stream or a system path.
    address : str, optional
        Group in hfile to look for config, by default the root.
    op : callable, optional
        How to transform the values under each key in hfile[address].attrs in
        the output, by default the identity. This may change depending on the 
        format of how the values were written (e.g., if yaml-encoded strings,
        one might use op=yaml.safe_load).

    Returns
    -------
    dict
        dict(hfile[address].attrs)
    """
    if not isinstance(filename, h5py.Group):
        with h5py.File(filename, 'r') as hfile:
            return config_from_hdf5_file(hfile, address=address)
    
    idict = filename[address].attrs
    odict = {}
    for k, v in idict.items():
        odict[k] = op(v)
    return odict

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

    >>> from sofind.utils import get_sytem fn
    >>> home_config = '.mnms_config' # could also use full name, '.mnms_config.yaml'
    >>> basename = 'sims/sim_001.fits' # this file lives inside the the private_path, for example
    >>> config_keys=['mnms', 'private_path'] # get the private_path
    >>> fn = get_system_fn(home_config, basename, config_keys=config_keys)
    >>> print(fn)
    >>> '/scratch/gpfs/zatkins/data/ACTCollaboration/mnms/sims/sim_001.fits'
    """
    if not home_config.endswith('.yaml'):
        home_config += '.yaml'

    if config_keys is None:
        config_keys = []

    home_config_dict = config_from_yaml_file(
        os.path.join(os.environ['HOME'], home_config)
        )
    
    out = home_config_dict
    for key in config_keys:
        out = out[key]

    return os.path.join(out, basename)

def get_protected_fn(*fns, no_fn_collisions=True, write_to_fn_idx=None):
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
                f'Want to write to {write_fn}\n\nbut at least one of the following exists:\n{err_str}'
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

# This creates a mapping between Product subclasses and their product tag
def get_producttag(product):
    """Return product.split('.')[-1]"""
    return product.split('.')[-1]

def get_super_qids_from_qids_and_subproduct_kwargs(*qids, **subproduct_kwargs):
    """Generate 'super_qids' from qids and a dictionary that maps keys of
    subproduct_kwargs to an iterable of their possible values. 'super_qids'
    are the outer product of the possible values for each key, and then the 
    qids (starting with the subproduct_kwargs from left to right in insertion
    order).

    For example, if qids is ('pa5a', 'pa5b'), and subproduct_kwargs is
    {'el_split': ['el1', 'el2', 'el3'], 'something_else': [0, 1]}, then
    the following 12 tuples form the ordered 'super_qids':

    ({'el_split': 'el1', 'something_else': 0}, 'pa5a'),
    ({'el_split': 'el1', 'something_else': 0}, 'pa5b'),
    ({'el_split': 'el1', 'something_else': 1}, 'pa5a'),
    ({'el_split': 'el1', 'something_else': 1}, 'pa5b'),
    ({'el_split': 'el2', 'something_else': 0}, 'pa5a'),
    ({'el_split': 'el2', 'something_else': 0}, 'pa5b'),
    ({'el_split': 'el2', 'something_else': 1}, 'pa5a'),
    ({'el_split': 'el2', 'something_else': 1}, 'pa5b'),
    ({'el_split': 'el3', 'something_else': 0}, 'pa5a'),
    ({'el_split': 'el3', 'something_else': 0}, 'pa5b'),
    ({'el_split': 'el3', 'something_else': 1}, 'pa5a'),
    ({'el_split': 'el3', 'something_else': 1}, 'pa5b')

    Parameters
    ----------
    qids : str or iterable of str
        One or more array qids for this model.
    subproduct_kwargs : (key, iterable) mapping, optional
        Any additional keyword arguments required to load products from
        disk, or to format model and sim filenames. The iterable for each
        key should list, in order, all possible values the key can take.

    Returns
    -------
    list
        List of the super_qids.
    """
    super_qids = []
    for vals in product(*subproduct_kwargs.values(), qids):
        _subproduct_kwargs = dict(zip(subproduct_kwargs.keys(), vals[:-1]))
        qid = vals[-1]

        # e.g. ({'inout_split': 'inout1', 'el_split': 1}, 'pa5a')
        super_qid = (_subproduct_kwargs, qid)
        super_qids.append(super_qid)
    
    return super_qids