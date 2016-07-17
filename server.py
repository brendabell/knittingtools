import logging
import logging.config
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

logging.config.fileConfig('logging.conf')

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

			actions['get'](self)
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

			actions['post'](self)
		except Exception:
			exc_type, exc_value, exc_traceback = sys.exc_info()
			self.log_error("%s %s\n" % (
				exc_type,
				exc_value))
			logger.debug("path=%s %s",
				self.path,
				repr(traceback.format_exception(exc_type, exc_value,exc_traceback)))

	def log_request(self, code=None, size=None):
		logger.info("%s - - [%s] %s %s %s" % (
			self.address_string(),
			self.log_date_time_string(),
			self.requestline,
			code or '-',
			size or '-'))

	def log_error(self, *args):
		logger.error("%s" % args)

	def log_message(self, format, *args):
		logger.info("%s - - [%s] %s\n" % (
			self.address_string(),
			self.log_date_time_string(),
			format%args))

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
