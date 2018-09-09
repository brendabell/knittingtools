'''
All rights reserved (c) 2016-2018 Brenda A. Bell.

This file is part of the PCGenerator (see
https://github.com/brendabell/knittingtools).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

import logging
import logging.config
import os
import sys
import traceback

from BaseHTTPServer import BaseHTTPRequestHandler
from BaseHTTPServer import HTTPServer

from handlers import actions

pcgenerator_actions = {
	'get': actions.pcgenerator_get,
	'post': actions.pcgenerator_post }

calculator_actions = {
	'get': actions.calculator_get,
	'post': None
}

index_actions = {
	'get': actions.index_get,
	'post': None
}

template_map = {
	'/pcgenerator': pcgenerator_actions,
	'/pcgenerator/': pcgenerator_actions,
	'/calculator': calculator_actions,
	'/calculator/': calculator_actions,
	'/knittingtools': index_actions,
	'/knittingtools/': index_actions,
	'/index': index_actions,
	'/index/': index_actions,
	'/': index_actions}

logging.config.fileConfig("{0}/{1}".format(os.path.dirname(os.path.realpath(__file__)), 'logging.conf'))

logger = logging.getLogger('root')

class MyHandler(BaseHTTPRequestHandler):

	def handle_not_found(self):
		self.send_response(404)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		self.wfile.write(
			"<h1>Aw, snap! We seem to have a problem.</h1><p><b>")
		self.wfile.write('The request resource was not found on this server.')

	def do_GET(self):
		try:
			actions = template_map.get(self.path, None)
			if actions is None:
				self.handle_not_found()
				return

			actions['get'](self, logger)
		except Exception:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			self.log_error("%s %s\n" % (
				exc_type,
				exc_value))
			logger.debug("path=%s %s",
				self.path,
				repr(traceback.format_exception(exc_type, exc_value,exc_traceback)))

	def do_POST(self):
		try:
			actions = template_map.get(self.path, None)
			if actions is None:
				self.handle_not_found()
				return

			actions['post'](self, logger)
		except Exception:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			self.log_error("%s %s\n" % (
				exc_type,
				exc_value))
			logger.debug("path=%s %s",
				self.path,
				repr(traceback.format_exception(exc_type, exc_value, exc_traceback)))

	def log_request(self, code=None, size=None):
		logger.info("%s - - [%s] %s %s %s" % (
			self.headers.get('X-Forwarded-For', None) or self.address_string(),
			self.log_date_time_string(),
			self.requestline,
			code or '-',
			size or '-'))

	def log_error(self, *args):
		logger.error(args)

	def log_message(self, *args):
		logger.info("%s - - [%s] %s" % (
			self.headers.get('X-Forwarded-For', None) or self.address_string(),
			self.log_date_time_string(),
			args))

def main():
	try:
		logger.info("Starting server...")
		server = HTTPServer(('', 8080), MyHandler)
		server.serve_forever()
	except KeyboardInterrupt:
		logger.info("Stopping server...")
	except Exception:
		logger.error(sys.exc_info()[0])
	finally:
		server.socket.close()

if __name__ == '__main__':
	main()
