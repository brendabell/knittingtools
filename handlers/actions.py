import cairosvg
import cgi
import os
import sys
import time
import traceback

from modules.pcgenerator import PCGenerator
from modules.pcgenerator import calibrate

def pcgenerator_get(handler, logger):

	f = open("{}/../templates/{}".format(
		os.path.dirname(os.path.realpath(__file__)),
		"pcgenerator.html"))

	try:
		handler.send_response(200)
		handler.send_header('Content-type', 'text/html')
		handler.end_headers()
		handler.wfile.write(f.read())

		return
			
	except Exception:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		handler.log_error("%s", traceback.format_exception(exc_type, exc_value,exc_traceback))

		handler.wfile.write(
			"<h1>Aw, snap! We seem to have a problem.</h1><p><b>")
		handler.wfile.write(
			repr(traceback.format_exception(exc_type, exc_value,exc_traceback)))
		handler.wfile.write(
			"</b><p>Please report this error via private message to "
			"<a href='http://www.ravelry.com/people/beebell'>beebell on Ravelry</a>. "
			"It will be helpful if you include the pattern you uploaded to help me "
			"diagnose the issue.")

	finally:
		f.close()

def pcgenerator_post(handler, logger):

	try:
		logger.debug('parsing header')
		ctype, pdict = cgi.parse_header(handler.headers.getheader('Content-Type'))
		logger.debug('checking form data')
		if ctype == 'multipart/form-data':
			logger.debug('parsing form data')
			query=cgi.parse_multipart(handler.rfile, pdict)

		logger.debug('calibrate?')
		calibrate_only = query.get('test', [''])[0] == 'test'
		logger.debug(calibrate_only)

		result = None
		filename_template = None
		convert_to_png = False

		if calibrate_only:
			logger.debug('calibrating')
			result = calibrate()
			logger.debug('calibration done')
			logger.debug(result)
			filename_template = 'attachment; filename="calibrate-{}.{}"'
		else:
			upfilecontent = query.get('upfile')
			if len(upfilecontent[0]) > 4000:
				handler.send_response(302)
				handler.send_header('Content-type', 'text/html')
				handler.end_headers()
				handler.wfile.write("Sorry. Your file cannot exceed 2500 bytes!")
			else:
				machine_type = query.get('machine')
				vert_repeat = query.get('vert')
				convert_to_png = query.get('png', [''])[0] == 'png'

				generator = PCGenerator(
					handler,
					upfilecontent[0],
					machine_type[0],
					int(vert_repeat[0]))
				result = generator.generate()
				filename_template = 'attachment; filename="punchcard-{}.{}"'

		handler.send_response(200)

		if convert_to_png:
			result = cairosvg.svg2png(bytestring=result)
			handler.send_header('Content-type', 'image/png')
			handler.send_header('Content-Disposition', filename_template.format(int(time.time()), "png"))
		else:
			handler.send_header('Content-type', 'image/svg+xml')
			handler.send_header('Content-Disposition', filename_template.format(int(time.time()), "svg"))

		handler.end_headers()
		handler.wfile.write(result)

		return

	except ValueError as e:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		handler.log_error("%s", traceback.format_exception(exc_type, exc_value,exc_traceback))

		handler.send_response(302)
		handler.send_header('Content-type', 'text/html')
		handler.end_headers()
		handler.wfile.write(
			"<h1>Aw, snap! We seem to have a problem.</h1><p><b>")
		handler.wfile.write(
			repr(traceback.format_exception(exc_type, exc_value,exc_traceback)))
		handler.wfile.write(e)
		handler.wfile.write(
			"</b><p>Please report this error via private message to "
			"<a href='http://www.ravelry.com/people/beebell'>beebell on Ravelry</a>. "
			"It will be helpful if you include the pattern you uploaded to help me "
			"diagnose the issue.")

	except Exception:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		handler.log_error("%s", traceback.format_exception(exc_type, exc_value,exc_traceback))

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

def calculator_get(handler):

	f = open("{}/../templates/{}".format(
		os.path.dirname(os.path.realpath(__file__)),
		"calculator.html"))

	try:
		handler.send_response(200)
		handler.send_header('Content-type', 'text/html')
		handler.end_headers()
		handler.wfile.write(f.read())

		return
			
	except Exception:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		handler.log_error("%s", traceback.format_exception(exc_type, exc_value,exc_traceback))

		handler.wfile.write(
			"<h1>Aw, snap! We seem to have a problem.</h1><p><b>")
		handler.wfile.write(
			repr(traceback.format_exception(exc_type, exc_value,exc_traceback)))
		handler.wfile.write(
			"</b><p>Please report this error via private message to "
			"<a href='http://www.ravelry.com/people/beebell'>beebell on Ravelry</a>. "
			"It will be helpful if you include the pattern you uploaded to help me "
			"diagnose the issue.")

	finally:
		f.close()

def index_get(handler):
	f = open("{}/../templates/{}".format(
		os.path.dirname(os.path.realpath(__file__)),
		"index.html"))

	try:
		handler.send_response(200)
		handler.send_header('Content-type', 'text/html')
		handler.end_headers()
		handler.wfile.write(f.read())

		return
			
	except Exception:
		exc_type, exc_value, exc_traceback = sys.exc_info()
		handler.log_error("%s", traceback.format_exception(exc_type, exc_value,exc_traceback))

		handler.wfile.write(
			"<h1>Aw, snap! We seem to have a problem.</h1><p><b>")
		handler.wfile.write(
			repr(traceback.format_exception(exc_type, exc_value,exc_traceback)))
		handler.wfile.write(
			"</b><p>Please report this error via private message to "
			"<a href='http://www.ravelry.com/people/beebell'>beebell on Ravelry</a>. "
			"It will be helpful if you include the pattern you uploaded to help me "
			"diagnose the issue.")

	finally:
		f.close()
