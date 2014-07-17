
#
# WhistleSheet Debug File
#

# Display all the frequencies from the pruned list
def display_frequencies(pruned_data_list):
	for note in pruned_data_list:
		print note

# Print notes without their duration
def display_notes_without_duration(notes_list):
	for note in notes_list:
		print note[0],
		print note[1]

# Print notes with their duration
def display_notes_with_duration(notes_duration_list):
	for note in notes_duration_list:
		print note[0], '\t', note[1],
		print ' (' , note[2], ')'
