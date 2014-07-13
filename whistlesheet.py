import pyaudio # Record/play sound
import wave    # Sound file read/write
import os      # To check file existance and deletion
import numpy   # Used for FFT
from collections import deque # Lists with fast pops and appends on both sides

# CONFIG
FORMAT 	  = pyaudio.paInt16	# Mac default is Int24 (16 bit signed integer)
CHANNELS  = 2				# Mac default (# of audio channels)
RATE      = 44100 			# Mac default (Hz, audio samples per second)
CHUNK     = 1024			# Decrease number to increase frequency detection speed
RECORD_SECONDS = 5			# Number of seconds that are recorded by record()
THRESHOLD = 50000			# Peak needed to be counted as input
WAVE_OUTPUT_FILENAME = 'whistle.wav' # record() will save the audio file as this name


# Input organized as [frequency, int(|peak|)]
raw_data_list = []

# Input with noise filtered out
pruned_data_list = deque([])


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
		if note[0] < 500 or note[0] > 5000 or note[1] < THRESHOLD:
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


# Dispaly all the frequencies from the pruned list
def display_frequencies():
	for note in pruned_data_list:
		print note


if __name__ == '__main__':
	# record()
	# play()
	get_frequencies()
	mute_noise()
	prune_empty_sounds()
	display_frequencies()

