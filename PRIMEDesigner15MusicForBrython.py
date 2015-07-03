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

def handlePlayButtonClick(state):
	def handlePlayButtonClick2(evt):
		
		index = state["Selected_Music"]
		puzzle = state["Music_Puzzles"][index]
		playSong(puzzle.sheetMusic)
		
	return handlePlayButtonClick2
	
# Plays a song given some sheetMusic
def playSong(sheetMusic):
	
	song = sheetMusic.split("\n")
	wait = 0
	for note in song:
		values = note.split(" ")
		wait = wait + float(values[0])
		pitch = values[1]
		hold = values[2]
		
		#console.log(wait + " " + pitch + " " + sustain)
		piano.play({
			'wait' : wait,
			'pitch' : pitch,
			'env' : {'hold' : float(hold)},
			filter : { 'q' : 15 } 
		})
	
	playButton = document.getElementById("playButton")
	if(playButton is not None):
		playButton.disabled = True
		timer = timer.set_timeout(allowPlay,(wait+1) * 1000)


def allowPlay():
	playButton = document.getElementById("playButton")
	playButton.disabled = False
