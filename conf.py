"""Sphinx configurations for pipeline_lsst_io.

These configurations are centrally defined in Documenteer:
https://documenteer.lsst.io/pipelines/configuration.html
"""

from documenteer.conf.pipelines import *  # noqa: F403


project_name = "LSST Science Pipelines"
html_theme_options["logotext"] = project_name  # noqa: F405
html_title = project_name
html_short_title = project_name
