import cgi
from os import curdir
import sys
import traceback

from modules.pcgenerator import PCGenerator

def pcgenerator_get(handler):

	f = open("{}/templates/{}".format(
		curdir,
		"pcgenerator.html"))

	try:
		handler.send_response(200)
		handler.send_header('Content-type', 'text/html')
		handler.end_headers()
		handler.wfile.write(f.read())

		return
			
	except Exception:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		handler.wfile.write(
			"<h1>Aw, snap! We seem to have a problem.</h1><p><b>")
		handler.wfile.write(
			repr(traceback.format_exception(exc_type, exc_value,exc_traceback)))
		handler.wfile.write(
			"</b><p>Please report this error via private message to "
			"<a href='http://www.ravelry.com/people/beebell'>beebell on Ravelry</a>. "
			"It will be helpful if you include the pattern you uploaded to help me "
			"diagnose the issue.")
		handler.log_error("%s", traceback.format_exception(exc_type, exc_value,exc_traceback))

	finally:
		f.close()

def pcgenerator_post(handler):

	try:
		ctype, pdict = cgi.parse_header(handler.headers.getheader('content-type'))
		if ctype == 'multipart/form-data':
			query=cgi.parse_multipart(handler.rfile, pdict)

		upfilecontent = query.get('upfile')
		if len(upfilecontent[0]) > 2500:
			handler.send_response(302)
			handler.send_header('Content-type', 'text/html')
			handler.end_headers()
			handler.wfile.write("Sorry. Your file cannot exceed 2500 bytes!")
		else:
			horz_repeat = query.get('horz')
			vert_repeat = query.get('vert')
			cell_height = query.get('rowheight')
			cell_width = query.get('colwidth')
			generator = PCGenerator(
				upfilecontent[0],
				float(cell_height[0]),
				float(cell_width[0]),
				int(horz_repeat[0]),
				int(vert_repeat[0]))
			result = generator.generate()

			handler.send_response(200)
			handler.send_header('Content-type', 'image/svg+xml')
			handler.send_header("Content-Disposition", "attachment; filename=punchcard.svg")
			handler.end_headers()
			handler.wfile.write(result)

			return

	except ValueError as e:
		handler.send_response(302)
		handler.send_header('Content-type', 'text/html')
		handler.end_headers()
		handler.wfile.write(
			"<h1>Aw, snap!</h1><p>")
		handler.wfile.write(e)

	except Exception:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		handler.send_response(302)
		handler.send_header('Content-type', 'text/html')
		handler.end_headers()
		handler.wfile.write(
			"<h1>Aw, snap! We seem to have a problem.</h1><p><b>")
		handler.wfile.write(
			repr(traceback.format_exception(exc_type, exc_value,exc_traceback)))
		handler.wfile.write(
			"</b><p>Please report this error via private message to "
			"<a href='http://www.ravelry.com/people/beebell'>beebell on Ravelry</a>. "
			"It will be helpful if you include the pattern you uploaded to help me "
			"diagnose the issue.")
		handler.log_error("%s", traceback.format_exception(exc_type, exc_value,exc_traceback))

def calculator_get(handler):

	f = open("{}/templates/{}".format(
		curdir,
		"calculator.html"))

	try:
		handler.send_response(200)
		handler.send_header('Content-type', 'text/html')
		handler.end_headers()
		handler.wfile.write(f.read())

		return
			
	except Exception:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		handler.wfile.write(
			"<h1>Aw, snap! We seem to have a problem.</h1><p><b>")
		handler.wfile.write(
			repr(traceback.format_exception(exc_type, exc_value,exc_traceback)))
		handler.wfile.write(
			"</b><p>Please report this error via private message to "
			"<a href='http://www.ravelry.com/people/beebell'>beebell on Ravelry</a>. "
			"It will be helpful if you include the pattern you uploaded to help me "
			"diagnose the issue.")
		handler.log_error("%s", traceback.format_exception(exc_type, exc_value,exc_traceback))

	finally:
		f.close()

def index_get(handler):
	f = open("{}/templates/{}".format(
	curdir,
	"index.html"))

	try:
		handler.send_response(200)
		handler.send_header('Content-type', 'text/html')
		handler.end_headers()
		handler.wfile.write(f.read())

		return
			
	except Exception:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		handler.wfile.write(
			"<h1>Aw, snap! We seem to have a problem.</h1><p><b>")
		handler.wfile.write(
			repr(traceback.format_exception(exc_type, exc_value,exc_traceback)))
		handler.wfile.write(
			"</b><p>Please report this error via private message to "
			"<a href='http://www.ravelry.com/people/beebell'>beebell on Ravelry</a>. "
			"It will be helpful if you include the pattern you uploaded to help me "
			"diagnose the issue.")
		handler.log_error("%s", traceback.format_exception(exc_type, exc_value,exc_traceback))

	finally:
		f.close()
