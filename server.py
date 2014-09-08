import os
from flask import (Flask, request, redirect, render_template, make_response,
	               url_for, send_from_directory)
from werkzeug import secure_filename
from whistlesheet import WhistleSheet

OUTPUT_FOLDER = 'output'
UPLOAD_FOLDER = 'uploads'


app = Flask(__name__)
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def is_wav_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1] == 'wav'


@app.route("/sheetify")
def get_sheet_music():
	ws = WhistleSheet()
	ws.set_bpm(125)
	ws.set_octave(5)
	ws.sheetify()
	return send_from_directory(app.config['OUTPUT_FOLDER'], 'lilypond.pdf')

@app.route("/", methods=['GET', 'POST'])
def hello():
	if request.method == 'POST':
		file = request.files['file']
		if file and is_wav_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			print url_for('uploaded_file',
				filename=filename)
			return redirect(url_for('uploaded_file',
				filename=filename))
	return render_template('index.html')

@app.route("/uploads/<filename>")
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
	app.run()
