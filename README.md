# actapack
Simple, extendable framework for loading ACT products from disk.

## Dependencies
Currently:
* from `simonsobs`: `pixell`

All other dependencies (e.g. `numpy` etc.) are required by packages listed here, especially by `pixell`.

## Installation
Clone this repo and `cd` to `/path/to/actapack/`:
```
$ pip install .
```
or 
```
$ pip install -e .
```
to see changes to source code automatically updated in your environment.

## Setup
All users must create a file `.actapack_config.yaml` in their system's `HOME` directory. This file encodes the location on the system of all products implemented in the `actapack` package. It also groups a set of product locations under data model "names," such that different data models may have their products in different locations.

For instance, let's assume the products currently implemented (see `actapack/products`) are in `map.py` and `beam.py`. If a user wishes to interact with the `dr6_default` data model, then their `.actapack_config.yaml` file must contain the following block:
```
dr6_default:
    map_path: "/path/to/maps/on/this/system/"
    beam_path: "/path/to/maps/on/this/system/"
```
where the word before the `_path` for each product must match the module names of those product implementations.

## Usage
All you need in your code is the following (e.g. for the `dr6_default` data model):
```
from actapack import DataModel

dm = DataModel.from_config('dr6_default')

mymap = dm.read_map(...)
mybeam_fn = dm.get_beam_fn(...)
```

## If you would like to contribute a product to `actapack`
There are three steps:
1. Create a new product module in the `actapack/products` directory.
    * The module should only contain a subclass of the `actapack.products.product.Product` class.
    * There is a set prescription your subclass implementation must follow. To make it easy, a template of this implementation (for a product called `HotDog`) can be copied from `actapack.products.__init__.py`. You should *only* modify the class name and the exposed methods (not the class declaration or `__init__` method). Note the template has more detail on how to implement your product class. You can also look at e.g. `actpack.products.map.Map` for inspiration.
2. Make sure your product is imported directly by the `actapack.products` package. For instance, if your module was named `hotdog.py` and your product class in that module was `HotDog`, add either of these lines to `actapack.products.__init__.py`:

    ```
    from .hotdog import *
    # or
    from .hotdog import HotDog
    ```
3. Add a config (or multiple configs if you have multiple product versions etc.) to `actapack/configs/product_configs/{module_name}/`. Following the hotdog example, there is a config file `hotdog_template.yaml` in `actapack/configs/product_configs/hotdog/`.
    * This must be a `.yaml` file.
    * This should contain any information to help get filenames for your product or load them from disk. For instance, given a set of keyword arguments `array='pa6', freq='f090', num_splits=8, condiment='mustard'`, the `hotdog_file_template` in `hotdog_template.yaml` would populate to `pa6_f090_8way_mustard.txt` (the actual implementation of that population would happen in your `HotDog` class's `get_hotdog_fn` method).
    
Please commit and push your contribution to a new branch and open a PR on github!
    
## If you would like to contribute a data model to `actapack`
There are one (maybe two) steps:
1. Create a new data model config in `actapack/configs/datamodel_configs/`.
    * Like your `.actapack_config.yaml` file, this config must have an entry for each implemented product, where now the entry is `{module_name}_dict`. 
    * It must also have an entry for a `qid_dict`, indicating one of the qid config files under `actapack/configs/qid_configs/`.
    * Note: for each of the above, one could also add the full dictionary of information by hand, rather than pointing to a config file.
2. Only if one of the included qid config files is not sufficient for your needs, you'll need to add another one with your qids (or add your qids to what's already there).

Please commit and push your contribution to a new branch and open a PR on github!
