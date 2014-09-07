from flask import Flask, request, render_template, make_response
from whistlesheet import WhistleSheet
app = Flask(__name__)


@app.route("/sheetify")
def get_sheet_music():
	ws = WhistleSheet()
	ws.set_bpm(125)
	ws.set_octave(5)
	ws.sheetify()
	return app.send_static_file('lilypond.pdf')

@app.route("/")
def hello():
	return render_template('index.html')

if __name__ == '__main__':
	app.run()
