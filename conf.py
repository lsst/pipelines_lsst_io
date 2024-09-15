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

.. |eups-tag| replace:: v27_0_0
.. |eups-tag-mono| replace:: ``v27_0_0``
.. |eups-tag-bold| replace:: **v27_0_0**
"""

# Patch EUPS and Git tag context for Jinja templating
jinja_contexts = {
    "default": {
        "release_eups_tag": "v27_0_0",
        "release_git_ref": "27.0.0",
        "version": "v27_0_0",
        "release": "v27_0_0",
        "scipipe_conda_ref": "27.0.0",
        "pipelines_demo_ref": "27.0.0",
    }
}

jira_uri_template = "https://ls.st/{ticket}"

# needed for pipe_base
intersphinx_mapping['networkx'] = ('https://networkx.org/documentation/stable/', None)
