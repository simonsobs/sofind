# This module's design gets around the fact that abstractmethods cannot be 
# easily "renamed" dynamically

from sofind import utils, systems

import functools
import os
from copy import deepcopy

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
        self.configs = kwargs.pop('configs')

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
        
        assert product not in ['qids', 'configs'], \
            "Cannot have a product named 'qids' or 'configs'"
        
        product_dict = kwargs.pop(product, None)

        if product_dict is not None:
            setattr(self, product, product_dict)     

    def check_product_config_internal_consistency(self, product):
        """Ensure the subproduct configuration file is internally consistent for
        every subproduct in this product in the datamodel. 

        Parameters
        ----------
        product : str
            Name of type of product, e.g. 'maps'. Can also be a module __name__
            in which case the product is inferred from the module basename.

        Raises
        ------
        AssertionError
            If a subproduct config lists a system that is not an sofind system.

        KeyError
            If subproduct config does not have a populated system_paths block.

        AssertionError
            If an allowed_qid is not in all of the specified allowed_qid_configs.
            Both 'allowed_qid' and 'allowed_qid_configs' may be 'all'.

        AssertionError
            If any qid in 'allowed_qids_extra_kwargs' is not in 'allowed_qids'.
        """
        try:
            product_dict = self.get_product_dict(product)
        except LookupError:
            return # if not in the data model, it is internally consistent

        for subproduct, subproduct_dict in product_dict.items():
            subproduct_config = self.get_subproduct_config(product, subproduct)
            product = utils.get_producttag(product)

            # check each listed system is in sofind systems
            try:
                for system in subproduct_dict['system_paths']:
                    assert system in systems.sofind_systems, \
                        f'product {product}, subproduct {subproduct} (config {subproduct_config}) ' + \
                        f'has system {system} but {system} not in sofind_systems: ' + \
                        f'{systems.sofind_systems}'
            except KeyError as e:
                raise KeyError(f'product {product}, subproduct {subproduct} (config {subproduct_config}) '
                            'missing system_paths') from e
            except TypeError as e:
                assert subproduct_dict['system_paths'] is None # None is OK

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
                            f'{subproduct} (config {subproduct_config}), but not in ' + \
                            f'{allowed_qids_config}'

            # check each allowed_qids_extra_kwarg key is an allowed_qid
            if subproduct_dict['allowed_qids_extra_kwargs'] is not None:
                assert allowed_qids is not None, \
                    f'product {product}, subproduct {subproduct} (config {subproduct_config}) has '+ \
                    'allowed_qids_extra_kwargs but allowed_qids is None'

                if allowed_qids != 'all':
                    for qid in subproduct_dict['allowed_qids_extra_kwargs']:
                        assert qid in allowed_qids, \
                            f'qid {qid} has extra kwargs in product {product}, subproduct ' + \
                            f'{subproduct} (config {subproduct_config}), but not is not an allowed_qid'

    def check_subproduct_config_is_subset(self, this_product, this_subproduct,
                                          this_subproduct_dict, that_product,
                                          that_subproduct, that_subproduct_dict):
        """Check that the allowed_qids_configs, allowed_qids, and
        allowed_qids_extra_kwargs of one subproduct config are a subset of
        those of another subproduct config.

        Parameters
        ----------
        this_product : str
            Test name of type of product, e.g. 'maps'. Can also be a module __name__
            in which case the product is inferred from the module basename.
        this_subproduct : str
            The test subproduct.
        this_subproduct_dict : dict
            A dictionary corresponding to the test subproduct configuration file. Should
            contain 'allowed_qids_configs', 'allowed_qids',
            'allowed_qids_extra_kwargs' entries.
        that_product : str
            Target name of type of product, e.g. 'maps'. Can also be a module __name__
            in which case the product is inferred from the module basename.
        that_subproduct : str
            The target subproduct.
        that_subproduct_dict : dict
            A dictionary corresponding to the target subproduct configuration file. Should
            contain 'allowed_qids_configs', 'allowed_qids',
            'allowed_qids_extra_kwargs' entries.

        Raises
        ------
        AssertionError
            If an allowed_qids_config in this subproduct is not allowed by
            that subproduct.

        AssertionError
            If an allowed_qid in this subproduct is not allowed by that
            subproduct.

        AssertionError
            If allowed_qids_extra_kwargs in this subproduct is not a subset of 
            the allowed_qids_extra_kwargs of that subproduct.

        Notes
        -----
        The allowed_qids_extra_kwargs in this subproduct cannot be None unless
        those of that subproduct are None.
        """
        this_product = utils.get_producttag(this_product)
        that_product = utils.get_producttag(that_product)

        # check each allowed_qids_config is allowed by that_subproduct
        allowed_qids_configs = this_subproduct_dict['allowed_qids_configs']
        if allowed_qids_configs == 'all':
            assert that_subproduct_dict['allowed_qids_configs'] == 'all', \
                f'product {this_product}, subproduct {this_subproduct} allows ' + \
                f'all qids_configs but product {that_product}, subproduct ' + \
                f'{that_subproduct} does not'
        elif that_subproduct_dict['allowed_qids_configs'] != 'all':
            for allowed_qids_config in allowed_qids_configs:
                assert allowed_qids_config in that_subproduct_dict['allowed_qids_configs'], \
                    f'product {this_product}, subproduct {this_subproduct} ' + \
                    f'allows {allowed_qids_config} but product {that_product}, ' + \
                    f'subproduct {that_subproduct} does not'

        # check each allowed_qid is allowed by that_subproduct
        allowed_qids = this_subproduct_dict['allowed_qids']
        if allowed_qids == 'all':
            assert that_subproduct_dict['allowed_qids'] == 'all', \
                f'product {this_product}, subproduct {this_subproduct} allows ' + \
                f'all qids but product {that_product}, subproduct ' + \
                f'{that_subproduct} does not'
        elif that_subproduct_dict['allowed_qids'] != 'all':
            for allowed_qid in allowed_qids:
                try:
                    assert allowed_qid in that_subproduct_dict['allowed_qids'], \
                        f'product {this_product}, subproduct {this_subproduct} ' + \
                        f'allows {allowed_qid} but product {that_product}, ' + \
                        f'subproduct {that_subproduct} does not'
                except TypeError as e:
                    raise AssertionError(
                        f'product {this_product}, subproduct {this_subproduct} ' + \
                        f'allows {allowed_qid} but product {that_product}, ' + \
                        f'subproduct {that_subproduct} allows no qids') from e
        
        # check that allowed_qids_extra_kwargs is a subset
        if not (this_subproduct_dict['allowed_qids_extra_kwargs'] is None and \
                that_subproduct_dict['allowed_qids_extra_kwargs'] is None):
            assert this_subproduct_dict['allowed_qids_extra_kwargs'].items() \
                <= that_subproduct_dict['allowed_qids_extra_kwargs'].items(), \
                f'product {this_product}, subproduct {this_subproduct} ' + \
                f'allowed_qids_extra_kwargs is not a subset of {that_product}, ' + \
                f'subproduct {that_subproduct} allowed_qids_extra_kwargs'

    def get_qid_kwargs_by_subproduct(self, product, subproduct, qid):
        """Return a dict of key-value pairs for this qid. The dict is a merger
        of any default pairs in this datamodel's qid_dict, as well as any
        additional pairs specified in a particular subproduct's configuration
        file, if any.

        Parameters
        ----------
        product : str
            The type of product, e.g. 'maps' or 'beams'.
        subproduct : str
            The specific subproduct.
        qid : str
            Dataset identification string.

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
        subproduct_config = self.get_subproduct_config(product, subproduct)
        subproduct_dict = self.get_subproduct_dict(product, subproduct)

        # check allowed_qids is not None
        assert subproduct_dict['allowed_qids'] is not None, \
            f'No allowed qids for product {product}, subproduct {subproduct} (config {subproduct_config})'

        # check qid is in the allowed_qids or 'all'
        if qid not in subproduct_dict['allowed_qids']:
            assert subproduct_dict['allowed_qids'] == 'all', \
                f'qid {qid} not allowed by product {product}, subproduct ' + \
                f'{subproduct} (config {subproduct_config})'

        qid_dict = deepcopy(self.qids[qid])
        if subproduct_dict['allowed_qids_extra_kwargs'] is not None:
            qid_subproduct_dict = subproduct_dict['allowed_qids_extra_kwargs'].get(qid, {})
            qid_dict.update(deepcopy(qid_subproduct_dict))

        return qid_dict
    
    def get_equal_qid_kwargs_by_subproduct(self, product, subproduct, *qids):
        """Return a dict of key-value pairs for the qids that are equal over 
        the qids. The dict is a merger of any default pairs in this datamodel'
        qid_dict, as well as any additional pairs specified in a particular
        subproduct's configuration file, if any.

        Parameters
        ----------
        product : str
            The type of product, e.g. 'maps' or 'beams'.
        subproduct : str
            The specific subproduct.
        qids : str
            Dataset identification strings.

        Returns
        -------
        dict
            A set of keywords for the requested qids, such as its array, frequency,
            etc.
        """
        all_qid_kwargs = [
            self.get_qid_kwargs_by_subproduct(product, subproduct, qid) for qid in qids
            ]
        return functools.reduce(
            lambda d1, d2: dict(d1.items() & d2.items()), all_qid_kwargs
            )

    def get_qid_names_by_subproduct(self, product, subproduct, *qids,
                                    qid_names_template=None):
        """Return a string of concatenated formatted qid names.

        Parameters
        ----------
        product : str
            The type of product, e.g. 'maps' or 'beams'.
        subproduct : str
            The specific subproduct.
        qids : str
            Dataset identification strings.
        qid_names_template : str, optional
            A template formatting string for a qid. Will be populated by a call
            to get_qid_kwargs_by_subproduct for each qid. If None, the qid is
            unaltered.

        Returns
        -------
        str
            Underscore-joined formatted qid names.
        """
        qid_names = []
        for qid in qids:
            qid_kwargs = self.get_qid_kwargs_by_subproduct(
                product, subproduct, qid
                )
            if qid_names_template is None:
                qid_names.append(qid)
            else:
                qid_names.append(qid_names_template.format(**qid_kwargs))
        return '_'.join(qid_names)

    def get_product_dict(self, product, copy=True):
        """Get the set of subproduct dictionaries under a product type, such as
        'maps' or 'beams'.

        Parameters
        ----------
        product : str
            Name of type of product, e.g. 'maps'. Can also be a module __name__
            in which case the product is inferred from the module basename.
        copy : bool, optional
            Return a deepcopy of the product_dict, by default True. Otherwise the
            product_dict which is bound as an attribute to this product object is
            returned.
            
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
                f'product {product} not in datamodel configuration file'
                ) from e
        
        return deepcopy(product_dict) if copy else product_dict                   
            
    def get_subproduct_dict(self, product, subproduct, copy=True):
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
        copy : bool, optional
            Return a deepcopy of the subproduct_dict, by default True. Otherwise the
            subproduct_dict which is bound as an attribute to this product object is
            returned.

        Returns
        -------
        dict
            A dictionary of information for this subproduct.

        Raises
        ------
        KeyError
            If a subproduct under the product type is not in this datamodel.
        """
        product_dict = self.get_product_dict(product, copy=False)
        try:
            subproduct_dict = product_dict[subproduct]
        except KeyError as e:
            product = utils.get_producttag(product)
            raise LookupError(
                f'product {product}, subproduct {subproduct} not in '
                'datamodel configuration file'
            ) from e
        
        return deepcopy(subproduct_dict) if copy else subproduct_dict                   

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
        AssertionError
            If a user's SOFIND_SYSTEM is not an sofind system.

        LookupError
            If a subproduct is not served on the user SOFIND_SYSTEM.
        """
        subproduct_dict = self.get_subproduct_dict(product, subproduct)
        subproduct_config = self.get_subproduct_config(product, subproduct)
        my_system = os.environ['SOFIND_SYSTEM']

        assert my_system in systems.sofind_systems, \
            f'user system {my_system} not in sofind_systems: {systems.sofind_systems}'

        try:
            product = utils.get_producttag(product)
            subproduct_path = subproduct_dict['system_paths'][my_system]
        except (TypeError, KeyError) as e:
            # we know KeyError thrown on my_system because 
            # check_subproduct_config_internal_consistency already checks for key
            # system_paths in subproduct_dict
            #
            # TypeError is if subproduct_dict['system_paths'] is None
            raise LookupError(
                f'product {product}, subproduct {subproduct} (config {subproduct_config}) not served on '
                f'user system {my_system}'
            ) from e
        return subproduct_path
    
    def get_subproduct_config(self, product, subproduct):
        """Get the config basename to a directory holding the files for this
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
            The config basename.

        Raises
        ------
        KeyError
            If a subproduct under the product type is not in this datamodel.
        """
        try:
            product = utils.get_producttag(product)
            subproduct_config = self.configs[product][subproduct]
        except KeyError as e:
            raise LookupError(
                f'product {product}, subproduct {subproduct} not in '
                'datamodel configuration file'
            ) from e
        return subproduct_config