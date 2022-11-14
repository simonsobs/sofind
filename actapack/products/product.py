# This module's design gets around the fact that abstractmethods cannot be 
# "renamed" dynamically

import functools

# This is only for use in decorating Product methods, but needs to be 
# defined outside the Product class scope
def make_productmethod_decorator(productmethods_list):
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
    productmethod = make_productmethod_decorator(productmethods)

    def __init__(self, **kwargs):
        """Base class for products. Enforces subclasses implement any
        productmethods exactly once.
        """
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

    # All Product subclasses must implement any @productmethods defined below
    # @property
    # @productmethod
    # def path_key(self):
    #     pass

    @productmethod
    def get_fn(self):
        pass

    @productmethod
    def read_product(self):
        pass


# This is for use inside the declaration of each Product subclass. Every 
# product must have a list of implemented methods and an @implements 
# decorator as class attributes. I.e. one should copy these lines in the
# subclass declaration:

#     implementedmethods = []
#     implements = make_implements_decorator(implementedmethods)
def make_implements_decorator(implementedmethods_list):
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