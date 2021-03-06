
#
# WhistleSheet LilyPond Converter
#


from subprocess import Popen, PIPE
import os
import config


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
def convert_to_lilypond(notes_duration_list, SONG_ID, SONG_TITLE, SONG_COMPOSER, BPM, OCTAVE):
	print('Converting to Lilypond notation')
	ONE_BAR_DURATION = 64
	current_bar_duration = 0
	lily_notes = open(os.path.join(config.OUTPUT_FOLDER, '%s.ly' % SONG_ID), 'w')
	lily_notes.write('\\version "2.18.2"\n\n')
	lily_notes.write('\\pointAndClickOff\n')
	lily_notes.write('\\header {\n\ttitle = "%s"\n\ttagline = ""\n\tcomposer = "%s"\n}\n\n' % (SONG_TITLE, SONG_COMPOSER))
	lily_notes.write('\\absolute {\n\t\\clef treble\n\t\\tempo 4 = %d\n' % BPM)
	for n in notes_duration_list:
		note = n[0]
		octave = n[1]
		length = n[2]
		octave_char = convert_octave_to_lilypond(octave - OCTAVE + 4)
		while length > 1:
			# print "Current bar length is %d" % current_bar_duration
			# print "Note length is %d" % length
			carry_over_length = 0
			if current_bar_duration + length > ONE_BAR_DURATION:
				carry_over_length = length - (ONE_BAR_DURATION - current_bar_duration)
				length -= carry_over_length
				# print "New note length is %d" % length
				# print "Carrying over %d" % carry_over_length
			# print ""
			lily_notes.write('\t' + note)
			# if note == 'r':
				# lily_notes.write('\n')
			if note != 'r':
				lily_notes.write(octave_char)
			if length > 64:
				print "Length is greater than to 64"
				print "This is an error"
			if length >= 64:
				lily_notes.write('1\n')
				current_bar_duration += 64
				length -= 64
			# elif length >= 56:
			# 	lily_notes.write('2..\n')
			# 	current_bar_duration += 56
			# 	length -= 56
			elif length >= 48:
				lily_notes.write('2.\n')
				current_bar_duration += 48
				length -= 48
			elif length >= 32:
				lily_notes.write('2\n')
				current_bar_duration += 32
				length -= 32
			# elif length >= 28:
			# 	lily_notes.write('4..\n')
			# 	length -= 28
			elif length >= 24:
				lily_notes.write('4.\n')
				current_bar_duration += 24
				length -= 24
			elif length >= 16:
				lily_notes.write('4\n')
				current_bar_duration += 16
				length -= 16
			# elif length >= 14:
			# 	lily_notes.write('8..\n')
			# 	length -= 14
			elif length >= 12:
				lily_notes.write('8.\n')
				current_bar_duration += 12
				length -= 12
			elif length >= 8:
				lily_notes.write('8\n')
				current_bar_duration += 8
				length -= 8
			# elif length >= 7:
			# 	lily_notes.write('16..\n')
			# 	length -= 7
			elif length >= 6:
				lily_notes.write('16.\n')
				current_bar_duration += 6
				length -= 6
			elif length >= 4:
				lily_notes.write('16\n')
				current_bar_duration += 4
				length -= 4
			# elif length >= 2:
			# 	lily_notes.write('16-.\n')
			# 	current_bar_duration += 2
			# 	length -= 2
			else:
				print "Length was <4, discarding note"
				length = 0
			if carry_over_length > 0:
				lily_notes.write('~')
				if length == 0:
					current_bar_duration = 0
					lily_notes.write('\t\\bar "|" \n')
				length += carry_over_length
				carry_over_length = 0
			elif current_bar_duration == ONE_BAR_DURATION:
				current_bar_duration = 0
				lily_notes.write('\t\\bar "|" \n')
	lily_notes.write('\t\\bar "|."\n}')
	lily_notes.close()


# Typeset the Lilypond file into a PDF
def typeset_lilypond(SONG_ID):
	lilypond_bin = config.LILYPOND_BIN
	pdf_directory = os.path.join(config.OUTPUT_FOLDER, "%s" % SONG_ID)
	lily_directory = pdf_directory + ".ly"
	args = (lilypond_bin, "--output=" + pdf_directory, lily_directory)
	popen = Popen(args, stdout=PIPE)
	popen.wait()
	os.remove(lily_directory)
