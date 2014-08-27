from whistlesheet import WhistleSheet
import musicxmlconverter as mxc
import debug

def run_console_version():
	ws = WhistleSheet()
	ws.set_bpm(125)
	ws.set_time(20)
	ws.set_octave(6)
	# ws.record()
	# ws.play()
	ws.sheetify()

if __name__ == '__main__':
	run_console_version()
