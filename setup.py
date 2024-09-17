# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='management_logging',
    version='1.2.4',
    author='Ryan Stalbow',
    author_email='ryan.stalbow@uktv.co.uk',
    packages=['management_logging'],
    url='https://github.com/uktv/management_logging',
    license='MIT',
    description='Provides logging for management commands',
    long_description=open('README.md').read(),
    zip_safe=False,
    include_package_data=True,
    package_data={'': ['README.rst']},
    install_requires=['aws-xray-sdk',]
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
