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

.. |eups-tag| replace:: v24_1_1
.. |eups-tag-mono| replace:: ``v24_1_1``
.. |eups-tag-bold| replace:: **v24_1_1**
"""

# Patch EUPS and Git tag context for Jinja templating
jinja_contexts = {
    "default": {
        "release_eups_tag": "v24_1_1",
        "release_git_ref": "24.1.1",
        "version": "v24_1_1",
        "release": "v24_1_1",
        "scipipe_conda_ref": "24.1.1",
        "pipelines_demo_ref": "24.1.1",
        "newinstall_ref": "24.1.1",
    }
}
