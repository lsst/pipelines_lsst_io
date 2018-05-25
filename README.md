# LSST Science Pipelines Docs

**https://pipelines.lsst.io**

This repository contains the base source material for the LSST Science Pipelines Documentation.
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

Install the Python dependencies by running:

This Sphinx project must be built within a set up LSST environment.

```bash
git clone https://github.com/lsst/pipelines_lsst_io
cd pipelines_lsst_io
```

Set up packages included with these docs:

```
setup -r .
```

Create a virtual environment and install PyPI dependencies:

```bash
python -m venv --system-site-packages --without-pip .pyvenv
source .pyvenv/bin/activate
curl https://bootstrap.pypa.io/get-pip.py | python
.pyvenv/bin/pip install -r requirements.txt
```

Compile the site:

```bash
stack-docs build
```

The site will be built in the `_build/` directory.

## Licensing

Copyright 2015-2018 Association of Universities for Research in Astronomy.

Licensed under [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).
