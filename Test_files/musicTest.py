'''PRIMEDesigner15MusicForBrython

	Handle PRIME music stuff
'''
from javascript import JSObject, JSConstructor
from browser import document, window, alert, console, ajax
import time
from javascript import JSObject, JSConstructor

# Loads in a text file containing notes and seconds in between.
def recieveFile(req):
	if req.status == 200 or req.status == 0:

		# Get the name of the file from the response url
		url = req.responseURL
		name = 'unknown'
		slashIndex = 0
		for i in range(len(url)):
			char = url[i]
			if (char == '/'):
				slashIndex = i
			elif (char == '.'):
				name = url[slashIndex+1:i]
		
		
		console.log(name)
		
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
	req.open('GET',url,True)
	req.send()
	
createSong('testMusic.txt')


