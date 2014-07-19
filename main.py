import whistlesheet as ws
import debug

if __name__ == '__main__':
	ws.set_bpm(135)
	ws.set_octave(6)
	# ws.record()
	# ws.play()
	ws.get_frequencies()
	ws.mute_noise()
	ws.prune_empty_sounds()
	# debug.display_frequencies(pruned_data_list)
	ws.populate_max_freq_list()
	# ws.map_frequencies_to_notes()
	ws.map_frequencies_to_notes_with_tolerance()
	# debug.display_notes_without_duration(notes_list)
	ws.get_duration()
	# debug.display_notes_with_duration(notes_duration_list)
	ws.convert_to_lilypond()
	ws.typeset_lilypond()
