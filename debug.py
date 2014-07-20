
#
# WhistleSheet Debug File
#

import whistlesheet as ws

# Display all the frequencies from the pruned list
def display_frequencies():
	for note in ws.pruned_data_list:
		print note

# Print notes without their duration
def display_notes_without_duration():
	for note in ws.notes_list:
		print note[0],
		print note[1]

# Print notes with their duration
def display_notes_with_duration():
	for note in ws.notes_duration_list:
		print note[0], '\t', note[1],
		print ' (' , note[2], ')'
