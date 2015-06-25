'''PRIMEDesigner15MusicForBrython

	Handle PRIME music stuff
'''

from browser import document, window, alert, console, ajax
import time
from javascript import JSObject, JSConstructor

# Array of Arrays of Wad.js Oscillators (notes) whos index
# Corresponds the the Music Puzzle Array in the state.
songs = []

# Loads in a text file containing notes and seconds in between.
def recieveFile(req):
	if req.status == 200 or req.status == 0:

		# Get the name of the file from the response url
		url = req.responseURL
		sheetMusic = req.text
		name = 'unknown'
		slashIndex = 0
		for i in range(len(url)):
			char = url[i]
			if (char == '/'):
				slashIndex = i
			elif (char == '.'):
				name = url[slashIndex+1:i]
		
		# Split up the sheet music.
		sheetMusic = [name] + req.text.split(" ")
		console.log(sheetMusic)
		songs.append(sheetMusic)
		
	else:
		console.log("error" + req.text)

def err_msg():
	alert("file couldn't be opened after %s seconds" %timeout)

timeout = 4 

# Creates a series of wad.js oscillators out of the contents of the text file.
def createSong(url):
	
	req = ajax.ajax()
	req.bind("complete",recieveFile)
	req.set_timeout(timeout,err_msg)
	req.open('GET',url,False)
	req.send()
	
#createSong('testMusic.txt')

#Wad object used for playing sounds.
Wad = JSConstructor(window.Wad)
piano = Wad({
    'source' : 'square', 
    'env' : {
        'attack' : .01, 
        'decay' : .005, 
        'sustain' : .2, 
        'hold' : .015, 
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
list = []

#piano.play({ 'pitch' : 'A2' })
piano.play({
	'wait' : 0,
	'pitch' : 'A3', 
	filter : { 'q' : 15 } })
#piano.play({ 'pitch' : 'A4', 'env' : { 'release' : .2 } })