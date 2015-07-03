'''PRIMEDesigner15MusicForBrython
	Handle PRIME music stuff
'''

from browser import document, window, alert, console, ajax
import time
from javascript import JSObject, JSConstructor

class Saying:
	def __init__(self, text):
		self.text = text

Sayings = []
recieve = False
def get():
	saying = Saying("not modified")
	def requestSuccess(saying):
		def processSuccess(req):
			pass
			#saying.text = req.responseText
			#print(req.readyState)
		return processSuccess
		
	def loadingFunction(req):
		time.sleep(10)
		
	req = ajax.ajax()
	req.bind("loading",loadingFunction)
	req.bind("complete",requestSuccess(saying, requestSuccess(saying)))
	#req.set_timeout(timeout,requestFailure)
	req.open('GET',"testMusic.txt",True)
	#console.log(req.readyState)
	req.send()
	return saying
	
#console.log(get().text)
#def sayingHasChanged(saying):
#	Sayings.append(saying)

#def getSaying():
#	get()
#	saying = Sayings[0]
#	Sayings[:] = []
#	return saying

saying = get()
console.log(saying)
#saying = getSaying()
#console.log(saying)


































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
		songs.append(sheetMusic)
		
	else:
		console.log("error" + req.text)

def err_msg():
	alert("file couldn't be opened after %s seconds" %timeout)

timeout = 4 

def mySuccess(param1, param2):
	alert("hello")
	def regularSuccess(rec):
		console.log(rec.text)
		console.log(param1)
		console.log(param2)
		
	return regularSuccess	

# Creates a series of wad.js oscillators out of the contents of the text file.
def requestFile(url):
	
	req = ajax.ajax()
	req.bind("complete",mySuccess("hello","goodbye"))
	req.set_timeout(timeout,err_msg)
	req.open('GET',url,True)
	req.send()
	

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
