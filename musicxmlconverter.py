
#
# WhistleSheet MusicXML Converter
#

from os import system


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


def get_music_xml_footer():
	footer = '\t</part>\n</score-partwise>\n'
	return footer

