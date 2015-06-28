'''PRIMEDesigner15MusicForBrython

	Handle PRIME music stuff


from browser import document, window, alert, console, ajax
import time
from javascript import JSObject, JSConstructor

# Array of time between notes followed by notes
songs = []

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

def note(pitch, wait, hold):
	this.pitch = pitch
	this.wait = wait
	this. hold = hold

# Loads in a text file containing notes and seconds in between.
def recieveFile(req):
	if req.status == 200 or req.status == 0:

		# Get the name of the file from the response url
		url = req.responseURL
		sheetMusic = req.text
		console.log(sheetMusic)
		name = 'unknown'
		slashIndex = 0
		for i in range(len(url)):
			char = url[i]
			if (char == '/'):
				slashIndex = i
			elif (char == '.'):
				name = url[slashIndex+1:i]
		
		# Split up the sheet music.
		sheetMusic = [name] + req.text.split("\n")
		return sheetMusic
		
	else:
		console.log("error" + req.text)

def err_msg():
	alert("file couldn't be opened after %s seconds" %timeout)

timeout = 4 

# Creates a series of wad.js oscillators out of the contents of the text file.
def createSheetMusic(url):
	
	req = ajax.ajax()
	req.bind("complete",recieveFile)
	req.set_timeout(timeout,err_msg)
	req.open('GET',url,True)
	req.send()
	
#createSong('testMusic.txt')

def playSong(music_num):
	console.log(songs[music_num])
	sheetMusic = songs[music_num]
	wait = 0
	
	# The first "note" is the name of the song
	console.log("playing song: " + sheetMusic[0])
	
	# Thus skip the first note when playing the song
	song = iter(sheetMusic)
	next(song)
	
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

#piano.play({ 'pitch' : 'A2' })
#piano.play({ 'pitch' : 'A4', 'env' : { 'release' : .2 } })
'''