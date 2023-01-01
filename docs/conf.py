# Configuration file for the Sphinx documentation builder.
#
# Getting started with sphinx
# https://docs.readthedocs.io/en/stable/intro/getting-started-with-sphinx.html

# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

###################################################################################################
# Sys path setting for autodoc (needs to be able to import the code)
import sys
from pathlib import Path
here = Path(__file__)
root = here.parent.parent
venv = root / 'venv' / 'lib' / 'python3.7' / 'site-packages'
spil_conf = root / 'hamlet_conf'
print(root)
sys.path.append(str(root))
sys.path.append(str(venv))
sys.path.append(str(spil_conf))
# sys.exit()

###################################################################################################
# General options
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

project = 'Spil'
copyright = '2022, Michael Haussmann'
author = 'Michael Haussmann'
release = '0.1.0'  # see also from spil import __version__

extensions = ['myst_parser',
    # 'sphinx.ext.duration',
    'sphinx.ext.napoleon',  # Google format doctrings -> reSt before parsed
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
	# 'sphinx.ext.todo',
	'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

###################################################################################################
# HTML options
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_title = "Spil Documentation"
# html_logo = "img/small.png"
html_favicon = "img/favicon.ico"

html_theme_options = {
	# 'logo_only': True,
	'display_version': True,
	'prev_next_buttons_location': 'bottom',
	'style_external_links': True,    # Toc options
	'collapse_navigation': False,
	# 'sticky_navigation': False,
	'navigation_depth': 3,
	'includehidden': True,
	'titles_only': False
}

###################################################################################################
# Autodoc
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#configuration

# Automatically extract typehints when specified and place them in
# descriptions of the relevant function/method.
autodoc_typehints = "description"

# Don't show class signature with the class' name.
autodoc_class_signature = "separated"

autodoc_default_options = {
 #    'members': 'var1, var2',
    'member-order': 'bysource',
#     'special-members': '__init__',
    'undoc-members': True,
#     'exclude-members': '__weakref__'
}


###################################################################################################
# Napoleon, for Google docstring format
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#docstrings
#
napoleon_google_docstring = True
# napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True
