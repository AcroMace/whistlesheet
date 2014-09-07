import pyaudio # Record/play sound
import wave    # Sound file read/write
import os      # To check file existance and deletion

import config  # Config file with all the values

class WhistleRecorder:

	# time: Time to record in seconds
	def __init__(self, time=20, name=config.WAVE_OUTPUT_FILENAME):
		self.FORMAT   = pyaudio.paInt16
		self.CHANNELS = config.CHANNELS
		self.RATE     = config.RATE
		self.CHUNK    = config.CHUNK
		self.reset(time, name)

	def reset(self, time, name):
		self.RECORD_SECONDS       = time
		self.WAVE_OUTPUT_FILENAME = name

	# Changes the amount of seconds to record
	def set_time(self, time):
		self.RECORD_SECONDS = time

	# Changes the output name
	def set_output(self, name):
		self.WAVE_OUTPUT_FILENAME = name

	# Removes the old recording
	def remove_old_file(self):
		file_name = self.WAVE_OUTPUT_FILENAME
		if os.path.isfile(file_name):
			print('Existing %s detected' % file_name)
			print('Deleting previous file')
			os.remove(file_name)
		else:
			print('No previous instance of %s detected' % file_name)
			print('Making a new file')

	# Records sound
	def record(self):
		p = pyaudio.PyAudio()
		stream = p.open(format=self.FORMAT,
						channels=self.CHANNELS,
						rate=self.RATE,
						input=True,
						frames_per_buffer=self.CHUNK)

		frames = []

		print('Recording started')

		for i in range(int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
			data = stream.read(self.CHUNK)
			frames.append(data)

		stream.stop_stream()
		stream.close()
		p.terminate

		print('Recording ended, writing to file')

		self.remove_old_file()

		wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
		wf.setnchannels(self.CHANNELS)
		wf.setsampwidth(p.get_sample_size(self.FORMAT))
		wf.setframerate(self.RATE)
		wf.writeframes(''.join(frames))
		wf.close()

		print('Finished writing to file')


	# Plays the recorded sound
	def play(self):
		wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'rb')
		p = pyaudio.PyAudio()
		stream = p.open(format=self.FORMAT,
						channels=self.CHANNELS,
						rate=self.RATE,
						output=True)

		print('Playing sound')

		data = wf.readframes(self.CHUNK)

		while data != '':
			stream.write(data)
			data = wf.readframes(self.CHUNK)

		print('Finished playing sound')

		stream.stop_stream()
		stream.close()
		p.terminate()
