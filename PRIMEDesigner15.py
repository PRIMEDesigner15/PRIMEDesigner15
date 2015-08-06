"""
PRIMEDesigner15.py
A SOLUZION problem formulation
It is important that COMMON_CODE come
before all the other sections (except METADATA), including COMMON_DATA.
"""

# <METADATA>
SOLUZION_VERSION = "0.01"
PROBLEM_NAME = "PRIME Designer 2015"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ["S. Tanimoto", "Dennis Orzikh", "Paul Curry"]
PROBLEM_CREATION_DATE = "13-APL-2015"
PROBLEM_DESC=\
    """This version is mainly for the Brython version of the solving client
    and the Brython version of Python.
    However, it should all be generic Python 3, and this file is intended
    to work a future Python+Tkinter client that runs on the desktop.
    Anything specific to the Brython context should be in the separate
    file MondrianVisForBRYTHON.py, which is imported by this file when
    being used in the Brython SOLUZION client."""
#</METADATA>

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>

BRYTHON = True

if(BRYTHON):
	from PRIMEDesigner15VisForBrython import hide_loading, show_loading, add_puzzle_menu, create_rule_menu
	from templateRoot.PRIMEDesigner15Operator import Operator as Operator
	from templateRoot.PRIMEDesigner15Operator import AsyncOperator as AsyncOperator
	
from browser import document, window, alert, console, ajax
from javascript import JSObject, JSConstructor
import time, json


# Preforms a deep copy of the given state. 
def copy_state(state):
	newState = {"Rooms": [], "Doors": []}
	newRooms = []
	newDoors = []
	newImagePuzzles = []
	newMusicPuzzles = []
	
	
	# Copy the rooms (without doors in their walls) and doors into the newState's dictionary.
	for room in state["Rooms"]:
		newRooms.append(room.copy())
	for door in state["Doors"]:
		newDoors.append(door.copy())
	for imagePuzzle in state["Image_Puzzles"]:
		newImagePuzzles.append(imagePuzzle.copy())
	for musicPuzzle in state["Music_Puzzles"]:
		newMusicPuzzles.append(musicPuzzle.copy())
	
	
	# Put the new lists into the new state's lists.
	newState["Rooms"] = newRooms
	newState["Doors"] = newDoors
	newState["Image_Puzzles"] = newImagePuzzles
	newState["Music_Puzzles"] = newMusicPuzzles
	
	newState["Rules"] = state["Rules"]
	
	# Primitives and operators do not need to be deep copied.
	newState["Selected_Room"] = state["Selected_Room"]	
	newState["Selected_Image"] = state["Selected_Image"]
	newState["Selected_Music"] = state["Selected_Music"]
	newState["Role"] = state["Role"]
	
	# Operators is updated in set_operators.
	newState["Operators"] = state["Operators"]
	
	# Add in doors/puzzles to the walls in the rooms.
	door_index = 0
	for room_num in range(9):
		for direction in ['N', 'S', 'E', 'W']:
			oldWall = state["Rooms"][room_num].walls[direction]
			newWall = newState["Rooms"][room_num].walls[direction]
			if(oldWall.door is not None and newWall.door is None):
				add_door_to_room(room_num, direction, newState, state["Doors"][door_index])
				door_index += 1
			if(oldWall.puzzle is not None):
				image_index = 0
				music_index = 0
				if(type(oldWall.puzzle) is imagePuzzle):
					add_puzzle_to_room(room_num,direction,newState,oldWall.puzzle)
					image_index += 1
				else:
					add_puzzle_to_room(room_num,direction,newState,oldWall.puzzle)
					music_index += 1
					
	return newState
		
def describe_state(state):
	""" Produces a textual description of a state.
    Might not be needed in normal operation with GUIs."""	
	
#Template JSON Stuff	
#try:
#  from browser import window, alert
#  window.SOLUZION_INITIAL_STATE = INITIAL_STATE
#  window.IS_JSON = json_encode(INITIAL_STATE)
  #alert("Inside of the template Mondrian.py, the INITIAL_STATE JSON is "+window.IS_JSON)
  #print(INITIAL_STATE)
#except Exception as e:dsa
#  print("There was an exception when trying to communicate back from Python to Javascript.")
#  print(e)


""" A note on the coordinate system used: 
	Each room is of size 1. The game is thus of width 3 and height 3"""

ROOM_SIZE = 1
	
class Room:	

	""" A room in the game contains 4 walls that could have wallpapers or doors
		and a possible ambient soundtrack, and a possible puzzle. """
	def __init__(self, x1, y1, x2, y2):
		
		# Coordinates for display of the room.
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		
		# 4 walls. 
		self.walls = {}
		# Horizontal walls.
		self.walls['N'] = Wall(x1 ,y1 ,x2 ,y1, 'N') #top 
		self.walls['S'] = Wall(x1 ,y2 ,x2 ,y2, 'S') #bottom
			
		# Vertical walls.
		self.walls['W'] = Wall(x1 ,y1 ,x1 ,y2, 'W') #left
		self.walls['E'] = Wall(x2 ,y1 ,x2 ,y2, 'E') #right
	
		# Possible ambient soundtrack.
		self.music = None
		
	def copy(self):
		newRoom = Room(self.x1, self.y1, self.x2, self.y2)
		for direction in ['N','S','W','E']:
			newRoom.walls[direction] = self.walls[direction].copy()
		if(self.music is None):
			newRoom.music = None
		else:
			newRoom.music = self.music.copy()
		
		return newRoom
		
""" A wall could contain a door and a wallpaper """	
class Wall:

	def __init__(self, x1, y1, x2, y2, loc): 
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.loc = loc
		
		self.door = None
		
		# Possible puzzle
		self.puzzle = None
		
		# Creates a wallpaper, default picture is wall.jpg
		self.wallpaper = Wallpaper()
		
	# Returns a copy of itself. Does not copy its door.
	def copy(self):
		newWall = Wall(self.x1,self.y1,self.x2,self.y2,self.loc)
		if(newWall.puzzle is None):
			newWall.puzzle = None
		else: 
			newWall.puzzle =  puzzle.copy()
		
		newWall.wallpaper = self.wallpaper.copy()
		return newWall
		
# Default url is wall.jpg
# Test url is stripes.jpg for transformation testing.
class Wallpaper:
	
	def __init__(self, url = "images/wall.jpg"):
		self.url = url
	
	# Returns a copy of itself.
	def copy(self):
		return Wallpaper(self.url)

class Door:
	
	def __init__(self, isOpen = False, url="images/door.jpg"):
		self.isOpen = isOpen
		self.url = url
		
	# Closes the door if it is open.
	# Opens the door if it is closed.
	def open_or_close(self):
		self.isOpen = not isOpen
	
	# Returns a deep copy of itself.
	def copy(self):
		return Door(self.isOpen, self.url)

class ImagePuzzle:

	def __init__(self, name = "defaultImageName", url = "images/metalfencing.jpg", transformList = []):
		
		self.name = name
		self.url = url
		
		# shallow copying a new list
		self.transformList = transformList[:]
	
	def add_transform(self, transform):
		self.transformList.append(transform)
	
	def copy(self):
		return ImagePuzzle(self.name,self.url, self.transformList)
		
class MusicPuzzle:

	def __init__(self, name = "defaultMusicName", notes = [], transformList = []):
		
		self.name = name
		
		# shallow copying a new list
		self.notes = notes[:]
		
		# shallow copying a new list
		self.transformList = transformList[:]
		
	def add_transform(self, transform):
		self.transformList.append(transform)
	
	def copy(self):
		# Deep copy note list
		noteCopy = []
		for note in self.notes:
			noteCopy.append(note)
		return MusicPuzzle(self.name, noteCopy, self.transformList)
	
class Rule:
	def __init__(self, name = "defaultName", causeCondition, effectCondition, isActive):
		
		self.name = name
		
		self.causeCondition = causeCondition
		
		self.effectCondition = effectCondition
		
		self.isActive = isActive
'''
If solve puzzle then open/close door
If enter room then open/close door
If solve puzzle then message
If enter room then message

'''		

# Takes a room num from 0 to 8 and a side for the door to be on, [N, S, E, W]
# Optional newDoor parameter which allows you to pass which door the walls will point to.
# Is default set to the creation of a new door.
def add_door_to_room(room_num, side, state, newDoor = None):
	ROOMS = state["Rooms"]
	DOORS = state["Doors"]
	
	if(newDoor is None):
		newDoor = Door()
		DOORS.append(newDoor)
	
	ROOMS[room_num].walls[side].door = newDoor
	if side == 'N':
		ROOMS[room_num - 3].walls['S'].door = newDoor
	elif side == 'S':
		ROOMS[room_num + 3].walls['N'].door = newDoor
	elif side == 'E':
		ROOMS[room_num + 1].walls['W'].door = newDoor
	elif side == 'W':
		ROOMS[room_num - 1].walls['E'].door = newDoor
	else:
		alert("Error: Invalid direction passed to add_door")
		DOORS.pop()

	print(DOORS)

# Operator version of add door that returns new state
def add_door_operator(state, room_num, side):
	
	newState = copy_state(state)
	add_door_to_room(room_num, side, newState)
	
	return newState

# Removes the reference to a door from the a wall shared 
# by two rooms.
def remove_door_from_room(room_num, side, state):
	
	ROOMS = state["Rooms"]
	DOORS = state["Doors"]
	ROOMS[room_num].walls[side].door = None
	if side == 'N':
		ROOMS[room_num - 3].walls['S'].door = None
	elif side == 'S':
		ROOMS[room_num + 3].walls['N'].door = None
	elif side == 'E':
		ROOMS[room_num + 1].walls['W'].door = None
	elif side == 'W':
		ROOMS[room_num - 1].walls['E'].door = None
	else:
		alert("Error: Invalid direction passed to add_door")

	# Remove a doors from the list so there are two fewer doors
	DOORS.pop()

# Operator version of remove door that returns new state
def remove_door_operator(state, room_num, side):

	newState = copy_state(state)
	remove_door_from_room(room_num,side,newState)
	return newState
	
# Checks if a door can be placed on a wall, meaning a door cannot already be on a wall
# and a puzzle cannot be on the wall or on the other side of the wall.
def add_doors_is_valid(state, side):
	
	# Reduce magic constants.
	
	ROOMS = state["Rooms"]
	DOORS = state["Doors"]
	room_num = state["Selected_Room"]
	
	if side == 'N':
		north_room = room_num - 3
		if (north_room < 0):
			return False
		elif (ROOMS[room_num].walls['N'].door is not None 
				or ROOMS[room_num].walls['N'].puzzle is not None
				or ROOMS[north_room].walls['S'].puzzle is not None):
			return False
		else:
			return True
	elif side == 'S':
		south_room = room_num + 3
		if (south_room > 8):
			return False
		elif (ROOMS[room_num].walls['S'].door is not None 
				or ROOMS[room_num].walls['S'].puzzle is not None
				or ROOMS[south_room].walls['N'].puzzle is not None):
			return False
		else:
			return True
	elif side == 'E':
		east_room = room_num + 1
		if (room_num + 1) % 3 is 0:
			return False
		elif (ROOMS[room_num].walls['E'].door is not None 
				or ROOMS[room_num].walls['E'].puzzle is not None
				or ROOMS[east_room].walls['W'].puzzle is not None): 	
			return False
		else:
			return True
	elif side == 'W':
		west_room = room_num - 1
		if (room_num + 1) % 3 is 1:
			return False
		elif (ROOMS[room_num].walls['W'].door is not None 
				or ROOMS[room_num].walls['W'].puzzle is not None
				or ROOMS[west_room].walls['E'].puzzle is not None):	
			return False
		else: 
			return True
	else:
		return False

# Return true if a door can be removed and false if it cant
def remove_doors_is_valid(state,side):
	
	ROOMS = state["Rooms"]
	DOORS = state["Doors"]
	room_num = state["Selected_Room"]

	door = ROOMS[room_num].walls[side].door
	return door is not None
	
# Adds the passed puzzle to the correct room and side of the 
# passed state
def add_puzzle_to_room(state,room_num,side,puzzle):
	state["Rooms"]["room_num"].walls["side"].puzzle = puzzle
	if(type(puzzle) is imagePuzzle):
		state["Image_puzzles"].append(puzzle)
	else:
		state["Music_puzzles"].append(puzzle)
	
# room_num, side parameters don't do anything..?
def add_puzzle_operator(state, sendBack):
	def processMenu(state,cardinal,puzzle):
		print(cardinal)
		print(puzzle)
		#sendBack from here
	add_puzzle_menu(state, processMenu)

# returns a list of cardinals representing 
# sides of a room that can not be used to place a puzzle
def puzzles_is_valid(state):
	invalidCardinals = []
	room_num = state["Selected_Room"]
	selectedRoom = state["Rooms"][room_num]
	
	if(selectedRoom.walls['N'].puzzle is not None or selectedRoom.walls['N'].door is not None):
		invalidCardinals.append('N')
	if(selectedRoom.walls['E'].puzzle is not None or selectedRoom.walls['E'].door is not None):
		invalidCardinals.append('E')
	if(selectedRoom.walls['S'].puzzle is not None or selectedRoom.walls['S'].door is not None):
		invalidCardinals.append('S')
	if(selectedRoom.walls['W'].puzzle is not None or selectedRoom.walls['W'].door is not None):
		invalidCardinals.append('W')	

	return invalidCardinals


def create_rule_operator(state, sendBack):
	def processMenu(state, cause, effect):
		print(cause)
		print(effect)
		#sendBack from here
	console.log("inside create_rule")	
	create_rule_menu(state, processMenu)
		
#def add_music_puzzle_to_room(state, room_num):
		
# takes a room num from 0 to 8 and prompts the user for a url for the wallpaper
def add_wallpaper_to_room(state, sendBack, room_num):
	
	# Prompt the user for wallpaper url 
	url = window.prompt("Enter a complete URL for a wallpaper. Say 'cancel' to cancel.", "images/wall.jpg")
	if(url_is_valid(url)):	
	
		# Copy state
		newState = copy_state(state)
		
		ROOMS = newState["Rooms"]
		picked = ROOMS[room_num]
		
		for loc in picked.walls:
			picked.walls[loc].wallpaper.url = url
		
		sendBack(newState)
	
	elif(url != "cancel"):
		alert("URL was not valid")
		
		# Recurse
		add_wallpaper_to_room(state,sendBack,room_num)
	else: #url == "cancel"
		sendBack()
	
def url_is_valid(url):	
	# Note: Only works with Brython Implemented
	# if not, only returns true
	try:
		fileContents = open(url)
		return True
	except OSError:
		return False
	else:
		return False

# Changes which room the user selects. Then calls the callback function, passing it the new state.
def change_room_selection(state, room_num):
	newState = copy_state(state)
	newState["Selected_Room"] = room_num
	return newState
	
def change_image_puzzle_selection(state, puzzle_num):
	newState = copy_state(state)
	newState["Selected_Image"] = puzzle_num
	return newState

def change_music_puzzle_selection(state, puzzle_num):
	newState = copy_state(state)
	newState["Selected_Music"] = puzzle_num
	return newState
	
def change_role(state, role):
	global OPERATORS
	newState = copy_state(state)
	newState['Role'] = role
	
	# reset the operators
	newState['Operators'] = set_operators(newState)
	
	return newState

def create_image_puzzle(state):

	# Prompt the user for a image url
	url = window.prompt("Enter a complete URL for a picture. Say 'cancel' to cancel.", "images/force.jpg")

	if(url_is_valid(url)):
	
		newState = copy_state(state)
		name = getName(url)
		newPuzzle = ImagePuzzle(name,url)
		newState["Image_Puzzles"].append(newPuzzle)
		newState["Selected_Image"] = len(newState["Image_Puzzles"]) - 1
		
		return newState
		
	elif(url != "cancel"):
	
		alert("URL was not valid. Try again.")
		# Recurse
		create_image_puzzle(state)
		
	else: #url == "cancel"
		return state
	
# gets a name out of a url
def getName(url):
	
	# Get name out of the url
	name = ""
	i = 0
	foundDot = False
	while foundDot == False:
		char = url[i]
		if(char == "/"):
			name = ""
		elif(char == "."):
			foundDot = True
		else:
			name = name + char
		i = i + 1
	
	return name
		
def create_music_puzzle(state, sendBack):
	url = window.prompt("Enter a complete URL for a sheetMusic file. Say 'cancel' to cancel.", "music/twinkleTwinkle.txt")
	if(url_is_valid(url)):
		show_loading()
		# When the request is recieved
		def requestSuccess(req):
			if(req.status == 200 or req.status == 0):
				newState = copy_state(state)
				# Assign name of song from json object
				song = json.loads(req.responseText)
				newPuzzle = MusicPuzzle(song["name"],song["notes"])
		
				newState["Music_Puzzles"].append(newPuzzle)
				newState["Selected_Music"] = len(newState["Music_Puzzles"]) - 1
				hide_loading()
				sendBack(newState)
			else:
				print("request failure")
		
		request = ajax.ajax()
		request.open('GET',url,True)
		request.bind("complete",requestSuccess)
		request.send()
	
	elif(url != "cancel"):
		alert("URL was not valid. Try again.")
		create_music_puzzle(state, sendBack)
	else:
		sendBack()

def addImageTransformation(state, transformation):
	newState = copy_state(state)
	
	# Add transform to newState list
	newState["Image_Puzzles"][newState["Selected_Image"]].add_transform(transformation)

	return newState
	
def addMusicTransformation(state, transformation):
	newState = copy_state(state)
	
	# Add transform to newState list
	newState["Music_Puzzles"][newState["Selected_Music"]].add_transform(transformation)
	return newState
	

	
#</COMMON_CODE>		

#<OPERATORS>
# Method that can be called to set the Operators 
# of the current Role given the current State.
# Each operators state transfer must have a callback function defined.
def set_operators(state):

	# Sendback is the function given by the client which receives the modified state
	sb = None
	
	role_operators =\
		[Operator("Change Role to " + role + ".",
			lambda state, r = role: state['Role'] is not r,
			lambda state, r = role: change_role(state, r))
		for role in ["Architect", "Image Puzzle", "Music Puzzle", "Rules"]] 
	if (state['Role'] == "Architect"):
		selection_operators =\
			[Operator("Switch to room numbered " + str(num + 1) + " for editing.",
				lambda state, n = num: n is not state["Selected_Room"],
				lambda state, n = num: change_room_selection(state, n))
			for num in range(9)]

		add_door_operators =\
			[Operator("Add door to current room on " + cardinal + " wall.",
				lambda state, c = cardinal: add_doors_is_valid(state, c),
				lambda state, c = cardinal: add_door_operator(state, state["Selected_Room"], c))
			for cardinal in ['N', 'S', 'E', 'W']]
			
		remove_door_operators =\
			[Operator("Remove door from current room on " + cardinal + " wall.",
				lambda state, c = cardinal: remove_doors_is_valid(state, c),
				lambda state, c = cardinal: remove_door_operator(state, state["Selected_Room"], c))
			for cardinal in ['N', 'S', 'E', 'W']]
			
		wallpaper_operators =\
			AsyncOperator("Add wallpaper to current room.",
				lambda state: True,
				lambda state, sb: add_wallpaper_to_room(state, sb, state["Selected_Room"]))
				
		add_puzzle_operators =\
			AsyncOperator("Add a puzzle to current room",
				lambda state: True,
				lambda state, sb: add_puzzle_operator(state, sb))
				
		OPERATORS = selection_operators	+ add_door_operators + remove_door_operators + wallpaper_operators + add_puzzle_operators +  role_operators
		
	elif(state['Role'] == "Image Puzzle"):
		
		numOfPuzzles = len(state["Image_Puzzles"])
			
		selection_operators =\
			[Operator("Switch to puzzle " + str(num + 1) + ", \"" + state["Image_Puzzles"][num].name + ",\" for editing",
				lambda state, n = num: n < len(state["Image_Puzzles"]) and len(state["Image_Puzzles"]) > 1 and n != state["Selected_Image"],
				lambda state, n = num: change_image_puzzle_selection(state, n))
			for num in range(numOfPuzzles)]
		
		create_new_puzzle =\
			Operator("Create a new image puzzle.",
				lambda state: True,
				lambda state: create_image_puzzle(state))
		horiz_flip =\
			Operator("Flip the image horizontally.",
				lambda state: state["Selected_Image"] > -1,
				lambda state, sb: addImageTransformation(state, "horizFlip"))
		vert_flip =\
			Operator("Flip the image vertically.",
				lambda state: state["Selected_Image"] > -1,
				lambda state, sb: addImageTransformation(state, "vertFlip"))
		shuff_rows =\
			Operator("Shuffle the rows of the image.",
				lambda state: state["Selected_Image"] > -1,
				lambda state, sb: addImageTransformation(state, "shuffleRows"))
		invs_shuff_rows =\
			Operator("Invert Row shuffling",
				lambda state: state["Selected_Image"] > -1,
				lambda state, sb: addImageTransformation(state, "shuffleRowsInverse"))
		shuff_cols =\
			Operator("Shuffle the columns of the image.",
				lambda state: state["Selected_Image"] > -1,
				lambda state, sb: addImageTransformation(state, "shuffleColumns"))
				
		OPERATORS = selection_operators + role_operators + create_new_puzzle + horiz_flip + vert_flip + shuff_rows + invs_shuff_rows + shuff_cols
		
	elif(state['Role'] == "Music Puzzle"):
		
		numOfPuzzles = len(state["Music_Puzzles"])
		
		selection_operators =\
			[Operator("Switch to puzzle " + str(num + 1) + ", \"" + state["Music_Puzzles"][num].name + "\" for editing.",
				lambda state, n = num: n < len(state["Music_Puzzles"]) and len(state["Music_Puzzles"]) > 1 and n != state["Selected_Music"],
				lambda state, n = num: change_music_puzzle_selection(state, n))
			for num in range(numOfPuzzles)]
		
		create_new_puzzle =\
			AsyncOperator("Create a new music puzzle.",
				lambda state: True,
				lambda state, sb: create_music_puzzle(state, sb))
		
		increase_pitch =\
			Operator("Increase pitch of song",
				lambda state: state["Selected_Music"] > -1,
				lambda state, sb: addMusicTransformation(state, "increasePitch"))
		
		decrease_pitch =\
			Operator("Decrease pitch of song",
				lambda state: state["Selected_Music"] > -1,
				lambda state, sb: addMusicTransformation(state, "decreasePitch"))
		
		increase_tempo =\
			Operator("Increase tempo of song",
				lambda state: state["Selected_Music"] > -1,
				lambda state, sb: addMusicTransformation(state, "increaseTempo"))
		
		decrease_tempo =\
			Operator("Decrease tempo of song",
				lambda state: state["Selected_Music"] > -1,
				lambda state, sb: addMusicTransformation(state, "decreaseTempo"))

		shuffle_notes =\
			Operator("Shuffle notes of song",
				lambda state: state["Selected_Music"] > -1,
				lambda state, sb: addMusicTransformation(state, "shuffleNotes"))

		reverse_notes =\
			Operator("Reverse notes of song",
				lambda state: state["Selected_Music"] > -1,
				lambda state, sb: addMusicTransformation(state, "reverseNotes"))
		
		OPERATORS = selection_operators + role_operators  + create_new_puzzle + increase_tempo + decrease_tempo + shuffle_notes + increase_pitch + decrease_pitch + reverse_notes        
	
	elif(state['Role'] == "Rules"):
		create_rule =\
			AsyncOperator("Create new Rule.",
				lambda state: True,
				lambda state: create_rule_operator(state))
				
		OPERATORS = role_operators + create_rule
	else:
		alert("unsupported role")
	
	return OPERATORS

#</OPERATORS>
	
#<INITIAL_STATE> The game is a list of 9 rooms stored a list.
INITIAL_STATE = {}
INITIAL_STATE['Rooms'] = []
INITIAL_STATE['Doors'] = []
INITIAL_STATE['Image_Puzzles'] = []
INITIAL_STATE['Music_Puzzles'] = []

'''
# ADD A BLANK MUSIC PUZZLE FOR DEBUG PURPOSES ONLY
INITIAL_STATE["Music_Puzzles"].append(MusicPuzzle())
INITIAL_STATE["Music_Puzzles"].append(MusicPuzzle())
INITIAL_STATE["Music_Puzzles"].append(MusicPuzzle())
INITIAL_STATE["Music_Puzzles"].append(MusicPuzzle())

# ADD A BLANK IMAGE PUZZLE FOR DEBUG PURPOSES ONLY
INITIAL_STATE["Image_Puzzles"].append(ImagePuzzle())'''

INITIAL_STATE['Rules'] = []
#INITIAL_STATE['Causes'] = []
#INITIAL_STATE['Effects'] = []
INITIAL_STATE['Selected_Room'] = 0
INITIAL_STATE['Selected_Image'] = -1
INITIAL_STATE['Selected_Music'] = -1
INITIAL_STATE['Role'] = "Architect"
INITIAL_STATE['Operators'] = set_operators(INITIAL_STATE)	


# Create 9 rooms, add them to the the state.
for j in range(3):
	for i in range(3):
		INITIAL_STATE['Rooms'].append( Room(i, j, i + 1, j + 1) )	
# Now initialize operators.
OPERATORS = INITIAL_STATE['Operators']
#</INITIAL_STATE>




