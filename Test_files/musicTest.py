'''PRIMEDesigner15MusicForBrythonTest

	Handle PRIME music stuff
'''
from browser import document, window, alert, console, ajax
import time
from javascript import JSObject, JSConstructor

# Creates a series of wad.js oscillators out of the contents of the text file.
def createSong(req):
	alert("hello?")
	if req.status == 200 or req.status == 0:
		console.log(req.text)
	else:
		console.log("error" + req.text)

def err_msg():
	alert("server didn't reply after %s seconds" %timeout)

timeout = 4 

# Loads in a text file containing notes and seconds in between.
def loadMusicFile(url):
	
	req = ajax.ajax()
	req.bind("complete",createSong)
	req.set_timeout(timeout,err_msg)
	req.open('GET',url,True)
	req.send()


string = 'testMusic.txt?foo=%s'
loadMusicFile('testMusic.txt')



