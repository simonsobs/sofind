from setuptools import setup, find_packages

setup(
    name='sofind',
    packages=find_packages(),
    package_data={'sofind': ['datamodels/*.yaml', 'products/*/*.yaml', 'qids/*.yaml']},
    version='0.0.11',
    install_requires=[
        'pixell>=0.12.0'
        ]
    )
