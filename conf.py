"""Sphinx configurations for pipeline_lsst_io.

These configurations are centrally defined in Documenteer:
https://documenteer.lsst.io/pipelines/configuration.html
"""

from documenteer.conf.pipelines import *  # noqa: F403


project_name = "LSST Science Pipelines"
html_theme_options["logotext"] = project_name  # noqa: F405
html_title = project_name
html_short_title = project_name


def setup(app):
    # Undo the automodapi autodoc enhancements that are incompatible with
    # pybind11 properties. Essentially this restores the built-in getattr
    # as the attr getter for "type" rather than
    # https://github.com/astropy/sphinx-automodapi/blob/b68a5f3c6805d7c5d0eaa55fff1ff84cc671baf0/sphinx_automodapi/autodoc_enhancements.py#L15
    app.add_autodoc_attrgetter(type, getattr)
