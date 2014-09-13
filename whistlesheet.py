import wave    # Sound file read/write
import numpy   # Used for FFT
from collections import deque # Lists with fast pops and appends on both sides
from os import path # File paths with Windows support

import config                    # Config file with all the values
import lilyconverter as lily     # Convert notes_duration_list to a LilyPond file
import musicxmlconverter as mxml # Convert notes_duration_list to a MusicXML file

class WhistleSheet:

	def __init__(self, song_id):
		self.INPUT_FOLDER  = 'input'
		# self.OUTPUT_FOLDER = 'output'
		self.reset(song_id)

	def reset(self, song_id):
		# CONFIG
		self.CHANNELS             = config.CHANNELS
		self.RATE                 = config.RATE
		self.CHUNK                = config.CHUNK
		self.THRESHOLD            = config.THRESHOLD
		self.OCTAVE               = config.OCTAVE
		self.BPM                  = config.BPM
		self.TITLE                = config.DEFAULT_TITLE
		self.BOT_FREQ             = config.BOT_FREQ
		self.TOP_FREQ             = config.TOP_FREQ
		self.FREQ_TOLERANCE       = config.FREQ_TOLERANCE
		self.DROP_TOLERANCE       = config.DROP_TOLERANCE
		self.SONG_ID              = song_id

		# Input organized as [frequency, int(|peak|)]
		self.raw_data_list = []

		# List of frequencies with random noise filtered out [frequency]
		self.pruned_data_list = deque([])

		# Maximum frequencies needed to be considered a certain note
		# In the form of [frequency, note, octave]
		self.max_freq_list = []

		# Frequencies converted into notes
		# In the form of [note, octave]
		self.notes_list = []

		# Notes with durations
		# In the form of [note, octave, duration]
		self.notes_duration_list = []


	# Changes the CHUNK size based on the BPM
	def set_bpm(self, bpm):
		# (RATE samples / 1 second)
		# (60 seconds / 1 min)
		# (1 min / BPM beats)
		# (1 beat / 16 points)
		self.CHUNK = int(self.RATE * 60 / self.BPM / 16)

	# Changes the octave
	def set_octave(self, octave):
		self.OCTAVE = octave

	# Changes the title of the song (for output)
	def set_title(self, title):
		self.TITLE = title

	# Calculates the frequencies from the recording
	def get_frequencies(self):
		# Opens the file saved by record()
		wf = wave.open(path.join(self.INPUT_FOLDER, '%s.wav' % self.SONG_ID), 'rb')
		# Reads CHUNK amount of frames
		data = wf.readframes(self.CHUNK)
		# Honestly not sure why the data length is CHUNK * 4, but this works for now
		while len(data) == self.CHUNK * self.CHANNELS * 2:
			# Unpacks the data
			unpacked_data = numpy.array(wave.struct.unpack("%dh"%(len(data)/2), data))
			# FFT on the unpacked data
			spectrum = numpy.fft.rfft(unpacked_data, self.RATE * self.CHANNELS)
			# Find the maximum
			# The max should be approximately accurate enough to map to a note
			peak = numpy.argmax(abs(spectrum))
			self.raw_data_list.append([peak, int(abs(spectrum[peak]))])
			data = wf.readframes(self.CHUNK)
		wf.close()


	# Get rid of all frequencies that are likely not whistling
	def mute_noise(self):
		for note in self.raw_data_list:
			# Human whistling frequencies range from 500 Hz to 5000 Hz
			if note[0] < self.BOT_FREQ or note[0] > self.TOP_FREQ or note[1] < self.THRESHOLD:
				self.pruned_data_list.append(0)
			else:
				self.pruned_data_list.append(note[0])


	# Gets rid of all the zeros from the start
	def prune_empty_sounds(self):
		notes_to_pop = 0
		for note in self.pruned_data_list:
			if note == 0:
				notes_to_pop += 1
			else:
				break
		for note in range(notes_to_pop):
			self.pruned_data_list.popleft()


	# Populate the maximum frequencies list
	def populate_max_freq_list(self):
		all_notes = ['a', 'bes', 'b', 'c', 'cis', 'd', 'ees', 'e', 'f', 'fis', 'g', 'aes']
		current_note = 0
		current_octave = 4
		current_freq = 440.00 # A4
		one_note_difference = pow(2.0, 1.0/12.0)
		current_freq *= pow(2.0, 1.0/24.0) # Half a note higher than A4	
		while current_freq <= self.TOP_FREQ:
			self.max_freq_list.append([current_freq, all_notes[current_note], current_octave])
			current_freq *= one_note_difference
			current_note += 1
			if current_note == 3: # note is C
				current_octave += 1
			elif current_note == 12: # note is A
				current_note = 0 # reset to beginning of list


	# Convert a single frequency to a note
	def map_frequency_to_note(self, freq):
		for maximum in self.max_freq_list:
			if freq == 0:
				return ['r', 0] # for rests
			elif freq < maximum[0]:
				return [maximum[1], maximum[2]]
		# raise Exception('The input frequency was too high')


	# Convert the frequencies into notes
	def map_frequencies_to_notes(self):
		for freq in self.pruned_data_list:
			self.notes_list.append(self.map_frequency_to_note(freq))


	# Check if two notes are within frequency tolerance
	# note1: frequency of the first note
	# note2: frequency of the second note
	def is_within_tolerance_level(self, freq1, freq2):
		max_tol = self.FREQ_TOLERANCE
		if freq1 == freq2:
			return True
		elif freq1 < freq2:
			return freq2 < (freq1 * max_tol)
		else:
			return freq1 < (freq2 * max_tol)


	# Add error tolerance for frequency variation
	def add_frequency_variation_tolerance(self):
		pdl       = self.pruned_data_list
		pdl_len   = len(self.pruned_data_list)
		cur_avg   = 0 # Average of the current total frequencies
		cur_tot   = 0 # Total of the current frequencies
		cur_count = 1 # Number of frequencies currently being considered
		for i in range(pdl_len):
			if self.is_within_tolerance_level(cur_avg, pdl[i]):
				# Updates the total, count, average
				cur_tot += pdl[i]
				cur_count += 1
				cur_avg = cur_tot / cur_count
			else:
				# Overwrite all notes included in average with average
				if cur_count != 1:
					for c in range(cur_count):
						pdl[i - cur_count + c] = cur_avg
				cur_avg = pdl[i]
				cur_tot = pdl[i]
				cur_count = 1
		self.pruned_data_list = pdl


	# Add duration to the notes
	def get_duration(self):
		notes_list_length = len(self.notes_list)
		current_note = 'n' # placeholder note
		current_octave = 0
		current_length = 0
		for l in range(notes_list_length):
			note = self.notes_list[l]
			next_note = note[0]
			next_octave = note[1]
			if (current_note == 'n'):
				# Initial run
				current_note = next_note
				current_octave = next_octave
				current_length = 1
			elif (current_note == next_note and current_octave == next_octave):
				current_length += 1
			else:
				self.notes_duration_list.append([current_note, current_octave, current_length])
				current_note = next_note
				current_octave = next_octave
				current_length = 1


	# Add error tolerance for frame drops
	def add_frame_drop_tolerance(self):
		ndl        = self.notes_duration_list
		ndl.insert(0, ['z', 0, 0]) # To check first item
		ndl_new    = []  # New notes_duration_list
		ndl_len    = len(self.notes_duration_list)
		max_tol    = self.DROP_TOLERANCE # Minimum number of duration required
		                                 # to count as a note
		for n in range(ndl_len - 2):
			cur_item   = ndl[n]     # Current item to test
			next_item  = ndl[n + 1] # Item directly after curent item
			check_item = ndl[n + 2] # Second item from current item
			# Skips to the next item if the current note has been overwritten
			cur_note   = cur_item[0]
			if cur_note == 'n': continue
			# Skips to the next item if the next note cannot be overwritten
			next_length = next_item[2]
			if next_length > max_tol:
				ndl_new.append(cur_item)
				continue
			# Rest of the definitions required for checks
			cur_octave   = cur_item[1]
			cur_length   = cur_item[2]
			check_note   = check_item[0]
			check_octave = check_item[1]
			check_length = check_item[2]
			# Checking note after the one adjacent to the current one
			if cur_note == check_note and cur_octave == check_octave:
				# Combine the current, next, and checked notes
				ndl_new.append([cur_note, cur_octave, cur_length + next_length + check_length])
				# Overwrite the next note
				ndl[n + 1][0] = 'n'
				# Overwrite the checked note
				ndl[n + 2][0] = 'n'
			else:
				# Combine the current and checked notes
				ndl_new.append([cur_note, cur_octave, cur_length + next_length])
				# Overwrite the checked note
				ndl[n + 1][0] = 'n'
		del ndl_new[0]
		self.notes_duration_list = ndl_new


	# Repeatedly calls add_frame_drop_tolerance
	def repeatedly_add_frame_drop_tolerance(self):
		length = len(self.notes_duration_list)
		while True:
			i = 1
			for n in self.notes_duration_list:
				i += 1
				if n[2] <= self.DROP_TOLERANCE:
					self.add_frame_drop_tolerance()
					break
			length = len(self.notes_duration_list)
			if i >= length:
				break


	# This should be moved to a helper module
	# Returns true if a <= b <= c
	def between(self, a, b, c):
		return a <= b and b <= c


	# Round numbers for better formatting
	# May want to precalculate the ranges if pushing to mobile
	# Keeping it this way for now for cleaner code
	def add_duration_rounding(self):
		for note in self.notes_duration_list:
			length = note[2]
			if length <= 5:
				note[2] = 0
			# elif between(3, length, 5):
			# 	# sixteenth note
			# 	note[2] = 4
			elif self.between(6, length, 10):
				# eighth note
				note[2] = 8
			elif self.between(11, length, 13):
				note[2] = 12
			elif self.between(14, length, 20):
				# quarter note
				note[2] = 16
			elif self.between(21, length, 28):
				# quarter and a half note
				note[2] = 24
			elif self.between(29, length, 40):
				# half note
				note[2] = 32
			elif self.between(41, length, 56):
				# half and a half note
				note[2] = 48
			elif self.between(57, length, 72):
				# whole note
				note[2] = 64


	# Convert notes_duration_list to a LilyPond file
	def convert_to_lilypond(self, typeset=True):
		lily.convert_to_lilypond(self.notes_duration_list, self.SONG_ID, self.TITLE, self.OCTAVE)
		if typeset:
			lily.typeset_lilypond(self.SONG_ID)


	# Convert notes_duration_list to a MusicXML file
	def convert_to_music_xml(self):
		mxml.convert_to_music_xml(self.notes_duration_list, self.SONG_ID, self.TITLE, self.OCTAVE, self.BPM)


	# Take the WAV file and convert it to Lilypond or XML
	def sheetify(self, type='lilypond', typeset=True):
		self.get_frequencies()
		self.mute_noise()
		self.prune_empty_sounds()
		self.populate_max_freq_list()
		self.add_frequency_variation_tolerance()
		self.map_frequencies_to_notes()
		self.get_duration()
		self.add_frame_drop_tolerance()
		self.repeatedly_add_frame_drop_tolerance()
		self.add_duration_rounding()
		if (type == 'lilypond'):
			self.convert_to_lilypond()
		else:
			self.convert_to_music_xml()
