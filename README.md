# deep-surf

[![Travis](https://img.shields.io/travis/HowardRiddiough/deep-surf/master.svg?label=Travis%20CI)](
    https://travis-ci.org/HowardRiddiough/deep-surf)
[![codecov](https://codecov.io/gh/HowardRiddiough/deep-surf/branch/master/graph/badge.svg)](
    https://codecov.io/gh/HowardRiddiough/deep-surf)

The goal of this repo is to record the number of surfers currently in the water at 
[Scheveningen Noord](https://goo.gl/maps/dxb3422NShQ2). We aim to make those predictions using Object 
Detection. In the future we aim to be able to record wave height and wave quality using Deep Learning and 
to apply our methodology to beaches all over the world.

Contributions are welcome, please read our [guidelines](CONTRIBUTING.MD).

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

There are two key data elements: Images and Annotations.

### Images 

Image data is collected hosted on [scheveningenlive.nl](http://www.scheveningenlive.nl/). We currently 
collect data from two web cams:

1. [Surf Webcam](http://www.scheveningenlive.nl/surf-webcam/)
![sample webcam data](tests/data/frame/surfwebcam_20190129095446.jpg?raw=true)

2. [Sportsstrand Webcam](http://www.scheveningenlive.nl/sportstrand-webcam/)
![sample webcam data](tests/data/frame/sportstrandwebcam_20190212095550.jpg?raw=true)




### Annotations

Annotations record objects that can be found in an image and thier respective location in that image.


## Command Line Tools

We have command line tools! In this repo command line tools are well documented and can be found 
[here](cli-tools).
