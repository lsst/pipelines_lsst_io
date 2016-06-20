# LSST Science Pipelines Docs

**https://pipelines.lsst.io**

This repository contains the base source material for LSST's Stack Documentation.
Documentation is built using [Sphinx](http://sphinx-doc.org), which pulls in documentation material from LSST code repositories.

This repository is in early development.
While this repo (since Pipelines version 12.0) has authoritative release notes and installation information you make find the earlier documentation projects useful:

- [LSST Software User Guide wiki](https://confluence.lsstcorp.org/display/LSWUG.)
- [Doxyen-generated API reference](https://lsst-web.ncsa.illinois.edu/doxygen/x_masterDoxyDoc/)

Other documentation resources:

- [LSST Community forum](https://community.lsst.org)
- [DM Developer Guide](https://developer.lsst.io)

## Build the Docs

Create a [Python virtual environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/) for this project using your tool of choice: [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) or [pyvenv](https://docs.python.org/3.5/library/venv.html) (for Python 3).

Install the Python dependencies by running

```
pip install -r requirements.txt
```

Compile the HTML by running

```
make html
```

The site will be built in the `_build/` directory.

## Licensing

Copyright 2015-2016 AURA/LSST

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/">
![Creative Commons License](https://cdn.rawgit.com/lsst-sqre/lsst_stack_docs/master/_static/cc-by_large.svg?raw=true)
</a><br /><span xmlns:dct="http://purl.org/dc/terms/" property="dct:title">LSST Stack Handbook</span> by <a xmlns:cc="http://creativecommons.org/ns#" href="http://docs.lsst.codes" property="cc:attributionName" rel="cc:attributionURL">LSST Project</a> is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>
