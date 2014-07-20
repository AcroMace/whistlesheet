
#
# WhistleSheet Config File
#


#
# Recording config
#
CHANNELS       = 2     # Mac default (# of audio channels)
RATE           = 44100 # Mac default (Hz, audio samples per second)
CHUNK          = 1024  # Decrease number to increase frequency detection speed
RECORD_SECONDS = 20    # Number of seconds that are recorded by record()


#
# Threshold config
#
THRESHOLD      = 50000              # Peak needed to be counted as input
BOT_FREQ       = 500                # Lowest frequency considered to be whistling
TOP_FREQ       = 5000               # Highest frequency considered to be whistling
FREQ_TOLERANCE = pow(2.0, 1.0/18.0) # Max tolerance before being considered another note
DROP_TOLERANCE = 2                  # Max dropped frames before counting as another note

#
# Interpretation config
#
OCTAVE    = 5   # Octave that counts as the fourth octave on the sheet
BPM       = 135 # Default BPM, affects CHUNK with set_bpm()


#
# Output config
#
WAVE_OUTPUT_FILENAME = 'whistle.wav' # record() will save the audio file as this name
LILY_OUTPUT_FILENAME = 'lilypond.ly' # convert_to_lilypond() will save the notes as this
