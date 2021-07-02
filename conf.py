"""Sphinx configurations for pipeline_lsst_io.

These configurations are centrally defined in Documenteer
(https://github.com/lsst-sqre/documenteer).
"""

from documenteer.sphinxconfig.stackconf import \
    build_pipelines_lsst_io_configs


globals().update(build_pipelines_lsst_io_configs(
    project_name='LSST Science Pipelines',
))

# Patch EUPS tag subsitutions
rst_epilog = """

.. |eups-tag| replace:: v22_0_0
.. |eups-tag-mono| replace:: ``v22_0_0``
.. |eups-tag-bold| replace:: **v22_0_0**
"""

# Patch EUPS and Git tag context for Jinja templating
jinja_contexts = {
    "default": {
        "release_eups_tag": "v22_0_0",
        "release_git_ref": "22.0.0",
        "version": "v22_0_0",
        "release": "v22_0_0",
        "scipipe_conda_ref": "22.0.0",
        "pipelines_demo_ref": "22.0.0",
        "newinstall_ref": "22.0.0",
    }
}
