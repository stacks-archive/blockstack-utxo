#!/usr/bin/python

from setuptools import setup, find_packages

# to set __version__
exec(open('blockstack_utxo/version.py').read())

setup(
    name='blockstack-utxo',
    version=__version__,
    url='https://github.com/blockstack/blockstack-utxo',
    license='MIT',
    author='Blockstack.org',
    author_email='support@blockstack.org',
    description='Python library for interacting with various blockchain service providers',
    keywords='blockchain bitcoin btc cryptocurrency name key value store data',
    packages=find_packages(),
    download_url='https://github.com/blockstack/blockstack-utxo/archive/master.zip',
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        "python-bitcoinrpc>=0.1",
        "requests>=2.4.3",
        "virtualchain>=0.0.13.0",
        "bitcoin>=1.1.42"
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
