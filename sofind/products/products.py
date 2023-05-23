# This module's design gets around the fact that abstractmethods cannot be 
# "renamed" dynamically

from sofind import utils

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
        self.qids = kwargs.pop('qids')
        self.paths = kwargs.pop('paths')

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
        module __name__: first, get the basename of __name__, e.g. 'things' from 
        'sofind.things.things'. Then, set the value under key 'things' in 
        kwargs to attributes of the same name in self.

        Parameters
        ----------
        product : str
            Name of type of product, e.g. 'maps'. Can also be a module __name__
            in which case the product is inferred from the module basename.
        kwargs : dict
            Dictionary holding values under keys corresponding to the 
            product (see function description).

        Notes
        -----
        The values retrieved from kwargs are popped out, so that after this function
        call those items are no longer in kwargs. This is why the signature is kwargs,
        not **kwargs: if the latter, then kwargs.pop(name) first builds a new
        dictionary 'kwargs' before popping. 

        Checks the product for compatibility (for each of its subproducts, see
        check_subproduct_config).
        """
        product = utils.get_producttag(product)
        
        assert product not in ['qids', 'paths'], \
            "Cannot have a product named 'qids' or 'paths'"
        
        product_dict = kwargs.pop(product, None)

        if product_dict is not None:
            for subproduct, subproduct_dict in product_dict.items():
                self.check_subproduct_config(product, subproduct, subproduct_dict)

            setattr(self, product, product_dict)     

    def check_subproduct_config(self, product, subproduct, subproduct_dict):
        """Ensure the subproduct configuration file is compatible. 

        Parameters
        ----------
        product : str
            Name of type of product, e.g. 'maps'. Can also be a module __name__
            in which case the product is inferred from the module basename.
        subproduct : str
            The specific subproduct.
        subproduct_dict : dict
            A dictionary corresponding to a subproduct configuration file. Should
            contain 'allowed_qids_configs', 'allowed_qids',
            'allowed_qids_extra_kwargs' entries.

        Raises
        ------
        AssertionError
            If 'allowed_qids_configs' is empty in the configuration file.

        AssertionError
            If an allowed_qid is not in any of the specified allowed_qid_configs.
            Both 'allowed_qid' and 'allowed_qid_configs' may be 'all'.

        AssertionError
            If any qid in 'allowed_qids_extra_kwargs' is not in 'allowed_qids'.
        """
        product = utils.get_producttag(product)

        # check that allowed_qids_configs is not None
        assert subproduct_dict['allowed_qids_configs'] is not None, \
            f'No allowed_qids_configs for product {product}, subproduct {subproduct}'
        
        # check each allowed_qid is in each allowed_qids_configs
        allowed_qids_configs = subproduct_dict['allowed_qids_configs']
        if allowed_qids_configs == 'all':
            allowed_qids_configs = os.listdir(utils.get_package_fn('sofind', 'qids'))

        allowed_qids = subproduct_dict['allowed_qids']

        if allowed_qids is not None and allowed_qids != 'all':
            for allowed_qids_config in allowed_qids_configs:

                # need to get the contents from the config_name
                allowed_qids_fn = utils.get_package_fn('sofind', f'qids/{allowed_qids_config}')
                allowed_qids_dict = utils.config_from_yaml_file(allowed_qids_fn)

                for qid in allowed_qids:
                    assert qid in allowed_qids_dict, \
                        f'qid {qid} allowed by product {product}, subproduct ' + \
                        f'{subproduct} configuration file, but not in ' + \
                        f'{allowed_qids_config}'

        # check each allowed_qid_extra_kwarg key is an allowed_qid
        if subproduct_dict['allowed_qids_extra_kwargs'] is not None:
            assert allowed_qids is not None, \
                f'{product}, subproduct {subproduct} configuration file has '+ \
                'allowed_qids_extra_kwargs but allowed_qids is None'

            if allowed_qids != 'all':
                for qid in subproduct_dict['allowed_qids_extra_kwargs']:
                    assert qid in allowed_qids, \
                        f'qid {qid} has extra kwargs in product {product}, subproduct ' + \
                        f'{subproduct} configuration file, but not is not an allowed_qid'

    def get_qid_kwargs_by_subproduct(self, qid, product, subproduct):
        """Return a dict of key-value pairs for this qid. The dict is a merger
        of any default pairs in this datamodel's qid_dict, as well as any
        additional pairs specified in a particular subproduct's configuration
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

        Raises
        ------
        AssertionError
            If the suproduct has no allowed qids, signified by an empty
            'allowed_qids' block in the config file.

        AssertionError
            If there are allowed qids, but the called qid is not one of
            them.

        KeyError
            If qid is not in the data_model qids_dict.
        """
        subproduct_dict = self.get_subproduct_dict(product, subproduct)

        # check allowed_qids is not None
        assert subproduct_dict['allowed_qids'] is not None, \
            f'No allowed qids for product {product}, subproduct {subproduct}'

        # check qid is in the allowed_qids or 'all'
        if qid not in subproduct_dict['allowed_qids']:
            assert subproduct_dict['allowed_qids'] == 'all', \
                f'qid {qid} not allowed by product {product}, subproduct ' + \
                f'{subproduct} configuration file'

        qid_dict = self.qids[qid].copy()
        if subproduct_dict['allowed_qids_extra_kwargs'] is not None:
            qid_subproduct_dict = subproduct_dict['allowed_qids_extra_kwargs'].get(qid, {})
            qid_dict.update(qid_subproduct_dict.copy())

        return qid_dict
                
    def get_product_dict(self, product):
        """Get the set of subproduct dictionaries under a product type, such as
        'maps' or 'beams'.

        Parameters
        ----------
        product : str
            Name of type of product, e.g. 'maps'. Can also be a module __name__
            in which case the product is inferred from the module basename.

        Returns
        -------
        dict
            A mapping from subproduct names in this product type to a dict of
            information for each subproduct.

        Raises
        ------
        LookupError
            If a product type is not in this datamodel.
        """
        product = utils.get_producttag(product)
        try:
            product_dict = getattr(self, product)
        except AttributeError as e:
            raise LookupError(
                f'Product {product} not in datamodel configuration file'
                ) from e
        
        return product_dict                    
            
    def get_subproduct_dict(self, product, subproduct):
        """Get the subproduct dictionary for this subproduct of a given product
        type. The subproduct dictionary will hold things like a filename
        template for this subproduct, and any qid updates particular to this 
        subproduct.

        Parameters
        ----------
        product : str
            Name of type of product, e.g. 'maps'. Can also be a module __name__
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
            If a subproduct under the product type is not in this datamodel.
        """
        product_dict = self.get_product_dict(product)
        try:
            subproduct_dict = product_dict[subproduct]
        except KeyError as e:
            product = utils.get_producttag(product)
            raise LookupError(
                f'Product {product}, subproduct {subproduct} not in '
                'datamodel configuration file'
            ) from e
        return subproduct_dict

    def get_subproduct_path(self, product, subproduct):
        """Get the system path to a directory holding the files for this
        subproduct of a given product type. 

        Parameters
        ----------
        product : str
            Name of type of product, e.g. 'maps'. Can also be a module __name__
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
            their .sofind_config.yaml file under this datamodel, indicating
            they do not want to interact with these subproducts.
        """
        try:
            product = utils.get_producttag(product)
            subproduct_path = self.paths[product][subproduct]
        except KeyError as e:
            raise LookupError(
                f'Product {product}, subproduct {subproduct} not in user '
                f'.sofind_config.yaml file, cannot get {product}, {subproduct} '
                'filename'
            ) from e
        return subproduct_path