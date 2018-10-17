"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gps-pedagogique',

    use_scm_version=True,
    setup_requires=['setuptools_scm'],

    description='CircuitPython library for a beginner-friendly GPS tracker.',
    long_description=long_description,
    long_description_content_type='text/x-rst',

    # The project's main homepage.
    url='https://github.com/Wizehunt/GPS-pedagogique',

    # Author details
    author='Théo Kriszt',
    author_email='theo@kriszt.fr',

    install_requires=[],

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers, Users',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Hardware',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='gps module latitude longitude INRA beginner logger tracker micropython circuitpython',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    py_modules=['lib/gps-pedagogique'],
)
