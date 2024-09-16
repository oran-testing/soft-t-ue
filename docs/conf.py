# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Soft-Tester UE'
copyright = '2024, RAN TESTER UE'
author = 'Joshua J. Moore'
release = '1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os
import sys
import sphinx_rtd_theme

sys.path.insert(0, os.path.abspath('.'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_theme_options = {
    "display_version": False,
    "show_sourcelink": False,
    "collapse_navigation" : False,
    "sticky_navigation": False,
    'flyout': False,  
}

html_context = {
    "sidebar_external_links_caption": "Useful Links",
    "sidebar_external_links": [
        (
            '<i class="fa fa-globe"></i> Website',
            "https://www.rantesterue.org/",
        ),
        (
            '<i class="fa fa-github fa-fw"></i> Source code',
            "https://github.com/oran-testing/soft-t-ue",
        ),
        (
            '<i class="fa fa-bug fa-fw"></i> Report an issue',
            "https://github.com/oran-testing/soft-t-ue/issues",
        ),
    ],
}

html_show_sphinx = False
html_show_sourcelink = False
html_favicon = 'images/favicon.png'
html_logo = 'images/logo.png'
html_static_path = ['_static']
html_css_files = [
    'custom.css',
]
templates_path = ['_templates']

