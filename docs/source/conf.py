# Configuration file for the Sphinx documentation builder.

import os
import sys
from importlib import metadata
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information

project = 'Image Marker'
copyright = '2025'
author = 'Andi Kisare, Ryan Walker, Lindsey Bleem'

release = metadata.version("imgmarker")
version = metadata.version("imgmarker")

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'numpydoc',
    'sphinx_design'
]

autosummary_generate = True  # Turn on sphinx.ext.autosummary
autodoc_mock_imports = ['PyQt6', 'PyQt6.QtGui', 'PyQt6.QtCore', 'PyQt6.QtWidgets']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'furo'

# -- Options for EPUB output
epub_show_urls = 'footnote'