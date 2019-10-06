from __future__ import absolute_import
from __future__ import print_function

import io
import os
import re
from glob import glob
from setuptools import find_packages
from setuptools import setup
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="unleashed-py",
    version="0.0.13",
    url="https://github.com/jonathanStrange0/unleashed-py",
    license='MIT',

    author="Jonathan Mucha",
    author_email="jonmucha@gmail.com",

    long_description_content_type="text/x-rst",
    description="Python package to connect to the Unleashed Software inventory management API",
    long_description=read("README.rst"),
    packages=find_packages('unleashed-py'),
    package_dir={'': 'unleashed-py'},
    py_modules=[splitext(basename(path))[0] for path in glob('unleashed-py/*.py')],
    include_package_data=True,
    # packages=find_packages(exclude=('tests',)),

    install_requires=['requests'],

    python_requires='>=3.6',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
