# -*- coding: utf-8 -*-
import sys
from setuptools import setup, find_packages

version = '0.9.0'
long_description = ''

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Python Software Foundation License",
    "Programming Language :: Python",
    "Topic :: Software Development",
    "Topic :: Software Development :: Documentation",
]

tests_requires = [
    'nose',
    'mock',
    'pep8>=1.3',
    'testing.mysqld>=1.2.3',
    'testing.postgresql>=1.0.1',
]

if sys.version_info < (2, 7):
    tests_requires.append('unittest2')

setup(
    name='schema2rst',
    version=version,
    description='schema2rst generates reST doc from database schema',
    long_description=long_description,
    classifiers=classifiers,
    keywords=['document', 'generator'],
    author='Takeshi Komiya',
    author_email='i.tkomiya at gmail.com',
    url='https://bitbucket.org/tk0miya/schema2rst',
    license='PSL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={'': ['buildout.cfg']},
    include_package_data=True,
    install_requires=[
        'setuptools',
        'sqlalchemy',
        'pyyaml',
        'six',
    ],
    extras_require=dict(
        test=tests_requires,
    ),
    test_suite='nose.collector',
    tests_require=tests_requires,
    entry_points="""
       [console_scripts]
       schemadump = schema2rst.commands.dump:main
       schema2rst = schema2rst.commands.rst:main
       schema2graph = schema2rst.commands.graph:main
    """,
)
