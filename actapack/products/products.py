# This module's design gets around the fact that abstractmethods cannot be 
# "renamed" dynamically

import functools
import os


# This is only for use in decorating Product methods, but needs to be 
# defined outside the Product class scope
def get_productmethod_decorator(productmethods_list):
    """Make a decorator that adds the decorated function to the specified
    list. The decorated function then only raises a NotImplementedError
    if called.

    Parameters
    ----------
    productmethods_list : list
        List of decorated functions.

    Returns
    -------
    function
        The @productmethod decorator in the calling scope.
    """
    def decorator(base_func):
        productmethods_list.append(base_func.__name__)
        @functools.wraps(base_func)
        def wrapper(*args, **kwargs):
            raise NotImplementedError('This is an abstract productmethod')
        return wrapper
    return decorator


# All products must inherit from Product and implement its productmethods
class Product: 

    # Methods decorated with productmethod will be added to the
    # productmethods list
    productmethods = []
    productmethod = get_productmethod_decorator(productmethods)

    def __init__(self, **kwargs):
        """Base class for products. Enforces subclasses implement any
        productmethods exactly once.
        """
        self.qids_dict = kwargs.pop('qids_dict')

        for product in Product.__subclasses__():
            for method_name in self.productmethods:
                num_implementations = 0
                for implementedmethod_name in product.implementedmethods: 
                    if implementedmethod_name == method_name:
                        num_implementations += 1

                assert num_implementations == 1, \
                    f'Product {product.__name__} must have exactly 1 ' + \
                    f'implementation of {method_name}; found '+ \
                    f'{num_implementations}'

    @productmethod
    def get_fn(self):
        pass

    @productmethod
    def read_product(self):
        pass


# This creates a mapping between Product subclasses and their product tag
def get_producttag_by_filename(filename):
    """Return os.path.splitext(os.path.basename(filename))[0]"""
    return os.path.splitext(os.path.basename(filename))[0]


# This is a helper function to package-up all the lines (and the only lines)
# of code to be run in a Product subclass's __init__method
def set_attrs_by_filename(self, filename, kwargs):
    """Assign attributes in self from kwargs based on filename. First, get the
    extension-less basename of filename, e.g. 'test' from
    '/home/zatkins/test.py'. Then, set the value under keys 'test_path' and 
    'test_dict' in kwargs to attributes of the same name in self.

    Parameters
    ----------
    filename : str
        Path to a file, e.g. the calling module of this function.
    kwargs : dict
        Dictionary holding values under keys corresponding to the 
        filename (see function description).

    Notes
    -----
    The values retrieved from kwargs are popped out, so that after this function
    call those items are no longer in kwargs.
    """
    producttag = get_producttag_by_filename(filename)
    setattr(self, f'{producttag}_path', kwargs.pop(f'{producttag}_path', None))
    setattr(self, f'{producttag}_dict', kwargs.pop(f'{producttag}_dict', None))


# This is for use inside the declaration of each Product subclass. Every 
# product must have a list of implemented methods and an @implements 
# decorator as class attributes. I.e. one should copy these lines in the
# subclass declaration:

#     implementedmethods = []
#     implements = make_implements_decorator(implementedmethods)
def get_implements_decorator(implementedmethods_list):
    """Make a decorator that adds the decorated function to the specified
    list. The decorated function itself is unaltered.

    Parameters
    ----------
    implementedmethods_list : list
        List of decorated functions.
    
    Returns
    -------
    function
        The @implements decorator in the calling scope.
    """
    def implements(base_func):
        def decorator(sub_func):
            implementedmethods_list.append(base_func.__name__)
            return sub_func
        return decorator
    return implements