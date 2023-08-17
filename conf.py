"""Sphinx configurations for pipeline_lsst_io.

These configurations are centrally defined in Documenteer
(https://github.com/lsst-sqre/documenteer). Documentation:
https://documenteer.lsst.io/pipelines/configuration.html
"""

from documenteer.conf.pipelines import *

project = "LSST Science Pipelines"
html_theme_options["logotext"] = project
html_title = project
html_short_title = project

# Patch EUPS tag substitutions
rst_epilog = """

.. |eups-tag| replace:: v25_0_1
.. |eups-tag-mono| replace:: ``v25_0_1``
.. |eups-tag-bold| replace:: **v25_0_1**
"""

# Patch EUPS and Git tag context for Jinja templating
jinja_contexts = {
    "default": {
        "release_eups_tag": "v25_0_1",
        "release_git_ref": "25.0.1",
        "version": "v25_0_1",
        "release": "v25_0_1",
        "scipipe_conda_ref": "25.0.1",
        "pipelines_demo_ref": "25.0.1",
        "newinstall_ref": "25.0.1",
    }
}

# needed for pipe_base
intersphinx_mapping['networkx'] = ('https://networkx.org/documentation/stable/', None)
