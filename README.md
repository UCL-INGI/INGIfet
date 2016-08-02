# INGIfet
Cafet INGI management

This software is meant to provide simple means to handle candy and beverage intakes in the INGI cafet.
First and foremost, this is a system based on honor. The previous system was simply a paper sheet where
you draw a stick in front of your name when taking something in the fridge. This software is meant to
replace this by provinding the same basic features and easing the accounting workload. The security
is thus **not** that important right now. For example, it is easy to reproduce a user RFID tag, but we
don't care (for now), as it is even easier to draw a stick in front of someone else name (or to not draw
a stick at all).

## Standalone installation (Linux, OsX, and presumably other unices)

1. Install the version of webpy compatible with Python3 :
  
   `pip install web.py==0.40.dev0`

2. Configure the application
  1. Copy `settings.py.example` to `settings.py`
  2. Update the settings accordingly
3. Init the database

  `python3 models.py`
  
4. Export LANG
  `export LANG=en_GB.UTF-8` otherwise you might have issue while decoding strings.

At this point, the best option is probably to use a virtualenv to run the application, so that you can install the py3 branch of webpy and install dedicated packages like pyqrcode.

## Installation on a webserver

Currently the application has only been deployed on Apache as a (F-)CGI script using Flup6 as middleware to implement the WSGI gateway interface. A more effective installation should be possible with a python3 compatible version of mod_wsgi.

Deployments using NGnix or Lighttpd have not been tested yet.
