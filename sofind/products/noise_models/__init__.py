from ..products import Product, get_implements_decorator
from sofind import utils

from pixell import enmap
import h5py
import yaml

import os
import time
import warnings
from abc import ABC, abstractmethod


class NoiseModel(Product):

    implementedmethods = []
    implements = get_implements_decorator(implementedmethods)
    
    def __init__(self, **kwargs):
        self.set_attrs(__name__, kwargs)
        super().__init__(**kwargs)

    @implements(Product.get_fn)
    def get_noise_fn(self, *args, which='sim', subproduct='default', **kwargs):
        subprod_dict = self.get_subproduct_dict(__name__, subproduct)
        fn = 'blah'

        # return the full system path to the file
        subprod_path = self.get_subproduct_path(__name__, subproduct)
        return os.path.join(subprod_path, fn)

    @implements(Product.read_product)
    def read_noise(self, *args, which='sim', subproduct='default', **kwargs):
        fn = self.get_map_fn(*args, subproduct=subproduct, **kwargs)

        return enmap.read_map(fn)