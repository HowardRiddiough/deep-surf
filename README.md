# deep-surf
The goal of this repo is to make live predictions on how many people are surfing Scheveningen Noord using 
Object Detection.

Currently this repo includes:

- Tools to make data collection easy

## Installation
Use Python 3.6! Because TensorFlow 1.10 does not support Python 3.7.

### Install package inside virtualenv
Create a virtualenv, for example:

    python -m venv ~/pyvenvs/deepsurf

Activate it:

    source ~/pyvenvs/deepsurf/bin/activate

Now install the package + dependencies + test dependencies (e.g. flake8 and pytest) in editable mode:

    pip install -e ".[test]"

You need to re-activate the virtualenv to be able to make use of the newly installed executables

You can now `import deepsurf` from Python, as long as the virtualenv is active. Even in Jupyter Notebook. 
Any changes you make in this directory directly take effect, because it's installed in editable mode (`-e` 
flag).

## Data


