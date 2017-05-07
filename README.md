# knittingtools

KnittingTools is a simple web app written in Python. It currently supports two main features:
* A knitting calculator
* A punchcard generator

## Dependencies
* CairoSVG 1.0.22
* svgwrite 1.1.8

## Installation
* Clone this repo to a local directory.
* If you are installing to a Linux platform that supports chkconfig, copy `./bin/knittingtools-chkconfig` to the location appropriate for your Linux distribution (usually /etc/rc.d/init.d).
* Edit the init script to reflect the appropriate locations for the lock file, python executable, server.py script and PID file. Note that the app has only been tested using the supplied virtual environment.

## Running The Application
Start, stop or restart the server using the following commands:

`sudo service knittingtools start`

`sudo service knittingtools stop`

`sudo service knittingtools restart`

Use the following command to determine the server's current status:

`sudo service knittingtools status`

## Logging
Access and error logs are written to `/var/log/knittingtools.log` and `/var/log/knittingtools.log` respectively. The log configuration can be modified by editing `logging.conf`.
