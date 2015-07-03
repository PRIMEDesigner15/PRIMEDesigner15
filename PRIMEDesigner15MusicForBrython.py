'''PRIMEDesigner15MusicForBrython

	Handles PRIME music role

'''

from browser import document, window, alert, console, ajax
import time
from javascript import JSObject, JSConstructor


console.log(globals())

#Wad object used for playing sounds.
Wad = JSConstructor(window.wad)
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

def handlePlayButtonClick(evt):
	index = current_state["Selected_Music"]
	puzzle = current_state["Music_Puzzles"][index]
	playSong(puzzle.sheetMusic)

# Plays a song given some sheetMusic
def playSong(sheetMusic):
	
	song = sheetMusic.split("\n")
	
	for note in song:
		values = note.split(" ")
		console.log(values)
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

# Stops whatever song is currently playing
def stopSong():		
	piano.stop()
