# `S`imons `O`bservatory `FI`le`N`ame `D`epot
Simple, extendable framework for loading generic products from disk.

## Contact
For any questions please reach out to Zach Atkins (email: [zatkins@princeton.edu](mailto:zatkins@princeton.edu), github: [@zatkins2](https://github.com/zatkins2)).

## Dependencies
Currently:
* from `simonsobs`: [`pixell`](https://github.com/simonsobs/pixell), [`mnms`](https://github.com/simonsobs/mnms)

All other dependencies (e.g. `numpy` etc.) are required by packages listed here, especially by `pixell`.

## Installation
Clone this repo and the `mnms` repo. `mnms` and `sofind` are install-time circular dependencies. Thus, they need to be installed in the same call to pip:
```shell
$ pip install path/to/mnms path/to/sofind
```
or 
```shell
$ pip install -e path/to/mnms -e path/to/sofind
```
to see changes to source code automatically updated in your environment.

## Quick Setup
Users only need to set one environment variable, `SOFIND_SYSTEM`, corresponding to the name of the cluster they are working on. Supported systems are listed in `sofind/systems.py` (e.g. `della`, `perlmutter`).

## Usage
All you need in your code is the following (e.g. for the `act_dr6v4` data model):
```python
from sofind import DataModel

# use the from_config method to specify the data model at runtime
dm = DataModel.from_config('act_dr6v4')

# a qid is an identifier tag for a dataset, like a detector array
my_qid = 'pa4a'

# have fun
my_default_map_filename = dm.get_map_fn(my_qid, **more_kwargs)
my_el_split_map = dm.read_map(my_qid, subproduct='el_split', el_split='el1')
```
Users should only ever interface with the high-level `DataModel` class. This class inherits from all implemented `sofind` products! Available `qids` for a particular data model or product are available either by following the `qids_config` entry in the data model config itself (referring to a particular file in `sofind/qids`) or should be documented for the product (see, e.g., the `sofind/products/maps` README file).

## If you would like to contribute a product to `sofind`
There are four steps:
1. Create a new product folder in the `sofind/products` directory. Add to this folder a python module named `__init__.py`.
    * There is a minimum prescription your subclass implementation must follow. To make it easy, a template of this implementation (for a product called `HotDog`) can be copied from `sofind/products/hotdogs/__init__.py`. You should *not* delete the template class declaration or `__init__` method (but you may add to them), and you *must* modify the `sofind.products.products.Product` methods decorated with `@productmethod`. Note the template has more detail on how to implement your product class. You can also look at e.g. `sofind.products.maps.Map` for inspiration.
    * Anything beyond this minimal perscription can be added if your product has more complicated features!
2. Make sure your product is imported directly by the `sofind.products` package. For instance, if your module was named `hotdogs` and your particular class named `HotDog`, then add this line to `sofind.products.__init__.py`:

    ```python
    from .hotdogs import HotDog
    ```
3. Add a config (or multiple configs if you have multiple product versions, or subproducts, etc.) to `sofind/products/{module_name}`. Following the hotdog example, there is a config file `hotdog_example.yaml` in `sofind/products/hotdogs`.
    * This must be a `.yaml` file.
    * You must have a `system_paths` block. This will have entries for a subset of the available clusters in `sofind/systems.py`. Each entry will point to a path giving the directory on that system in which the product files are located.
    * You must have an `allowed_qids_configs` block. If your subproduct is agnostic to qids, this can be `all`; otherwise, it must list the individual `qids_config` files (in `sofind/qids`) that this subproduct may work with.
    * You must have an `allowed_qids` block. If your product methods use a `qid` to provide keywords to filename templates, then the permissible `qid`(s) for that product must be listed here. May also be `all` or left blank if no `qid`(s) work with your subproduct. For instance, a call to `HotDog.read_hotdog` will raise an error if `hotdog_example.yaml` is used to configure the calling `DataModel` instance and the supplied `qid` is *not* one of `pa4a`, `pa5a`, or `pa6a`.
    * You must have an `allowed_qids_extra_kwargs` block. If your template filename requires additional keywords for a given `qid` than are present in any `allowed_qids_configs` files (see `sofind/qids`), those keywords would need to be added here. For instance, the `act_dr6_default_qids.yaml` file only contains `array`, `freq`, `patch`, and `daynight` keywords. The `num_splits` keyword required for the `hotdog_file_template` is thus added for each permissible qid directly in `hotdog_example.yaml`, e.g.:
        ```yaml
        allowed_qids_extra_kwargs:
            pa6a:
                num_splits: 8
        ```
        The `allowed_qids_extra_kwargs` block may be empty if there are no extra keywords to add for any of the `allowed_qids`.
    * This should contain any information to help get filenames for your product or load them from disk, such as a template filename. For instance, given a set of keyword arguments `array='pa6', freq='f090', num_splits=8, condiment='mustard'`, the `hotdog_file_template` string in `hotdog_example.yaml` would format to `pa6_f090_8way_mustard.txt` (the actual formatting would occur in your `HotDog` class's `get_hotdog_fn` method).
4. Clearly document product implementations and product configs. For example, see the docstrings in the `Map` class (`sofind/products/maps/__init__.py`) as well as the `maps` readme (`sofind/products/maps/README.md`).
    
Please commit and push your contribution to a new branch and open a PR on github! If you are updating an old config, please include it under a new file altogether so that historical products may still be loaded at runtime.
    
## If you would like to contribute a data model to `sofind`
There are one (maybe two) steps:
1. Create a new data model config in `sofind/datamodels`.
    * This config must have a block for each product this data model will load. Note, it is not necessary to have a block for every product in `sofind`, only those that will be functional in this data model. The same goes for subproducts of a product -- include only those that will be functional in this data model. To add a subproduct, include an entry under the associated product block like:
        ```yaml
        prod:
            subprod_config: config.yaml
        ``` 
        where `prod` and `subprod` are the names of the product and subproduct that may be called by the `DataModel`.
    * This config file must also have an entry for a `qids_config` (at the top-level), indicating one of the qid config files under `sofind/qids`.
2. Only if one of the included qid config files are not sufficient for your needs, you'll need to add another one with your qids.

Please commit and push your contribution to a new branch and open a PR on github! If you are updating an old config, please include it under a new file altogether so that historical products may still be loaded at runtime.
