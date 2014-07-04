import pyaudio
import wave    # Sound file read/write
import os      # To check file existance and deletion
import time    # For sleep


# CONFIG
FORMAT 	 = pyaudio.paInt16	# Mac default is Int24
CHANNELS = 2				# Mac default
RATE     = 44100 			# Mac default
CHUNK    = 1024				# Decrease number to increase frequency detection speed
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = 'whistle.wav'


def remove_old_file():
	if os.path.isfile(WAVE_OUTPUT_FILENAME):
		print('Existing %s detected' % WAVE_OUTPUT_FILENAME)
		print('Deleting previous file')
		os.remove(WAVE_OUTPUT_FILENAME)
	else:
		print('No previous instance of %s detected' % WAVE_OUTPUT_FILENAME)
		print('Making a new file')


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


if __name__ == '__main__':
	record()
	play()
