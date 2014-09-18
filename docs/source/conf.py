# -*- coding: utf-8 -*-

import sys
import os

sys.path.insert(0, os.path.abspath('../../'))

import pypushwoosh

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
]
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = u'pypushwoosh'
copyright = u'2014, Arello Mobile'
version = pypushwoosh.__version__
release = version

exclude_patterns = []
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = ['_static']
htmlhelp_basename = 'pypushwooshdoc'
latex_documents = [
    ('index', 'pypushwoosh.tex', u'pypushwoosh Documentation',
     u'Arello Mobile', 'manual'),
]
