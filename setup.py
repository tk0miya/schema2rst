# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os, sys

version = '0.1.0'
long_description = ''
#long_description = \
#        open(os.path.join("src","README.txt")).read() + \
#        open(os.path.join("src","TODO.txt")).read()

classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: Python Software Foundation License",
    "Programming Language :: Python",
    "Topic :: Software Development",
    "Topic :: Software Development :: Documentation",
]

setup(
     name='schema2rst',
     version=version,
     description='schema2rst generates reST file from database schema',
     long_description=long_description,
     classifiers=classifiers,
     keywords=['document','generator'],
     author='Takeshi Komiya',
     author_email='i.tkomiya at gmail.com',
     url='http://tk0miya.bitbucket.org/',
     license='PSL',
     packages=find_packages('src'),
     package_dir={'': 'src'},
     package_data = {'': ['buildout.cfg']},
     include_package_data=True,
     install_requires=[
        'setuptools',
        'sqlalchemy',
        'pyyaml',
         # -*- Extra requirements: -*-
     ],
     extras_require=dict(
         test=[
             'Nose',
             'minimock',
             'pep8',
         ],
     ),
     test_suite='nose.collector',
     tests_require=['Nose','minimock','pep8'],
     entry_points="""
        [console_scripts]
        schema2rst = schema2rst:main
        schema2graph = schema2rst.schema2graph:main
     """,
)
