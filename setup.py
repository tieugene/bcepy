# upload: python setup.py sdist upload -r pypi

import os
from setuptools import setup, find_packages

import bcepy

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

setup(
    name='bcepy',
    version=bcepy.__version__,
    description='BitCoin Export to SQL-loadable',
    keywords='btc bitcoin',
    platforms=["any"],
    license='GNU PUBLIC LICENSE',
    author='TI_Eugene',
    author_email='ti.eugene@gmail.com',
    maintainer='TI_Eugene',
    maintainer_email='ti.eugene@gmail.com',
    url='https://github.com/tieugene/bcepy/',
    include_package_data=True,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'bcepy = bcepy:main',
        ],
    },
    long_description=README,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
