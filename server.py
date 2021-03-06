import os
from flask import (Flask, request, render_template, send_from_directory)
from whistlesheet import WhistleSheet
import config
from random import randint


app = Flask(__name__)


# Make the directory if the directory does not already exist
#   name: name of the directory as a String
def make_directory(name):
	if not os.path.exists(name):
		os.makedirs(name)

# Used to make the input and output folders as the Lilypond binary
# only navigates to the folder if it exists and uses the
# directory parameter as the file name otherwise
def setup_directories():
	make_directory(config.OUTPUT_FOLDER)
	make_directory(config.INPUT_FOLDER)

# Makes sure that the file sent is a WAV file
# For "file.name.wav" returns ["file.name", "wav"]
def is_wav_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] == 'wav'

# Gets the values from a form and returns a tuple of the values
# Inserts an empty string if the key does not exist
#   request: flask request object
#   values: tuple of keys in the request
def get_form_values(request, values):
	return_values = tuple()
	for value in values:
		try:
			return_values += (request.form[value],)
		except KeyError:
			return_values += ('',)
	return return_values


# Sends the PDF given the sheet number
@app.route("/sheet/<number>")
def show_results_page(number):
	return send_from_directory(config.OUTPUT_FOLDER, '%s.pdf' % number)


@app.route("/", methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		file = request.files['song']
		print("Received data: %s" % request.form)
		if file and is_wav_file(file.filename):
			title, composer, bpm = get_form_values(request, ('title', 'composer', 'bpm'))
			filename = str(randint(0, 100000000))
			file.save(os.path.join(config.INPUT_FOLDER, '%s.wav' % filename))
			ws = WhistleSheet(filename)
			if title: ws.set_title(title)
			if composer: ws.set_composer(composer)
			if bpm: ws.set_bpm(bpm) # automatically converted to int
			try:
				ws.sheetify()
			except Exception, e: print "\nERROR: %s\n" % str(e)
			return filename
		return "Invalid request"
	return render_template('index.html')


@app.errorhandler(404)
def page_not_found(e):
	return render_template('error.html'), 404

@app.errorhandler(500)
def application_error(e):
	return render_template('error.html'), 500


if __name__ == '__main__':
	setup_directories()
	app.run()
