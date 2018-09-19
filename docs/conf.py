# -*- coding: utf-8 -*-

import os
import sys

#sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../lib'))
#sys.path.insert(0, os.path.abspath('../lib/elevages_numeriques'))


# -- General configuration ------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

# Uncomment the below if you use native CircuitPython modules such as
# digitalio, micropython and busio. List the modules you use. Without it, the
# autodoc module docs will fail to generate with a warning.
autodoc_mock_imports = ["adafruit_bus_device", "micropython"]
intersphinx_mapping = {'python': ('https://docs.python.org/3.4', None),'BusDevice': ('https://circuitpython.readthedocs.io/projects/busdevice/en/latest/', None),'CircuitPython': ('https://circuitpython.readthedocs.io/en/latest/', None)}
#intersphinx_mapping = {'python': ('https://docs.python.org/3.4', None),'CircuitPython': ('https://circuitpython.readthedocs.io/en/latest/', None)}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# If true, '()' will be appended to :func: etc. cross-reference text.
#
add_function_parentheses = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'
