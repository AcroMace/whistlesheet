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
	# debug.display_frequencies()
	ws.populate_max_freq_list()
	ws.add_frequency_variation_tolerance()
	# debug.display_frequencies()
	ws.map_frequencies_to_notes()
	# debug.display_notes_without_duration()
	ws.get_duration()
	# debug.display_notes_with_duration()
	ws.convert_to_lilypond()
	ws.typeset_lilypond()
