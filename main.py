import whistlesheet as ws

from datetime import datetime as time

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Line


class WSBpmBox(Widget):

	# Number of taps, initial tap time, final tap time
	num_of_taps = [0, 0, 0]
	bpm = 0

	def on_touch_down(self, touch):
		color = (0.5, 1, 1)
		with self.canvas:
			Color(*color, mode='hsv')
		if self.num_of_taps[0] == 0:
			self.num_of_taps[0] = 1
			self.num_of_taps[1] = time.now()
			self.num_of_taps[2] = self.num_of_taps[1]
			print "Only one tap, BPM cannot be calculated"
		else:
			self.num_of_taps[0] += 1
			self.num_of_taps[2] = time.now()
			time_difference = (self.num_of_taps[2] - self.num_of_taps[1]).total_seconds()
			self.bpm = 60 * self.num_of_taps[0] / time_difference
			ws.set_bpm(int(self.bpm))
			print int(self.bpm)


# class WSRecordButton(Button):

	# text = "Clear"


class WhistleSheetApp(App):

	def build(self):

		parent = Widget()
		bpm_box = WSBpmBox()
		# record_button = WSRecordButton()
		
		parent.add_widget(bpm_box)
		# parent.add_widget(WSRecordButton)

		return parent


def do_actual_calculation_stuff():
	ws.set_time(20)
	ws.set_octave(6)
	# ws.record()
	# ws.play()
	ws.get_frequencies()
	ws.mute_noise()
	ws.prune_empty_sounds()
	ws.populate_max_freq_list()
	ws.add_frequency_variation_tolerance()
	ws.map_frequencies_to_notes()
	ws.get_duration()
	ws.add_frame_drop_tolerance()
	ws.repeatedly_add_frame_drop_tolerance()
	ws.add_duration_rounding()
	ws.convert_to_lilypond()
	ws.typeset_lilypond()

if __name__ == '__main__':
	WhistleSheetApp().run()
	do_actual_calculation_stuff()
