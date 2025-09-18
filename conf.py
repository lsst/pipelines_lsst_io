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

# needed for pipe_base
intersphinx_mapping['networkx'] = ('https://networkx.org/documentation/stable/', None)
