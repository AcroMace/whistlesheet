import os
from flask import (Flask, request, redirect, render_template, make_response,
	               url_for, send_from_directory)
from whistlesheet import WhistleSheet
from random import randint

OUTPUT_FOLDER = 'output'
UPLOAD_FOLDER = 'input'


app = Flask(__name__)
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def is_wav_file(filename):
	# For "file.name.wav" returns ["file.name", "wav"]
	return '.' in filename and filename.rsplit('.', 1)[1] == 'wav'


@app.route("/", methods=['GET', 'POST'])
def hello():
	if request.method == 'POST':
		file = request.files['file']
		if file and is_wav_file(file.filename):
			filename = str(randint(0, 100000000))
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], '%s.wav' % filename))
			ws = WhistleSheet(filename)
			ws.set_bpm(125)
			ws.set_octave(5)
			ws.sheetify()
			return send_from_directory(app.config['OUTPUT_FOLDER'], '%s.pdf' % filename)
	return render_template('index.html')


if __name__ == '__main__':
	app.run()
