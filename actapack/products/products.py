# This module's design gets around the fact that abstractmethods cannot be 
# "renamed" dynamically

from actapack import utils

import functools

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

    # This is a helper function to package-up all the lines (and the only lines)
    # of code to be run in a Product subclass's __init__method
    def set_attrs(self, product, kwargs):
        """Assign attributes to self from kwargs based on product. If product is a
        module filename: first, get the extension-less basename of filename, e.g.
        'things' from '/home/zatkins/things.py'. Then, set the value under key
        'things' in kwargs to attributes of the same name in self.

        Parameters
        ----------
        product : str
            Name of type of product, e.g. 'maps'. Can also be a path to a module
            in which case the product is inferred from the module basename.
        kwargs : dict
            Dictionary holding values under keys corresponding to the 
            product (see function description).

        Notes
        -----
        The values retrieved from kwargs are popped out, so that after this function
        call those items are no longer in kwargs.

        If product is not in kwargs, then a value of {} is assigned.
        """
        producttag = utils.get_producttag(product)
        setattr(self, producttag, kwargs.pop(producttag, {}))

    def get_product_dict(self, product):
        """Get the set of subproduct dictionaries under a product type, such as
        'maps' or 'beams'.

        Parameters
        ----------
        product : str
            Name of type of product, e.g. 'maps'. Can also be a path to a module
            in which case the product is inferred from the module basename.

        Returns
        -------
        dict
            A mapping from subproduct names in this product type to a dict of
            information for each subproduct.

        Raises
        ------
        KeyError
            If a user has not added the product type to their
            .actapack_config.yaml file under this datamodel, indicating they 
            do not want to interact with these products.
        """
        producttag = utils.get_producttag(product)
        product_dict = getattr(self, producttag)
        if product_dict == {}:
            raise KeyError(
                f'Product {producttag} not in user .actapack_config.yaml file, '
                f'cannot get any {producttag} filename'
                )
        return product_dict

    def get_subproduct_dict(self, product, subproduct):
        """Get the subproduct dictionary for this subproduct of a given product
        type. The subproduct dictionary will hold things like a filename
        template for this subproduct, and any qid updates particular to this 
        subproduct.

        Parameters
        ----------
        product : str
            Name of type of product, e.g. 'maps'. Can also be a path to a module
            in which case the product is inferred from the module basename.
        subproduct : str
            The specific subproduct.

        Returns
        -------
        dict
            A dictionary of information for this subproduct.

        Raises
        ------
        KeyError
            If a user has not added the subproduct under the product type to
            their .actapack_config.yaml file under this datamodel, indicating
            they do not want to interact with these subproducts.
        """
        product_dict = self.get_product_dict(product)
        try:
            subproduct_dict = product_dict[f'{subproduct}_dict']
        except KeyError:
            producttag = utils.get_producttag(product)
            raise KeyError(
                f'Product {producttag}, subproduct {subproduct} not in user '
                f'.actapack_config.yaml file, cannot get {producttag}, {subproduct} '
                'filename'
            )
        return subproduct_dict

    def get_subproduct_path(self, product, subproduct):
        """Get the system path to a directory holding the files for this
        subproduct of a given product type. 

        Parameters
        ----------
        product : str
            Name of type of product, e.g. 'maps'. Can also be a path to a module
            in which case the product is inferred from the module basename.
        subproduct : str
            The specific subproduct.

        Returns
        -------
        str
            Path to directory.

        Raises
        ------
        KeyError
            If a user has not added the subproduct under the product type to
            their .actapack_config.yaml file under this datamodel, indicating
            they do not want to interact with these subproducts.
        """
        product_dict = self.get_product_dict(product)
        try:
            subproduct_path = product_dict[f'{subproduct}_path']
        except KeyError:
            producttag = utils.get_producttag(product)
            raise KeyError(
                f'Product {producttag}, subproduct {subproduct} not in user '
                f'.actapack_config.yaml file, cannot get {producttag}, {subproduct} '
                'filename'
            )
        return subproduct_path

    def get_qid_kwargs_by_suproduct(self, qid, product, subproduct):
        """Return a set of keyword arguments for this qid. The set is a merger
        of any default keywords in this datamodel's qid_dict, as well as any
        additional keywords specified in a particular subproduct's configuration
        file, if any.

        Parameters
        ----------
        qid : str
            Dataset identification string.
        product : str
            The type of product, e.g. 'maps' or 'beams'.
        subproduct : str
            The specific subproduct.

        Returns
        -------
        dict
            A set of keywords for the requested qid, such as its array, frequency,
            etc.
        """
        subprod_dict = self.get_subproduct_dict(product, subproduct)

        out = self.qids_dict[qid].copy()
        out.update(subprod_dict.get(qid, {}).copy())

        return out