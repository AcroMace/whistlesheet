import os
from flask import (Flask, request, redirect, render_template, make_response,
	               url_for, send_from_directory)
from whistlesheet import WhistleSheet
from random import randint


app = Flask(__name__)
app.config['OUTPUT_FOLDER'] = 'output'
app.config['INPUT_FOLDER']  = 'input'


# Make the directory if the directory does not already exist
#   name: name of the directory as a String
def make_directory(name):
	if not os.path.exists(name):
		os.makedirs(name)

# Used to make the input and output folders as the Lilypond binary
# only navigates to the folder if it exists and uses the
# directory parameter as the file name otherwise
def setup_directories():
	make_directory(app.config['OUTPUT_FOLDER'])
	make_directory(app.config['INPUT_FOLDER'])

# Makes sure that the file sent is a WAV file
# For "file.name.wav" returns ["file.name", "wav"]
def is_wav_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] == 'wav'


# Sends the PDF given the sheet number
@app.route("/sheet/<number>")
def show_results_page(number):
	return send_from_directory(app.config['OUTPUT_FOLDER'], '%s.pdf' % number)


@app.route("/", methods=['GET', 'POST'])
def home():
	if request.method == 'POST':
		file = request.files['song']
		print("Received data: %s" % request.form)
		if file and is_wav_file(file.filename):
			title = request.form['title']
			filename = str(randint(0, 100000000))
			file.save(os.path.join(app.config['INPUT_FOLDER'], '%s.wav' % filename))
			ws = WhistleSheet(filename)
			ws.set_bpm(125)
			ws.set_octave(5)
			if title: ws.set_title(title)
			try:
				ws.sheetify()
			except Exception, e: print "\nERROR: %s\n" % str(e)
			return filename
		return "Invalid request"
	return render_template('index.html')


if __name__ == '__main__':
	setup_directories()
	app.run()
