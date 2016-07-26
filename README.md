# INGIfet
Cafet INGI management

## Standalone installation (Linux, OsX, and presumably other unices)

1. Install the version of webpy compatible with Python3.
  1. Clone the `webpy/webpy` repository
  2. Switch to the branch `py3`
  3. Install it using `setup.py` or ensure that `PYTHONPATH` contains the path to the folder.
  4. Install or upgrade pyqrcode to a working Python3 version
2. Configure the application
  1. Copy settings.py.example to settings.py
  2. Update the settings accordingly
3. Init the database
  1. python3 models.py
4. Export LANG
  1. `export LANG=en_GB.UTF-8` otherwise you might have issue while decoding strings.

At this point, the best option is probably to use a virtualenv to run the application, so that you can install the py3 branch of webpy and install dedicated packages like pyqrcode.

## Installation on a webserver

Currently the application has only been deployed on Apache as a (F-)CGI script using Flup6 as middleware to implement the WSGI gateway interface. A more effective installation should be possible with a python3 compatible version of mod_wsgi.

Deployments using NGnix or Lighttpd have not been tested yet.
