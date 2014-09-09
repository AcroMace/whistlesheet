from whistlesheet import WhistleSheet
from whistlerecorder import WhistleRecorder
import musicxmlconverter as mxc
from sys import argv


def run_console_version(filename):
	ws = WhistleSheet(filename)
	# wr = WhistleRecorder()
	ws.set_bpm(125)
	# wr.set_time(20)
	ws.set_octave(6)
	# wr.record()
	# wr.play()
	ws.sheetify()

if __name__ == '__main__':
	arguments = argv[1:]
	if arguments:
		run_console_version(arguments[0])
	else:
		raise Exception("Please provide the name of the WAV file as an argument")
