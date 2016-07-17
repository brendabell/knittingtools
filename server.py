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
	'/index': index_actions }


class MyHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		print self.path
		actions = template_map.get(self.path, None)
		if actions is None:
			self.send_response(404)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('Not found!')

		actions['get'](self)

	def do_POST(self):
		print self.path
		actions = template_map.get(self.path, None)
		if actions is None:
			self.send_response(404)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			self.wfile.write('Not found!')

		actions['post'](self)


def main():
	try:
		server = HTTPServer(('', 8088), MyHandler)
		print 'started httpserver...'
		server.serve_forever()
	except KeyboardInterrupt:
		print '^C received, shutting down server'
	except Exception:
		print sys.exc_info()[0]
	finally:
		server.socket.close()

if __name__ == '__main__':
	main()
