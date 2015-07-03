'''PRIMEDesigner15MusicForBrython

	Handles PRIME music role

'''

from browser import document, window, alert, console, ajax, timer
import time
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

def allowPlay():
	playButton = document.getElementById("playButton")
	playButton.disabled = False
	
# Plays a song given some sheetMusic
def playSong(state):
	
	index = state["Selected_Music"]
	puzzle = state["Music_Puzzles"][index]
	sheetMusic = puzzle.sheetMusic
	
	
	# Music Settings
	tempo = 1.0
	
	# Apply transformations
	console.log(puzzle.transformList)
	for transform in puzzle.transformList:
		if(transform == "increaseTempo"):
			tempo = tempo - 0.5
		if(transform == "decreaseTempo"):
			tempo = tempo + 0.5
	
	#timeLimit = 10
	song = sheetMusic.split("\n")
	wait = 0
	for note in song:
		values = note.split(" ")
		wait = wait + float(values[0]) * tempo
		pitch = values[1]
		hold = values[2]
		
		
		piano.play({
			'wait' : wait,
			'pitch' : pitch,
			'env' : {'hold' : float(hold)},
			filter : { 'q' : 15 } 
		})
	
	# Trying to get this to work		
	'''if(wait > timeLimit):
	
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
	
