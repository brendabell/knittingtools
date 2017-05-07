# knittingtools

KnittingTools is a simple web app written in Python. It currently supports two main features:
* A knitting calculator
* A punchcard generator

The app has been tested on Python version 2.7 with the following dependencies:
* cairocffi 0.7.2
* CairoSVG 1.0.22
* pycparser 2.17
* pyparsing 2.1.5
* svgwrite 1.1.8

To run the server:

* Clone this repo
* If you are installing to a Linux platform that supports chkconfig, copy `./bin/knittingtools-chkconfig` to the location appropriate for your flavor of Linux (usually /etc/rc.d/init.d).
* Edit the init script to reflect the appropriate locations for the lock file, python executable, server.py script and PID file. Note that the app has only been tested using the supplied virtual environment.
* Start, stop or restart the server using the following commands:

`sudo service knittingtools start`

`sudo service knittingtools stop`

`sudo service knittingtools restart`

* Use the following command to determine the server's current status:

`sudo service knittingtools status`

Access and error logs are written to `/var/log/knittingtools.log` and `/var/log/knittingtools.log` respectively. The log configuration can be modified by editing `logging.conf`.
