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
	from PRIMEDesigner15VisForBrython import hide_loading, show_loading, add_puzzle_menu, add_condition_menu, add_action_menu
	from PRIMEDesigner15MusicForBrython import playAmbientMusic, stopAmbientMusic
	from templateRoot.PRIMEDesigner15Operator import Operator as Operator
	from templateRoot.PRIMEDesigner15Operator import AsyncOperator as AsyncOperator
	
from browser import document, window, alert, console, ajax
from javascript import JSObject, JSConstructor
import time, json

# Debug string
def dAlert(string):
	alert(string)

# Preforms a deep copy of the given state. 
def copy_state(state):

	oldRooms = state["Rooms"]
	oldRules = state["Rules"]
	oldImgPuzzles = state["Image_Puzzles"]
	oldMusPuzzles = state["Music_Puzzles"]
	
	newState = {}
	newRooms = []
	newRules = []
	newImagePuzzles = {}
	newMusicPuzzles = {}

	'''
	#Debug
	print("image puzzles")
	string = ""
	for puzzle in state["Image_Puzzles"]:
		string += puzzle.name + " ,"
	print(string)
	string = ""
	print("music puzzles")
	for puzzle in state["Music_Puzzles"]:
		string += puzzle.name + " ,"
	print(string)
	'''
	
	# Copy the rooms (without doors in their walls) and doors into the newState's dictionary.
	for room in oldRooms:
		newRooms.append(room.copy())
	for name in oldImgPuzzles:
		newImagePuzzles[name] = state["Image_Puzzles"][name].copy()
	for name in oldMusPuzzles:
		newMusicPuzzles[name] = state["Music_Puzzles"][name].copy()
	for rule in oldRules:
		newRules.append(rule.copy())
		
	# Put the new lists into the new state's lists.
	newState["Rooms"] = newRooms
	newState["Rules"] = newRules
	newState["Image_Puzzles"] = newImagePuzzles
	newState["Music_Puzzles"] = newMusicPuzzles
	
	# Primitives and operators do not need to be deep copied.
	newState["Selected_Room"] = state["Selected_Room"]
	newState["Selected_Image"] = state["Selected_Image"]
	newState["Selected_Music"] = state["Selected_Music"]
	newState["Role"] = state["Role"]
	
	# These are constant so the pointer can be passed up.
	newState['ConditionMaster'] = state['ConditionMaster']
	newState['ActionMaster'] = state['ActionMaster']
	
	# Operators is updated in set_operators.
	newState["Operators"] = state["Operators"]
	
	return newState
		
def describe_state(state):
	""" Produces a textual description of a state.
    Might not be needed in normal operation with GUIs."""	
	
# Goes through the rules of a state and marks the ones 
# refer to non-existent objects as defunct.
def check_rules(state):
	dAlert("checking rules")
	# Checks the string
	rules = state["Rules"]
	defunct = False
	for rule in rules:
		
		# Check cause
		for condition in rule.conditions:
			cdSplit = condition.split(" ")
			if(cdSplit[0] == "Solve:"):
				# Look for attached puzzle name inside both dictionaries of puzzles
				if(state["Music_Puzzles"][cause[1]] is None or state["Image_Puzzles"][cause[1]] is None):
					defunct = True
		
		for action in rule.actions:
			# Check action
			acSplit = rule.action.split(" ")
			if(acSplit[0] == "Open" or acSplit[0] == "Close"):
				roomNum = acSplit[4]
				dir = acSplit[6]
				
				# True if no door 
				if(state["Rooms"][roomNum]["Walls"][dir].hasDoor):
					defunct = True
			
		rule.defunct = defunct
		
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
	
class Room:

	""" A room in the game contains 4 walls that could have wallpapers or doors
		and a possible ambient soundtrack, and a possible puzzle. """
	def __init__(self, x1, y1, x2, y2, aMusic = None):
		
		# Coordinates for display of the room.
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		
		# Ambient music, contains a url to a piece of music mp3
		self.aMusic = aMusic
		
		# 4 walls. 
		self.walls = {}
		# Horizontal walls.
		self.walls['N'] = Wall(x1 ,y1 ,x2 ,y1, 'N') #top 
		self.walls['S'] = Wall(x1 ,y2 ,x2 ,y2, 'S') #bottom
			
		# Vertical walls.
		self.walls['W'] = Wall(x1 ,y1 ,x1 ,y2, 'W') #left
		self.walls['E'] = Wall(x2 ,y1 ,x2 ,y2, 'E') #right
		
	def copy(self):
			
		newRoom = Room(self.x1, self.y1, self.x2, self.y2, self.aMusic)
		for direction in ['N','S','W','E']:
			newRoom.walls[direction] = self.walls[direction].copy()
		
		return newRoom
		
""" A wall could contain a door and a wallpaper """	
class Wall:

	def __init__(self, x1, y1, x2, y2, loc, wallpaper = None, hasDoor = False, doorOpen = None, puzzle = None): 
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.loc = loc
		self.wallpaper = wallpaper
		
		if(self.wallpaper is None):
			# Creates a wallpaper, default picture is wall.jpg
			self.wallpaper = Wallpaper()
		
		# Whether the wall contains a door and if its open or not
		self.hasDoor = hasDoor
		self.doorOpen = doorOpen
		
		# Possible puzzle
		self.puzzle = puzzle
		
	# Returns a copy of itself. Does not copy its door.
	def copy(self):
		newWall = Wall(self.x1,self.y1,self.x2,self.y2,self.loc, self.wallpaper.copy(), self.hasDoor, self.doorOpen, self.puzzle)
		return newWall
		
# Default url is wall.jpg
# Test url is stripes.jpg for transformation testing.
class Wallpaper:
	
	def __init__(self, url = "images/wall.jpg"):
		
		# url of image to be displayed on the wallpaper, automatically set to wall.jpg
		self.url = url
	
	# Returns a copy of itself.
	def copy(self):
		
		return Wallpaper(self.url)
'''
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
'''
class ImagePuzzle:

	def __init__(self, url = "images/metalfencing.jpg", transformList = []):
		
		self.url = url
		
		# shallow copying a new list
		self.transformList = transformList[:]
	
	def add_transform(self, transform):
		self.transformList.append(transform)
	
	def copy(self):
		return ImagePuzzle(self.url, self.transformList)
		
class MusicPuzzle:

	def __init__(self, notes = [], transformList = []):
		
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

		return MusicPuzzle(noteCopy, self.transformList)

# Defaults are empty lists
class Rule:
	def __init__(self, conditions = [], actions = [], defunct = False):
			
		self.conditions = conditions[:]
		self.actions = actions[:]
		
		# Whether the rule still applies to the current architecture.
		self.defunct = defunct		
		
		self.name = "C: " + str(self.conditions) + ", " + "A: " + str(self.actions)
	
	# Copies the rule, list is used to return a new list
	def copy(self):
		
		return Rule(list(self.conditions), list(self.actions), self.defunct)


# Takes a room num from 0 to 8 and a side for the door to be on, [N, S, E, W]
# Optional newDoor parameter which allows you to pass which door the walls will point to.
# Is default set to the creation of a new door.
def add_door_to_room(room_num, side, state):
	ROOMS = state["Rooms"]
	
	ROOMS[room_num].walls[side].hasDoor = True
	if side == 'N':
		ROOMS[room_num - 3].walls['S'].hasDoor = True
	elif side == 'S':
		ROOMS[room_num + 3].walls['N'].hasDoor = True
	elif side == 'E':
		ROOMS[room_num + 1].walls['W'].hasDoor = True
	elif side == 'W':
		ROOMS[room_num - 1].walls['E'].hasDoor = True
	else:
		alert("Error: Invalid direction passed to add_door")


# Operator version of add door that returns new state
def add_door_operator(state, room_num, side):
	
	newState = copy_state(state)
	add_door_to_room(room_num, side, newState)
	
	return newState

# Removes the door between two walls or a puzzle on a wall
def remove_wall_object_from_room(state, side):
	room_num = state["Selected_Room"]
	rooms = state["Rooms"]
	wall = state["Rooms"][room_num].walls[side]
	if(wall.hasDoor):
		wall.hasDoor = False
		if side == 'N':
			dAlert(side)
			wall = rooms[room_num - 3].walls['S']
		elif side == 'S':
			wall = rooms[room_num + 3].walls['N']
		elif side == 'E':
			wall = rooms[room_num + 1].walls['W']
		elif side == 'W':
			wall = rooms[room_num - 1].walls['E']
		wall.hasDoor = False
		check_rules(state)
	elif(wall.puzzle is not None):
		wall.puzzle = None
		check_rules(state)
	else:
		alert("no puzzle or door to remove")
		

# Operator version of remove door that returns new state
def remove_wall_object_operator(state, side):

	newState = copy_state(state)
	remove_wall_object_from_room(newState,side)
	return newState
	
# Checks if a door can be placed on a wall, meaning a door cannot already be on a wall
# and a puzzle cannot be on the wall or on the other side of the wall.
def add_doors_is_valid(state, side):
	ROOMS = state["Rooms"]
	room_num = state["Selected_Room"]
	if side == 'N':
		north_room = room_num - 3
		if (north_room < 0):
			return False
		elif (ROOMS[room_num].walls['N'].hasDoor == True
				or ROOMS[room_num].walls['N'].puzzle is not None
				or ROOMS[north_room].walls['S'].puzzle is not None):
			return False
		else:
			return True
	elif side == 'S':
		south_room = room_num + 3
		if (south_room > 8):
			return False
		elif (ROOMS[room_num].walls['S'].hasDoor == True 
				or ROOMS[room_num].walls['S'].puzzle is not None
				or ROOMS[south_room].walls['N'].puzzle is not None):
			return False
		else:
			return True
	elif side == 'E':
		east_room = room_num + 1
		if (room_num + 1) % 3 is 0:
			return False
		elif (ROOMS[room_num].walls['E'].hasDoor == True 
				or ROOMS[room_num].walls['E'].puzzle is not None
				or ROOMS[east_room].walls['W'].puzzle is not None): 	
			return False
		else:
			return True
	elif side == 'W':
		west_room = room_num - 1
		if (room_num + 1) % 3 is 1:
			return False
		elif (ROOMS[room_num].walls['W'].hasDoor == True
				or ROOMS[room_num].walls['W'].puzzle is not None
				or ROOMS[west_room].walls['E'].puzzle is not None):	
			return False
		else: 
			return True
	else:
		return False

# Return true if a door can be removed and false if it cant
def remove_wall_object_is_valid(state,side):
	room = state['Rooms'][state["Selected_Room"]]
	wall = room.walls[side]
	return wall.hasDoor or wall.puzzle is not None
	
# Adds the passed puzzle name to the correct room and side of the 
# passed state. Default is creation of new blank imagePuzzle.
def add_puzzle_to_room(room_num,side, state, name = None):
	if name is None:
		
		# Create default name, make sure its unique
		name = "defaultImagePuzzle"
		name = check_puzzle_name(state,name)
		puzzle = ImagePuzzle()
		state["Image_puzzles"][name] = puzzle
		
	state["Rooms"][room_num].walls[side].puzzle = name
	
def add_puzzle_operator(state, room_num, sendBack):
	
	def processMenu(state,side,puzzleName):
		newState = copy_state(state)
		add_puzzle_to_room(room_num,side,newState,puzzleName)
		sendBack(newState)
		
	# Get banned directions
	bannedDirections = puzzles_is_valid(state)
	# Creates a menu with banned direction radio buttons disabled
	add_puzzle_menu(state, processMenu,bannedDirections)

# returns a list of cardinals representing 
# sides of a room that can not be used to place a puzzle
def puzzles_is_valid(state):
	invalidCardinals = []
	room_num = state["Selected_Room"]
	selectedRoom = state["Rooms"][room_num]
	
	for c in ['N','S','E','W']:
		if (selectedRoom.walls[c].puzzle is not None or selectedRoom.walls[c].hasDoor == True):
			invalidCardinals.append(c)

	return invalidCardinals		
		
# takes a room num from 0 to 8 and prompts the user for a url for the wallpaper
def add_wallpaper_to_room(state):
	
	# Prompt the user for wallpaper url 
	url = window.prompt("Enter a complete URL for a wallpaper. Say 'cancel' to cancel.", "images/wall.jpg")
	if(url is None):
	
		return None
		
	elif(url_is_valid(url)):
	
		newState = copy_state(state)
		room = newState["Rooms"][newState["Selected_Room"]]
		for loc in room.walls:
			room.walls[loc].wallpaper.url = url
		
		return newState
		
	else:
	
		alert("URL was not valid. Try again.")
		
		# Recurse
		return add_wallpaper_to_room(state)

	
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
	
def change_image_puzzle_selection(state, name):
	newState = copy_state(state)
	newState["Selected_Image"] = name
	return newState

def change_music_puzzle_selection(state, name):
	newState = copy_state(state)
	newState["Selected_Music"] = name
	return newState
	
def change_role(state, role):
	global OPERATORS
	global stopAmbientMusic
	
	if(state["Role"] == "Architect"):
		stopAmbientMusic()
	
	newState = copy_state(state)
	newState['Role'] = role
	
	# reset the operators
	newState['Operators'] = set_operators(newState)
	
	return newState

def create_image_puzzle(state):
	# Prompt the user for a image url
	url = window.prompt("Enter a complete URL for a picture. Say 'cancel' to cancel.", "images/force.jpg")
	if(url is None):
	
		return None
		
	elif(url_is_valid(url)):
	
		
		newState = copy_state(state)
		
		# Get name, make sure there are no copies
		name = getName(url)
		name = check_puzzle_name(state,name)
	
		newPuzzle = ImagePuzzle(url)
		
		# Add newPuzzle to dictionary
		newState["Image_Puzzles"][name] = newPuzzle
		newState["Selected_Image"] = name

		return newState
		
	else:
	
		alert("URL was not valid. Try again.")
		# Recurse
		return create_image_puzzle(state)	
	
	
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
	
def check_puzzle_name(state,name):
	# Make sure there are no copies of the name in image puzzles
	imageNames = state["Image_Puzzles"]
	musicNames = state["Music_Puzzles"]
	i = 1
	newName = name
	while(newName in imageNames or newName in musicNames):
		newName = name + " (" + str(i) + ")"
		i = i + 1
	return newName

# NOTE: This operators requires Brython as it uses a JSON object.
def create_music_puzzle(state, sendBack):
	
	url = window.prompt("Enter a complete URL for a json music file. Say 'cancel' to cancel.", "music/twinkleTwinkle.txt")
	
	if(url_is_valid(url)):
		
		# Double nested to allow use of name parameter
		def requestSuccess(name):
			# When the request is recieved
			def requestSuccess2(req):
				if(req.status == 200 or req.status == 0):
					newState = copy_state(state)
					# Assign name to song using data from JSON object
					song = json.loads(req.responseText)
					newPuzzle = MusicPuzzle(song["notes"])
					newState["Music_Puzzles"][name] = newPuzzle
					newState["Selected_Music"] = name
					
					# Hide loading visualization
					hide_loading()
					
					sendBack(newState)
				else:
					print("request failure")
			return requestSuccess2
		
		# Show loading visualization
		show_loading()
		
		# Get name, make sure there are no copies
		name = getName(url)
		name = check_puzzle_name(state,name)
		
		request = ajax.ajax()
		request.open('GET',url,True)
		request.bind("complete",requestSuccess(name))
		request.send()
	
	elif(url != "cancel"):
		alert("URL was not valid. Try again.")
		create_music_puzzle(state, sendBack)
	else:
		sendBack()

# Adds ambient music to a room. The rule designer chose when and if these play.		
def add_ambient_music(state):

	url = window.prompt("Enter a url for an mp3 to attach ambient music to a room", "music\defaultAmbient.mp3")
	if(url is None):
	
		return None
		
	elif(url_is_valid(url)):
	
		
		newState = copy_state(state)
		room_num = newState["Selected_Room"]
		
		# Add ambient music to room
		newState["Rooms"][room_num].aMusic = url

		return newState
		
	else:
	
		alert("URL was not valid. Try again.")
		
		# Recurse
		return add_ambient_music(state)
	
# Plays the ambient music in the selected room
def play_ambient_music(state):
	global show_loading, hide_loading
	global playAmbientMusic
	
	music = state["Rooms"][state["Selected_Room"]].aMusic

	def doneLoading():
		hide_loading()

	if(music is not None):
		show_loading()
		stopAmbientMusic()
		playAmbientMusic(music,doneLoading)
		
	return None

# Stops the ambient music from playing
def stop_ambient_music():
	stopAmbientMusic()

	
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

def createRule(state):
	newState = copy_state(state)
	newRule = Rule()
	newState["Rules"].append(newRule)
	
	return newState

def deleteRule(state, index):
	newState = copy_state(state)
	del newState["Rules"][index]
	
	return newState

def addCondition(state, index, sendBack):

	def processCondition(condition):
		newState = copy_state(state)
		newState["Rules"][index].conditions.append(condition)
		sendBack(newState)
	
	add_condition_menu(state, processCondition)
	
def addAction(state, index, sendBack):
	
	def processAction(action):
		newState = copy_state(state)
		newState["Rules"][index].actions.append(action)
		sendBack(newState)
	
	add_action_menu(state, processAction)	
	
#</COMMON_CODE>		

#<OPERATORS>
# Method that can be called to set the Operators 
# of the current Role given the current State.
# Each AsyncOperators state transfer must have a callback function defined.
def set_operators(state):

	# Sendback is the function given by the client which receives the modified state
	sb = None

	role_operators =\
		[Operator("Change Role to " + role + " Designer.",
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
		
		remove_object_operators =\
			[Operator("Remove puzzle or door from room on " + cardinal + " wall.",
				lambda state, c = cardinal: remove_wall_object_is_valid(state, c[0]),
				lambda state, c = cardinal: remove_wall_object_operator(state, c[0]))
			for cardinal in ['North', 'South', 'East', 'West']]
			
		wallpaper_operators =\
			Operator("Add wallpaper to current room.",
				lambda state: True,
				lambda state: add_wallpaper_to_room(state))
				
		add_puzzle_operators =\
			AsyncOperator("Add a puzzle to current room",
				lambda state: puzzles_is_valid(state) != ['N','S','E','W'],
				lambda state, sb: add_puzzle_operator(state, state["Selected_Room"], sb))
				
		add_ambient_music_operator =\
			Operator("Add ambient music to current room.",
				lambda state: True,
				lambda state: add_ambient_music(state))
		
		play_ambient_music_operator =\
			Operator("Play the ambient music in current room.",
				lambda state: state["Rooms"][state["Selected_Room"]].aMusic is not None,
				lambda state: play_ambient_music(state))
		
		stop_ambient_music_operator =\
			Operator("Stop all music from playing",
				lambda state: True,
				lambda state: stop_ambient_music())
				
		OPERATORS = selection_operators	+ add_door_operators + remove_object_operators + wallpaper_operators + add_puzzle_operators + add_ambient_music_operator + play_ambient_music_operator + stop_ambient_music_operator + role_operators
	
	elif(state['Role'] == "Image Puzzle"):
		
		puzzles = state["Image_Puzzles"]
		numOfPuzzles = len(puzzles)
		
		selection_operators =\
			[Operator("Switch to puzzle \"" + name + "\" for editing",
				lambda state, n = name: numOfPuzzles > 1 and n != state["Selected_Image"],
				lambda state, n = name: change_image_puzzle_selection(state, n))
			for name in puzzles.keys()]
		
		create_new_puzzle =\
			Operator("Create a new image puzzle.",
				lambda state: True,
				lambda state: create_image_puzzle(state))
				
		horiz_flip =\
			Operator("Flip the image horizontally.",
				lambda state: state["Selected_Image"] is not None,
				lambda state: addImageTransformation(state, "horizFlip"))
		vert_flip =\
			Operator("Flip the image vertically.",
				lambda state: state["Selected_Image"] is not None,
				lambda state: addImageTransformation(state, "vertFlip"))
		shuff_rows =\
			Operator("Shuffle the rows of the image.",
				lambda state: state["Selected_Image"] is not None,
				lambda state: addImageTransformation(state, "shuffleRows"))
		invs_shuff_rows =\
			Operator("Invert Row shuffling",
				lambda state: state["Selected_Image"] is not None,
				lambda state: addImageTransformation(state, "shuffleRowsInverse"))
		shuff_cols =\
			Operator("Shuffle the columns of the image.",
				lambda state: state["Selected_Image"] is not None,
				lambda state: addImageTransformation(state, "shuffleColumns"))
				
		OPERATORS =   selection_operators + create_new_puzzle + horiz_flip + vert_flip + shuff_rows + invs_shuff_rows + shuff_cols + role_operators
		
	elif(state['Role'] == "Music Puzzle"):
		
		puzzles = state["Music_Puzzles"]
		numOfPuzzles = len(puzzles)
		
		selection_operators =\
			[Operator("Switch to puzzle \"" + name + "\" for editing.",
				lambda state, n = name: numOfPuzzles > 1 and n != state["Selected_Music"],
				lambda state, n = name: change_music_puzzle_selection(state, n))
			for name in puzzles.keys()]
		
		create_new_puzzle =\
			AsyncOperator("Create a new music puzzle.",
				lambda state: True,
				lambda state, sb: create_music_puzzle(state, sb))
		
		increase_pitch =\
			Operator("Increase pitch of song",
				lambda state: state["Selected_Music"] is not None,
				lambda state: addMusicTransformation(state, "increasePitch"))
		
		decrease_pitch =\
			Operator("Decrease pitch of song",
				lambda state: state["Selected_Music"] is not None,
				lambda state: addMusicTransformation(state, "decreasePitch"))
		
		increase_tempo =\
			Operator("Increase tempo of song",
				lambda state: state["Selected_Music"] is not None,
				lambda state: addMusicTransformation(state, "increaseTempo"))
		
		decrease_tempo =\
			Operator("Decrease tempo of song",
				lambda state: state["Selected_Music"] is not None,
				lambda state: addMusicTransformation(state, "decreaseTempo"))

		shuffle_notes =\
			Operator("Shuffle notes of song",
				lambda state: state["Selected_Music"] is not None,
				lambda state: addMusicTransformation(state, "shuffleNotes"))

		reverse_notes =\
			Operator("Reverse notes of song",
				lambda state: state["Selected_Music"] is not None,
				lambda state: addMusicTransformation(state, "reverseNotes"))
		
		OPERATORS = selection_operators + role_operators  + create_new_puzzle + increase_tempo + decrease_tempo + shuffle_notes + increase_pitch + decrease_pitch + reverse_notes        
	
	elif(state['Role'] == "Rules"):
		create_rule =\
			Operator("Create new Rule.",
				lambda state: True,
				lambda state: createRule(state))
				
		delete_rules =\
			[Operator("Delete Rule " + str(index + 1) + ", \"" + rule.name + "\"",
				lambda state: True,
				lambda state, i = index: deleteRule(state, i))
			for index, rule in enumerate(state["Rules"])]
		
		add_condition =\
			[AsyncOperator("Add Condition to Rule " + str(index + 1) + ".",
				lambda state, r = rule: not r.defunct, #If defunct is false then valid
				lambda state, sb, i = index: addCondition(state, i, sb))
			for index, rule in enumerate(state["Rules"])]
		
		add_action =\
			[AsyncOperator("Add Action to Rule " + str(index + 1) + ".",
				lambda state, r = rule: not r.defunct, #If defunct is false then valid
				lambda state, sb, i = index: addAction(state, i, sb))
			for index, rule in enumerate(state["Rules"])]		
			
		OPERATORS = role_operators + create_rule + delete_rules + add_condition + add_action
	else:
		alert("unsupported role")
	

	return OPERATORS

#</OPERATORS>
	
#<INITIAL_STATE> The game is a list of 9 rooms stored a list.
INITIAL_STATE = {}
INITIAL_STATE['Rooms'] = []
INITIAL_STATE['Image_Puzzles'] = {}
INITIAL_STATE['Music_Puzzles'] = {}

# ADD A BLANK MUSIC PUZZLE FOR DEBUG PURPOSES ONLY
INITIAL_STATE["Music_Puzzles"]["test puzzle1"] = MusicPuzzle()

INITIAL_STATE['Rules'] = []

# ADD BLANK RULES FOR DEBUG PURPOSES ONLY

INITIAL_STATE['Rules'].append(Rule())
'''INITIAL_STATE['Rules'].append(Rule())
INITIAL_STATE['Rules'].append(Rule(["Cool bean",'fdafsasdfadfasfdaf','aaaaaaaaa'],["cool cream"], True))
INITIAL_STATE['Rules'].append(Rule())
INITIAL_STATE['Rules'].append(Rule())
INITIAL_STATE['Rules'].append(Rule(["not cool bean"]))
INITIAL_STATE['Rules'].append(Rule())
INITIAL_STATE['Rules'].append(Rule())
INITIAL_STATE['Rules'].append(Rule())
INITIAL_STATE['Rules'].append(Rule())
INITIAL_STATE['Rules'].append(Rule())
INITIAL_STATE['Rules'].append(Rule())
INITIAL_STATE['Rules'].append(Rule())
INITIAL_STATE['Rules'].append(Rule())
'''


INITIAL_STATE['Selected_Room'] = 0

# Stores name of selected image and selected music
INITIAL_STATE['Selected_Image'] = None
INITIAL_STATE['Selected_Music'] = None
INITIAL_STATE['Role'] = "Rules"
INITIAL_STATE['Operators'] = set_operators(INITIAL_STATE)	
INITIAL_STATE['ConditionMaster'] = ["Enter Room"]
INITIAL_STATE['ActionMaster'] = ["Open Door", "Close Door", "Play Music", "Display Message"]

# Create 9 rooms, add them to the the state.
for j in range(3):
	for i in range(3):
		INITIAL_STATE['Rooms'].append( Room(i, j, i + 1, j + 1) )	

# Temporary addition for debug purposes
INITIAL_STATE["Rooms"][0].aMusic = "music\defaultAmbient.mp3"
		
# Now initialize operators.
OPERATORS = INITIAL_STATE['Operators']
#</INITIAL_STATE>




