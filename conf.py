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

.. |eups-tag| replace:: v23_0_1
.. |eups-tag-mono| replace:: ``v23_0_1``
.. |eups-tag-bold| replace:: **v23_0_1**
"""

# Patch EUPS and Git tag context for Jinja templating
jinja_contexts = {
    "default": {
        "release_eups_tag": "v23_0_1",
        "release_git_ref": "23.0.1",
        "version": "v23_0_1",
        "release": "v23_0_1",
        "scipipe_conda_ref": "23.0.1",
        "pipelines_demo_ref": "23.0.1",
        "newinstall_ref": "23.0.1",
    }
}

import matplotlib.sphinxext.plot_directive
extensions.remove(matplotlib.sphinxext.plot_directive.__name__)
