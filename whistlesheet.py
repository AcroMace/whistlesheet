import pyaudio # Record/play sound
import wave    # Sound file read/write
import os      # To check file existance and deletion; typeset lilypond
import numpy   # Used for FFT
from collections import deque # Lists with fast pops and appends on both sides

# CONFIG
FORMAT 	  = pyaudio.paInt16	# Mac default is Int24 (16 bit signed integer)
CHANNELS  = 2				# Mac default (# of audio channels)
RATE      = 44100 			# Mac default (Hz, audio samples per second)
CHUNK     = 1024			# Decrease number to increase frequency detection speed
RECORD_SECONDS = 20			# Number of seconds that are recorded by record()
THRESHOLD = 50000			# Peak needed to be counted as input
OCTAVE    = 5				# Octave that counts as the fourth octave on the sheet
BPM       = 135				# Default BPM, affects CHUNK with set_bpm
BOT_FREQ  = 500             # Lowest frequency considered to be whistling
TOP_FREQ  = 5000            # Highest frequency considered to be whistling
WAVE_OUTPUT_FILENAME = 'whistle.wav' # record() will save the audio file as this name
LILY_OUTPUT_FILENAME = 'lilypond.ly' # convert_to_lilypond() will save the notes as this


# Input organized as [frequency, int(|peak|)]
raw_data_list = []

# List of frequencies with random noise filtered out [frequency]
pruned_data_list = deque([])

# Maximum frequencies needed to be considered a certain note
# In the form of [frequency, note, octave]
max_freq_list = []

# Frequencies converted into notes
# In the form of [note, octave]
notes_list = []

# Notes with durations
# In the form of [note, octave, duration]
notes_duration_list = []


# Changes the CHUNK size based on the BPM
def set_bpm(bpm=BPM):
	# (RATE samples / 1 second)
	# (60 seconds / 1 min)
	# (1 min / BPM beats)
	# (1 beat / 16 points)
	CHUNK = int(RATE * 60 / BPM / 16)


# Changes the octave
def set_octave(octave=OCTAVE):
	OCTAVE = octave


# Removes the old recording
def remove_old_file():
	if os.path.isfile(WAVE_OUTPUT_FILENAME):
		print('Existing %s detected' % WAVE_OUTPUT_FILENAME)
		print('Deleting previous file')
		os.remove(WAVE_OUTPUT_FILENAME)
	else:
		print('No previous instance of %s detected' % WAVE_OUTPUT_FILENAME)
		print('Making a new file')


# Records sound
def record():
	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					input=True,
					frames_per_buffer=CHUNK)

	frames = []

	print('Recording started')

	for i in range(int(RATE / CHUNK * RECORD_SECONDS)):
		data = stream.read(CHUNK)
		frames.append(data)

	stream.stop_stream()
	stream.close()
	p.terminate

	print('Recording ended, writing to file')

	remove_old_file()

	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(''.join(frames))
	wf.close()

	print('Finished writing to file')


# Plays the recorded sound
def play():
	wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
	p = pyaudio.PyAudio()
	stream = p.open(format=FORMAT,
					channels=CHANNELS,
					rate=RATE,
					output=True)

	print('Playing sound')

	data = wf.readframes(CHUNK)

	while data != '':
		stream.write(data)
		data = wf.readframes(CHUNK)

	print('Finished playing sound')

	stream.stop_stream()
	stream.close()
	p.terminate()


# Calculates the frequencies from the recording
def get_frequencies():
	# Opens the file saved by record()
	wf = wave.open(WAVE_OUTPUT_FILENAME, 'rb')
	# Reads CHUNK amount of frames
	data = wf.readframes(CHUNK)
	# Honestly not sure why the data length is CHUNK * 4, but this works for now
	while len(data) == CHUNK * CHANNELS * 2:
		# Unpacks the data
		unpacked_data = numpy.array(wave.struct.unpack("%dh"%(len(data)/2), data))
		# FFT on the unpacked data
		spectrum = numpy.fft.rfft(unpacked_data, RATE * CHANNELS)
		# Find the maximum
		# The max should be approximately accurate enough to map to a note
		peak = numpy.argmax(abs(spectrum))
		raw_data_list.append([peak, int(abs(spectrum[peak]))])
		data = wf.readframes(CHUNK)
	wf.close()


# Get rid of all frequencies that are likely not whistling
def mute_noise():
	for note in raw_data_list:
		# Human whistling frequencies range from 500 Hz to 5000 Hz
		if note[0] < BOT_FREQ or note[0] > TOP_FREQ or note[1] < THRESHOLD:
			pruned_data_list.append(0)
		else:
			pruned_data_list.append(note[0])


# Gets rid of all the zeros from the start
def prune_empty_sounds():
	notes_to_pop = 0
	for note in pruned_data_list:
		if note == 0:
			notes_to_pop += 1
		else:
			break
	for note in range(notes_to_pop):
		pruned_data_list.popleft()


# Display all the frequencies from the pruned list
def display_frequencies():
	for note in pruned_data_list:
		print note


# Populate the maximum frequencies list
def populate_max_freq_list():
	all_notes = ['a', 'bes', 'b', 'c', 'cis', 'd', 'ees', 'e', 'f', 'fis', 'g', 'aes']
	current_note = 0
	current_octave = 4
	current_freq = 440.00 # A4
	one_note_difference = pow(2.0, 1.0/12.0)
	current_freq *= pow(2.0, 1.0/24.0) # Half a note higher than A4	
	while current_freq <= TOP_FREQ:
		max_freq_list.append([current_freq, all_notes[current_note], current_octave])
		current_freq *= one_note_difference
		current_note += 1
		if current_note == 3: # note is C
			current_octave += 1
		elif current_note == 12: # note is A
			current_note = 0 # reset to beginning of list


# Convert a single frequency to a note
def map_frequency_to_note(freq):
	for maximum in max_freq_list:
		if freq == 0:
			return ['r', 0] # for rests
		elif freq < maximum[0]:
			return [maximum[1], maximum[2]]
	raise Exception('The input frequency was too high')


# Convert the frequencies into notes
def map_frequencies_to_notes():
	for freq in pruned_data_list:
		notes_list.append(map_frequency_to_note(freq))


# Print notes without their duration
def display_notes_without_duration():
	for note in notes_list:
		print note[0],
		print note[1]


# Add duration to the frequencies
def get_duration():
	notes_list_length = len(notes_list)
	current_note = 'n' # placeholder note
	current_octave = 0
	current_length = 0
	for l in range(notes_list_length):
		note = notes_list[l]
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
			notes_duration_list.append([current_note, current_octave, current_length])
			current_note = next_note
			current_octave = next_octave
			current_length = 1


# Print notes with their duration
def display_notes_with_duration():
	for note in notes_duration_list:
		print note[0], '\t', note[1],
		print ' (' , note[2], ')'


# Convert octave number to Lilypond notation
def convert_octave_to_lilypond(octave):
	quotes_and_commas = ''
	while octave != 4:
		if octave > 4:
			quotes_and_commas += "'"
			octave -= 1
		else:
			quotes_and_commas += ","
			octave += 1
	return quotes_and_commas


# Convert notes and duration to Lilypond notation
def convert_to_lilypond():
	print('Converting to Lilypond notation')
	lily_notes = open('lilypond.ly', 'w')
	lily_notes.write('\\version "2.18.2"\n\n')
	lily_notes.write('\\header {\n\ttitle = "WhistleSheet Alpha"\n}\n\n')
	lily_notes.write('\\absolute {\n\t\\clef treble\n')
	for n in notes_duration_list:
		note = n[0]
		octave = n[1]
		length = n[2]
		octave_char = convert_octave_to_lilypond(octave - OCTAVE + 4)
		while length > 1:
			lily_notes.write('\t' + note)
			if note != 'r':
				lily_notes.write(octave_char)
			if length >= 64:
				lily_notes.write('1\n')
				length -= 64
			elif length >= 56:
				lily_notes.write('2..\n')
				length -= 56
			elif length >= 48:
				lily_notes.write('2.\n')
				length -= 48
			elif length >= 32:
				lily_notes.write('2\n')
				length -= 32
			# elif length >= 28:
			# 	lily_notes.write('4..\n')
			# 	length -= 28
			elif length >= 24:
				lily_notes.write('4.\n')
				length -= 24
			elif length >= 16:
				lily_notes.write('4\n')
				length -= 16
			# elif length >= 14:
			# 	lily_notes.write('8..\n')
			# 	length -= 14
			elif length >= 12:
				lily_notes.write('8.\n')
				length -= 12
			elif length >= 8:
				lily_notes.write('8\n')
				length -= 8
			# elif length >= 7:
			# 	lily_notes.write('16..\n')
			# 	length -= 7
			elif length >= 6:
				lily_notes.write('16.\n')
				length -= 6
			elif length >= 4:
				lily_notes.write('16\n')
				length -= 4
			elif length >= 2:
				lily_notes.write('16-.\n')
				length -= 2
			else:
				length = 0
	lily_notes.write('\t\\bar "|."\n}')
	lily_notes.close()


# Typeset the Lilypond file into a PDF
def typeset_lilypond():
	os.system("lilypond --pdf " + LILY_OUTPUT_FILENAME)



if __name__ == '__main__':
	set_bpm(135)
	set_octave(6)
	# record()
	# play()
	get_frequencies()
	mute_noise()
	prune_empty_sounds()
	# display_frequencies()
	populate_max_freq_list()
	map_frequencies_to_notes()
	# display_notes_without_duration()
	get_duration()
	# display_notes_with_duration()
	convert_to_lilypond()
	typeset_lilypond()

