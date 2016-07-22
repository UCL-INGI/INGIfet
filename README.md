# INGIfet
Cafet INGI management

## Installation (Linux, OsX, and presumably other unices)

1. Install the version of webpy compatible with Python3.
  1. Clone the `webpy/webpy` repository
  2. Switch to the branch `py3`
  3. Install it using `setup.py` or ensure that `PYTHONPATH` contains the path to the folder.
2. Configure the application
  1. Copy settings.py.example to settings.py
  2. Update the settings accordingly
3. Init the database
  1. python3 models.py
4. Export LANG
  1. `export LANG=en_GB.UTF-8` otherwise you might have issue while decoding strings.
