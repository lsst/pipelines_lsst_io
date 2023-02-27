"""Sphinx configurations for pipeline_lsst_io.

These configurations are centrally defined in Documenteer
(https://github.com/lsst-sqre/documenteer).
"""

from documenteer.conf.pipelinespkg import *

project='LSST Science Pipelines'
html_theme_options["logotext"] = project
html_title = project
html_short_title = project


# Patch EUPS tag subsitutions
rst_epilog = """

.. |eups-tag| replace:: v24_0_0
.. |eups-tag-mono| replace:: ``v24_0_0``
.. |eups-tag-bold| replace:: **v24_0_0**
"""

# Patch EUPS and Git tag context for Jinja templating
jinja_contexts = {
    "default": {
        "release_eups_tag": "v24_0_0",
        "release_git_ref": "24.0.0",
        "version": "v24_0_0",
        "release": "v24_0_0",
        "scipipe_conda_ref": "24.0.0",
        "pipelines_demo_ref": "24.0.0",
        "newinstall_ref": "24.0.0",
    }
}

# Patch preset configuration of the matplotlib plot directive from
# documenteer. In documenteer 0.5 we automatically configure the docs
# with this extension, but in documenteer 0.6 we stopped adding this
# extension by default because of compatibility issues with the latest
# Sphinx. Once we move the Pipelines docs build in ci.lsst.codes to
# Documenteer 0.6+ we can drop this patch.
try:
    import matplotlib.sphinxext.plot_directive
    mpl_ext_name = matplotlib.sphinxext.plot_directive.__name__
    if mpl_ext_name in extensions:  # noqa F821
        extensions.remove(mpl_ext_name)  # noqa F821
except ImportError:
    pass
