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

.. |eups-tag| replace:: v23_0_2
.. |eups-tag-mono| replace:: ``v23_0_2``
.. |eups-tag-bold| replace:: **v23_0_2**
"""

# Patch EUPS and Git tag context for Jinja templating
jinja_contexts = {
    "default": {
        "release_eups_tag": "v23_0_2",
        "release_git_ref": "23.0.2",
        "version": "v23_0_2",
        "release": "v23_0_2",
        "scipipe_conda_ref": "23.0.2",
        "pipelines_demo_ref": "23.0.2",
        "newinstall_ref": "23.0.2",
    }
}
