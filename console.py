from whistlesheet import WhistleSheet
from whistlerecorder import WhistleRecorder
import musicxmlconverter as mxc

def run_console_version():
	ws = WhistleSheet()
	# wr = WhistleRecorder()
	ws.set_bpm(125)
	# wr.set_time(20)
	ws.set_octave(6)
	# wr.record()
	# wr.play()
	ws.sheetify()

if __name__ == '__main__':
	run_console_version()
