# `S`imons `O`bservatory `FI`le`N`ame `D`epot
Simple, extendable framework for loading generic products from disk.

## Contact
For any questions please reach out to Zach Atkins (email: [zatkins@princeton.edu](mailto:zatkins@princeton.edu), github: [@zatkins2](https://github.com/zatkins2)).

## Dependencies
Currently:
* from `simonsobs`: [`pixell`](https://github.com/simonsobs/pixell)

All other dependencies (e.g. `numpy` etc.) are required by packages listed here, especially by `pixell`.

## Installation
Clone this repo and `cd` to `/path/to/sofind/`:
```shell
$ pip install .
```
or 
```shell
$ pip install -e .
```
to see changes to source code automatically updated in your environment.

## Quick Setup
All users must create a file `.sofind_config.yaml` in their system's `HOME` directory. This file encodes the location on their system of products implemented in the `sofind` package. It also groups a set of these locations under data model "names," such as `act_dr6.01` (see `sofind/datamodels`). This way, different data models may have their products in different locations on the system. 

To facilitate setup, we have provided some `.sofind_config.yaml` files for common public systems, such as `NERSC`, in the `sofind_configs` folder for users to copy. If you are on one of these systems, all you need to do is copy the relevant file to `~/.sofind_config.yaml`!

## Usage
All you need in your code is the following (e.g. for the `act_dr6v3` data model):
```python
from sofind import DataModel

# use the from_config method to specify the data model at runtime
dm = DataModel.from_config('act_dr6v3')

# a qid is an identifier tag for a dataset, like a detector array
my_qid = 'pa4a'

# have fun
my_default_map_filename = dm.get_map_fn(my_qid, **more_kwargs)
my_pwv_split_map = dm.read_map(my_qid, subproduct='pwv_split', **more_kwargs)
my_beam = dm.read_beam(my_qid, **more_kwargs)
```
Users should only ever interface with the high-level `DataModel` class. This class inherits from all implemented `sofind` products! Available `qids` for a particular data model or product are available either by following the `qids_config` entry in the data model config itself (referring to a particular file in `sofind/qids`) or should be documented for the product (see, e.g., the `sofind/products/maps` README file).

## Detailed Setup
If you would like to better understand the meaning of your `.sofind_config.yaml` file or the structure of `sofind`, keep reading! This could be helpful in case changes are necessary, or if you'd like to install `sofind` on your laptop, for instance.

We'll start with a basic example. Let's assume you wish to interact with the `act_dr6v3` data model. Let's also assume that `sofind` currently implements map and beam products in `sofind/products/maps` and `sofind/products/beams`, along with possibly more products in different `sofind/products` modules as well. Then, your `.sofind_config.yaml` file might look like this:
```yaml
act_dr6v3:
    maps:
        default_path: "/path/to/default/maps/on/this/system/"
        pwv_split_path: "/path/to/pwv_split/maps/on/this/system/"
    beams:
        default_path: "/path/to/default/beams/on/this/system/"
```
First, we must have a block for the data model (`act_dr6v3`) we wish to use. Under this block, we must have "product"-level blocks for each product implementation (e.g. `maps`, `beams`) we wish to interact with. The name of these "product" blocks must match the module in which the product is implemented (e.g. `maps` for `sofind/products/maps`). Finally, within each "product" block, we may have several "subproducts." These "subproducts" share the same code interface (again, in `sofind/products/maps/__init__.py`), but may just be different "kinds" of maps.

The name of each "subproduct" is indicated by the words before `_path`. The system path for that product/subproduct pair is then listed. For example, all the possible files for the `pwv_split` subproduct of the `maps` product should be in the directory `"/path/to/pwv_split/maps/on/this/system/"`.

A few notes:
* A user's `.sofind_config.yaml` may have several different "data model" blocks, so that they can select from their desired data model at runtime.
* It is *not* necessary to have a "product" block for every product in a data model. In this example, if you omit the `beams` block, then a call to load a beam from disk (for any beam "subproduct") would raise an error, but the other products, like `maps`, would be unaffected. Thus, users do not need to make any other changes to `sofind` or their setup if some products do not exist on their system.  
* It is *not* necessary to have a "subproduct" path for every subproduct in a product. In this example, if you omit the `pwv_split_path` from the `maps` block, then a call map methods with the keyword argument `subproduct='pwv_split'` would raise an error without affecting other subproducts. Thus, users do not need to make any other changes to `sofind` or their setup if some subproducts do not exist on their system.  
* For many products (but not all!) the default "subproduct" passed to the methods in each product implementation (e.g. `read_map` in `sofind/products/maps/__init__.py`) is called "default". Thus, many (but not all!) "product" blocks in a `.sofind_config.yaml` file will have, at minimum, a `default_path`. However, there is nothing special about this name as far as whether it must be present or may be omitted from the `.sofind_config.yaml` file.

## If you would like to contribute a product to `sofind`
There are four steps:
1. Create a new product folder in the `sofind/products` directory. Add to this folder a python module named `__init__.py`.
    * There is a minimum prescription your subclass implementation must follow. To make it easy, a template of this implementation (for a product called `HotDog`) can be copied from `sofind/products/hotdogs/__init__.py`. You should *not* delete the template class declaration or `__init__` method (but you may add to them), and you *must* modify the `sofind.products.products.Product` methods decorated with `@productmethod`. Note the template has more detail on how to implement your product class. You can also look at e.g. `actpack.products.maps.Map` for inspiration.
    * Anything beyond this minimal perscription can be added if your product has more complicated features!
2. Make sure your product is imported directly by the `sofind.products` package. For instance, if your module was named `hotdogs` and your particular class named `HotDog`, then add this line to `sofind.products.__init__.py`:

    ```python
    from .hotdogs import HotDog
    ```
3. Add a config (or multiple configs if you have multiple product versions, or subproducts, etc.) to `sofind/products/{module_name}`. Following the hotdog example, there is a config file `hotdog_example.yaml` in `sofind/products/hotdogs`.
    * This must be a `.yaml` file.
    * This should contain any information to help get filenames for your product or load them from disk, such as a template filename. For instance, given a set of keyword arguments `array='pa6', freq='f090', num_splits=8, condiment='mustard'`, the `hotdog_file_template` string in `hotdog_example.yaml` would format to `pa6_f090_8way_mustard.txt` (the actual formatting would occur in your `HotDog` class's `get_hotdog_fn` method).
    * You must have an `allowed_qids_configs` block. If your subproduct is agnostic to qids, this can be `all`; otherwise, it must list the individual `qids_config` files (in `sofind/qids`) that this subproduct may work with.
    * You must have an `allowed_qids` block. If your product methods use a `qid` to provide keywords to filename templates, then the permissible `qid`(s) for that product must be listed here. May also be `all` or left blank if no `qid`(s) work with your subproduct. For instance, a call to `HotDog.read_hotdog` will raise an error if `hotdog_example.yaml` is used to configure the calling `DataModel` instance and the supplied `qid` is *not* one of `pa4a`, `pa5a`, or `pa6a`.
    * You must have an `allowed_qids_extra_kwargs` block. If your template filename requires additional keywords for a given `qid` than are present in any `allowed_qids_configs` files (see `sofind/qids`), those keywords would need to be added here. For instance, the `act_dr6_default_qids.yaml` file only contains `array`, `freq`, `patch`, and `daynight` keywords. The `num_splits` keyword required for the `hotdog_file_template` is thus added for each permissible qid directly in `hotdog_example.yaml`, e.g.:
        ```yaml
        allowed_qids_extra_kwargs:
            pa6a:
                num_splits: 8
        ```
        The `allowed_qids_extra_kwargs` block may be empty if there are no extra keywords to add for any of the `allowed_qids`.
4. Clearly document product implementations and product configs. For example, see the docstrings in the `Map` class (`sofind/products/maps/__init__.py`) as well as the `maps` readme (`sofind/products/maps/README.md`).
    
Please commit and push your contribution to a new branch and open a PR on github! If you are updating an old config, please include it under a new file altogether so that historical products may still be loaded at runtime.
    
## If you would like to contribute a data model to `sofind`
There are one (maybe two) steps:
1. Create a new data model config in `sofind/datamodels`.
    * Like the `.sofind_config.yaml` file, this config must have a block for each product this data model will load. Note, also like the `.sofind_config.yaml` file, it is not necessary to have a block for every product in `sofind`, only those that will be functional in this data model. The same goes for subproducts of a product -- include only those that will be functional in this data model. To add a subproduct, include an entry under the associated product block like:
        ```yaml
        data_model_name:
            prod:
                subprod_config: config.yaml
        ``` 
        where `prod` and `subprod` are the names of the product and subproduct that may be called by the `DataModel`.
    * This config file must also have an entry for a `qids_config` (at the top-level), indicating one of the qid config files under `sofind/qids`.
2. Only if one of the included qid config files are not sufficient for your needs, you'll need to add another one with your qids.

Please commit and push your contribution to a new branch and open a PR on github! If you are updating an old config, please include it under a new file altogether so that historical products may still be loaded at runtime.
