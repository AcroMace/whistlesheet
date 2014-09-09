
#
# WhistleSheet MusicXML Converter
#


def get_music_xml_header(title):
	header = ('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
			  '<!DOCTYPE score-partwise PUBLIC\n'
			  '\t"-//Recordare//DTD MusicXML 3.0 Partwise//EN"\n'
			  '\t"http://www.musicxml.org/dtds/partwise.dtd">\n'
			  '<score-partwise version="3.0">\n'
			  '\t<credit page="1">\n'
			  '\t\t<credit-words font-size="24" default-x="510" default-y="1260" '
			  'justify="center" valign="top">'
			  '%s'
			  '</credit-words>\n'
			  '\t</credit>\n'
			  '\t<part-list>\n'
			  '\t\t<score-part id="P1">\n'
			  '\t\t\t<part-name>Whistle</part-name>\n'
			  '\t\t</score-part>\n'
			  '\t</part-list>\n'
			  '\t<part id="P1">\n')
	return header % title


def get_music_xml_first_measure_properties(numerator, denominator, bpm):
	measure = ('\t\t<measure number="1">\n'
			   '\t\t\t<attributes>\n'
			   '\t\t\t\t<divisions>64</divisions>\n'
			   '\t\t\t\t<key>\n'
          	   '\t\t\t\t\t<fifths>0</fifths>\n'
          	   '\t\t\t\t\t<mode>major</mode>\n'
        	   '\t\t\t\t</key>\n'
        	   '\t\t\t\t<time>\n'
	           '\t\t\t\t\t<beats>%d</beats>\n'
          	   '\t\t\t\t\t<beat-type>%d</beat-type>\n'
        	   '\t\t\t\t</time>\n'
        	   '\t\t\t\t<clef number="1">\n'
          	   '\t\t\t\t\t<sign>G</sign>\n'
          	   '\t\t\t\t\t<line>2</line>\n'
        	   '\t\t\t\t</clef>\n'
        	   '\t\t\t</attributes>\n'
        	   '\t\t\t<direction placement="above">\n'
        	   '\t\t\t\t<direction-type>\n'
	           '\t\t\t\t\t<metronome>\n'
               '\t\t\t\t\t\t<beat-unit>quarter</beat-unit>\n'
	           '\t\t\t\t\t\t<per-minute>%d</per-minute>\n'
	           '\t\t\t\t\t</metronome>\n'
	           '\t\t\t\t</direction-type>\n'
	           '\t\t\t\t<sound tempo="%d"/>\n'
      		   '\t\t\t</direction>\n')
	return measure % (numerator, denominator, bpm, bpm)



def get_music_xml_footer():
	footer = '\t</part>\n</score-partwise>\n'
	return footer


# Convert notes and duration to Lilypond notation
def convert_to_music_xml(notes_duration_list, SONG_ID, OCTAVE, BPM):
	ONE_BAR_DURATION = 256
	current_bar_duration = 0
	measure = 1
	# NEED TO SUPPORT SONG_ID
	wxml = open('output/%s.xml' % SONG_ID, 'w')
	wxml.write(get_music_xml_header('WhistleSheet Alpha'))
	wxml.write(get_music_xml_first_measure_properties(4, 4, BPM))
	for n in notes_duration_list:
		note = n[0]
		octave = n[1] - OCTAVE + 4
		length = n[2] * 4		
		while length > 1:
			carry_over_length = 0
			if current_bar_duration + length > ONE_BAR_DURATION:
				carry_over_length = length - (ONE_BAR_DURATION - current_bar_duration)
				length -= carry_over_length
			wxml.write('\t\t\t<note>\n')
			if note == 'r':
				wxml.write('\t\t\t\t<rest/>\n')
			else:
				wxml.write('\t\t\t\t<pitch>\n')
				if len(note) == 1:
					wxml.write('\t\t\t\t\t<step>%s</step>\n' % note.upper())
				else:
					wxml.write('\t\t\t\t\t<step>%s</step>\n' % note[0].upper())
					if note[1:3] == 'es':
						wxml.write('\t\t\t\t\t<alter>-1</alter>\n')
					elif note[1:3] == 'is':
						wxml.write('\t\t\t\t\t<alter>1</alter>\n')
				wxml.write('\t\t\t\t\t<octave>%d</octave>\n' % octave)
				wxml.write('\t\t\t\t</pitch>\n')
			if length > 256:
				print "Length is greater than to 64"
				print "This is an error"
			if length >= 256:
				print "This should be a full bar"
				wxml.write('\t\t\t\t<duration>%d</duration>\n' % 256)
				wxml.write('\t\t\t\t<type>%s</type>\n' % 'whole')
				current_bar_duration += 256
				length -= 256
			elif length >= 128:
				wxml.write('\t\t\t\t<duration>%d</duration>\n' % 128)
				wxml.write('\t\t\t\t<type>%s</type>\n' % 'half')
				current_bar_duration += 128
				length -= 128
			elif length >= 64:
				wxml.write('\t\t\t\t<duration>%d</duration>\n' % 64)
				wxml.write('\t\t\t\t<type>%s</type>\n' % 'quarter')
				current_bar_duration += 64
				length -= 64
			elif length >= 32:
				wxml.write('\t\t\t\t<duration>%d</duration>\n' % 32)
				wxml.write('\t\t\t\t<type>%s</type>\n' % 'eighth')
				current_bar_duration += 32
				length -= 32
			elif length >= 16:
				wxml.write('\t\t\t\t<duration>%d</duration>\n' % 16)
				wxml.write('\t\t\t\t<type>%s</type>\n' % '16th')
				current_bar_duration += 16
				length -= 16
			else:
				print "Length was <16, discarding note"
				length = 0
			wxml.write('\t\t\t</note>\n')
			if carry_over_length > 0:
				if length == 0:
					current_bar_duration = 0
					measure += 1
					wxml.write('\t\t</measure>\n')
					wxml.write('\t\t<measure number="%d">\n' % measure)
					wxml.write('\t\t\t<attributes/>\n')
				length += carry_over_length
				carry_over_length = 0
			elif current_bar_duration == ONE_BAR_DURATION:
				current_bar_duration = 0
				measure += 1
				wxml.write('\t\t</measure>\n')
				wxml.write('\t\t<measure number="%d">\n' % measure)
				wxml.write('\t\t\t<attributes/>\n')
	wxml.write('\t\t\t<barline location="right">\n')
	wxml.write('\t\t\t\t<bar-style>light-heavy</bar-style>\n')
	wxml.write('\t\t\t</barline>\n\t\t</measure>\n')
	wxml.write(get_music_xml_footer())
	wxml.close()
