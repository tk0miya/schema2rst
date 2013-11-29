# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

version = '0.1.0'
long_description = ''

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
        test=[
            'Nose',
            'pep8>=1.3',
            'testing.mysqld',
            'testing.postgresql',
        ],
    ),
    test_suite='nose.collector',
    tests_require=[
        'Nose',
        'pep8>=1.3',
        'testing.mysqld',
        'testing.postgresql',
    ],
    entry_points="""
       [console_scripts]
       schemadump = schema2rst.commands.dump:main
       schema2rst = schema2rst.commands.rst:main
       schema2graph = schema2rst.commands.graph:main
    """,
)
