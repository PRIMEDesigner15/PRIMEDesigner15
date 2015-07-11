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

#def addBlankNote(notes):
#	note = new

class Note:
	
	def __init__(self,wait = 1, pitch = "A4", hold = "0"):
		self.wait = wait
		self.pitch = pitch
		self.hold = hold

# Debug tool
def printNotes(notes2):
	for chord in notes2:
		print(chord)

def allowPlay():
	playButton = document.getElementById("playButton")
	playButton.disabled = False
	
# Plays a song given some sheetMusic in JSON format
def playSong(state):
	
	index = state["Selected_Music"]
	puzzle = state["Music_Puzzles"][index]
	sheetMusic = puzzle.sheetMusic
	
	song = json.loads(sheetMusic)
	
	# Music Settings
	tempo = 1.0
	
	notes = song["notes"]
	
	# Secondary list of notes for permutation based transformations.
	notes2 = []
	
	# Apply transformations
	for transform in puzzle.transformList:
		if(transform == "increaseTempo"):
			tempo = tempo - 0.5
		if(transform == "decreaseTempo"):
			tempo = tempo + 0.5
		if(transform == "shuffleNotes"):
			
			# Group the notes into chords so shuffling doesn't break up chords
			i = 0
			n = len(notes2)
		
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
			
			#printNotes(notes2)
			print("len(notes2) = ")
			print(len(notes2))
			
			print("n = ") 
			print(n)
			
			printNotes(notes2)
			
			# Shuffle chords/notes of notes2
			temp = []
			#if(n%2==0):
			#	notes2.append([])
			#	alert("appending")
			for j in range(n-1):
				temp.append(notes2[(2*j)%(n-1)])
			print("-----------------------------")
			printNotes(temp)
			
			print("len(temp) = ")
			print(len(temp))
			
			# Clear notes
			notes = []
			notes2 = []
			
			# Read notes2 back into original notes array
			for chord in temp:
				for note in chord:
					notes.append(note)
			
		else:
			printNotes(notes)
	# Play transformed notes
	wait = 0
	for note in notes:
		wait = note["wait"] * tempo + wait 
		pitch = note["pitch"]
		hold = float(note["hold"]) 

		piano.play({
			'wait' : wait,
			'pitch' : pitch,
			'env' : {'hold' : hold},
			filter : { 'q' : 15 } 
		})
	'''
	# Trying to get this to work		
	if(wait > timeLimit):
	
		alert("Song cannot be more than " + str(timeLimit) + " seconds long.")
		if(playButton is not None):
			playButton.disabled = True
			timer = timer.set_timeout(allowPlay,(timeLimit) * 1000)
	else: 
		if(playButton is not None):
			playButton.disabled = True
			timer = timer.set_timeout(allowPlay,(wait+1) * 1000)
	'''
	
def handlePlayButtonClick(state):
	def handlePlayButtonClick2(evt):
		
		playSong(state)
		
	return handlePlayButtonClick2
	
