"""Sphinx configurations for pipeline_lsst_io.

These configurations are centrally defined in Documenteer
(https://github.com/lsst-sqre/documenteer). Documentation:
https://documenteer.lsst.io/pipelines/configuration.html
"""

from documenteer.conf.guide import *  # noqa: F403, import *
import documenteer
import lsst.sphinxutils
import os

_storage_path = os.path.dirname(documenteer.__file__)
html_theme_options['logo'] = {
    'image_light': os.path.join(_storage_path, 'assets', 'rubin-titlebar-imagotype-light.svg'),
    'image_dark': os.path.join(_storage_path, 'assets', 'rubin-titlebar-imagotype-dark.svg'),
}

html_static_path.append('_static')
html_css_files.append('navbar.css')

# Patch EUPS tag substitutions
rst_epilog = """

.. |eups-tag| replace:: v29_2_1
.. |eups-tag-mono| replace:: ``v29_2_1``
.. |eups-tag-bold| replace:: **v29_2_1**
"""

# Patch EUPS and Git tag context for Jinja templating
jinja_contexts = {
    "default": {
        "release_eups_tag": "v29_2_1",
        "release_git_ref": "29.2.1",
        "version": "v29_2_1",
        "release": "v29_2_1",
        "scipipe_conda_ref": "29.2.1",
        "pipelines_demo_ref": "29.2.1",
    }
}

jira_uri_template = "https://ls.st/{ticket}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx_automodapi.automodapi",
    "sphinx_automodapi.smart_resolver",
    "documenteer.ext.jira",
    "lsst.sphinxutils.ext.packagetoctree"
]
autosummary_generate = True
suppress_warnings = ['docutils']

# needed for pipe_base
intersphinx_mapping['networkx'] = ('https://networkx.org/documentation/stable/', None)
