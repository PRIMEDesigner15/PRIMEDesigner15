'''PRIMEDesigner15MusicForBrython

	Handles PRIME music role

'''

from browser import document, window, alert, console, ajax, timer
import time, json
from javascript import JSObject, JSConstructor

#Wad object used for playing sounds.
Wad = JSConstructor(window.Wad)
piano = Wad({
    'source' : 'square', 
    'env' : {
        'attack' : .01, 
        'decay' : .005, 
        'sustain' : .2, 
        'hold' : 0.15, 
        'release' : .3
    }, 
    filter : {
        'type' : 'lowpass', 
        'frequency' : 1200, 
        'q' : 8.5, 
        'env' : {
            'attack' : .2, 
            'frequency' : 600
        }
    }
})

# This object is a mapping of note names to frequencies. 
Pitches = {
	'A0'  : 27.5000,
	'A#0' : 29.1352,
	'Bb0' : 29.1352,
	'B0'  : 30.8677,
	'C1'  : 32.7032,
	'C#1' : 34.6478,
	'Db1' : 34.6478,
	'D1'  : 36.7081,
	'D#1' : 38.8909,
	'Eb1' : 38.8909,
	'E1'  : 41.2034,
	'F1'  : 43.6535,
	'F#1' : 46.2493,
	'Gb1' : 46.2493,
	'G1'  : 48.9994,
	'G#1' : 51.9131,
	'Ab1' : 51.9131,
	'A1'  : 55.0000,
	'A#1' : 58.2705,
	'Bb1' : 58.2705,
	'B1'  : 61.7354,
	'C2'  : 65.4064,
	'C#2' : 69.2957,
	'Db2' : 69.2957,
	'D2'  : 73.4162,
	'D#2' : 77.7817,
	'Eb2' : 77.7817,
	'E2'  : 82.4069,
	'F2'  : 87.3071,
	'F#2' : 92.4986,
	'Gb2' : 92.4986,
	'G2'  : 97.9989,
	'G#2' : 103.826,
	'Ab2' : 103.826,
	'A2'  : 110.000,
	'A#2' : 116.541,
	'Bb2' : 116.541,
	'B2'  : 123.471,
	'C3'  : 130.813,
	'C#3' : 138.591,
	'Db3' : 138.591,
	'D3'  : 146.832,
	'D#3' : 155.563,
	'Eb3' : 155.563,
	'E3'  : 164.814,
	'F3'  : 174.614,
	'F#3' : 184.997,
	'Gb3' : 184.997,
	'G3'  : 195.998,
	'G#3' : 207.652,
	'Ab3' : 207.652,
	'A3'  : 220.000,
	'A#3' : 233.082,
	'Bb3' : 233.082,
	'B3'  : 246.942,
	'C4'  : 261.626,
	'C#4' : 277.183,
	'Db4' : 277.183,
	'D4'  : 293.665,
	'D#4' : 311.127,
	'Eb4' : 311.127,
	'E4'  : 329.628,
	'F4'  : 349.228,
	'F#4' : 369.994,
	'Gb4' : 369.994,
	'G4'  : 391.995,
	'G#4' : 415.305,
	'Ab4' : 415.305,
	'A4'  : 440.000,
	'A#4' : 466.164,
	'Bb4' : 466.164,
	'B4'  : 493.883,
	'C5'  : 523.251,
	'C#5' : 554.365,
	'Db5' : 554.365,
	'D5'  : 587.330,
	'D#5' : 622.254,
	'Eb5' : 622.254,
	'E5'  : 659.255,
	'F5'  : 698.456,
	'F#5' : 739.989,
	'Gb5' : 739.989,
	'G5'  : 783.991,
	'G#5' : 830.609,
	'Ab5' : 830.609,
	'A5'  : 880.000,
	'A#5' : 932.328,
	'Bb5' : 932.328,
	'B5'  : 987.767,
	'C6'  : 1046.50,
	'C#6' : 1108.73,
	'Db6' : 1108.73,
	'D6'  : 1174.66,
	'D#6' : 1244.51,
	'Eb6' : 1244.51,
	'E6'  : 1318.51,
	'F6'  : 1396.91,
	'F#6' : 1479.98,
	'Gb6' : 1479.98,
	'G6'  : 1567.98,
	'G#6' : 1661.22,
	'Ab6' : 1661.22,
	'A6'  : 1760.00,
	'A#6' : 1864.66,
	'Bb6' : 1864.66,
	'B6'  : 1975.53,
	'C7'  : 2093.00,
	'C#7' : 2217.46,
	'Db7' : 2217.46,
	'D7'  : 2349.32,
	'D#7' : 2489.02,
	'Eb7' : 2489.02,
	'E7'  : 2637.02,
	'F7'  : 2793.83,
	'F#7' : 2959.96,
	'Gb7' : 2959.96,
	'G7'  : 3135.96,
	'G#7' : 3322.44,
	'Ab7' : 3322.44,
	'A7'  : 3520.00,
	'A#7' : 3729.31,
	'Bb7' : 3729.31,
	'B7'  : 3951.07,
	'C8'  : 4186.01
}

'''
class Note:
	
	def __init__(self,wait = 1, pitch = "A4", hold = "0"):
		self.wait = wait
		self.pitch = pitch
		self.hold = hold

'''

# Debug tool
def printNotes(notes2):
	for chord in notes2:
		print(chord)

# Enables the play song button
def allowPlay():
	playButton = document.getElementById("playButton")
	playButton.disabled = False

# Groups the list of notes into chords	
def groupIntoChords(notes):
	notes2 = []
	i = 0
	n = 0
		
	# Edge case
	notes2.append([])
	notes2[0].append(notes[0])
	n = n + 1
			
	iternotes = iter(notes)
	next(iternotes)
			
	for note in iternotes:
		if(i >= n-1):
			notes2.append([])
			n = n + 1
		if(note["wait"] != 0):
			i = i + 1
			
		notes2[i].append(note)
			
	return notes2
	
# Reads a chord-organized list of notes and returns a normal list of notes
def readChords(notes):

	notes2 = []
	
	# Read temp back into original notes array
	for chord in notes:
		for note in chord:
			notes2.append(note)
	
	return notes2
	
# Plays a song given some sheetMusic in JSON format
def playSong(state):
	
	global Pitches
	
	index = state["Selected_Music"]
	puzzle = state["Music_Puzzles"][index]
	
	# Music Settings
	tempo = 1.0
	pitchChange = 0.0
	
	notes = puzzle.notes
	
	# Secondary list of notes for permutation based transformations.
	notes2 = []
	
	# Apply transformations
	for transform in puzzle.transformList:
	
		if(transform == "increasePitch"):
			pitchChange = pitchChange + 10.0
			
		if(transform == "decreasePitch"):
			pitchChange = pitchChange - 10.0
			
		if(transform == "increaseTempo"):
			tempo = tempo - 0.5
			
		if(transform == "decreaseTempo"):
			tempo = tempo + 0.5
			
		if(transform == "shuffleNotes"):
			
			# Temp storage array
			notes2 = []
			
			# Group the notes into chords so shuffling doesn't break up chords
			notes = groupIntoChords(notes)
			n = len(notes)
			
			# Shuffle chords/notes of notes2
			# Pad to next odd number for invertibility
			if(n%2==0):
				notes.append([])
				n = n + 1
			for j in range(n):
				notes2.append(notes[(2*j)%(n)])
			
			# Read temp back into original notes array
			notes = readChords(notes2)	
			
		if(transform == "reverseNotes"):
		
			# Temp storage array
			notes2 = []
			
			notes = groupIntoChords(notes)
			n = len(notes) - 1
			
			for i in range(n,-1,-1):
				notes2.append(notes[i])
			
			# Read notes2 back into original notes
			notes = readChords(notes2)

	
	# Play transformed notes
	wait = 0
	for note in notes:
		wait = note["wait"] * tempo + wait 
		pitch = Pitches[note["pitch"]] + pitchChange
		hold = float(note["hold"]) 

		piano.play({
			'wait' : wait,
			'pitch' : pitch,
			'env' : {'hold' : hold},
			filter : { 'q' : 15 } 
		})
	
	
	timeLimit = 10
	playButton = document.getElementById("playButton")
	
	# Trying to get this to work		
	if(wait > timeLimit):
		alert("Song cannot be more than " + str(timeLimit) + " seconds long.")
		if(playButton is not None):
			playButton.disabled = True
			buttonDisabled = timer.set_timeout(allowPlay,(timeLimit) * 1000)
	else: 
		if(playButton is not None):
			playButton.disabled = True
			buttonDisabled = timer.set_timeout(allowPlay, int(wait+1) * 1000)
	
	
def handlePlayButtonClick(state):
	def handlePlayButtonClick2(evt):
		
		playSong(state)
		
	return handlePlayButtonClick2
	
