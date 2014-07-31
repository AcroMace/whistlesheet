import whistlesheet as ws
import musicxmlconverter as mxc
import debug

def run_console_version():
	ws.set_bpm(125)
	ws.set_time(20)
	ws.set_octave(6)
	# ws.record()
	# ws.play()
	ws.get_frequencies()
	ws.mute_noise()
	ws.prune_empty_sounds()
	# debug.display_frequencies()
	ws.populate_max_freq_list()
	ws.add_frequency_variation_tolerance()
	# debug.display_frequencies()
	ws.map_frequencies_to_notes()
	# debug.display_notes_without_duration()
	ws.get_duration()
	# debug.display_notes_with_duration()
	ws.add_frame_drop_tolerance()
	# debug.display_notes_with_duration()
	ws.repeatedly_add_frame_drop_tolerance()
	# debug.display_notes_with_duration()
	ws.add_duration_rounding()
	# debug.display_notes_with_duration()
	# ws.convert_to_lilypond()
	ws.convert_to_music_xml()

if __name__ == '__main__':
	run_console_version()
