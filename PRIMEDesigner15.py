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
	from PRIMEDesigner15VisForBrython import hide_loading, show_loading, url_is_valid
	from PRIMEDesigner15VisForBrython import add_puzzle_menu, add_condition_menu, add_action_menu, edit_rule_menu
	from PRIMEDesigner15VisForBrython import delete_condition_menu, delete_action_menu, open_or_closed_menu
	from templateRoot.PRIMEDesigner15Operator import Operator as Operator
	from templateRoot.PRIMEDesigner15Operator import AsyncOperator as AsyncOperator
	
from browser import document, window, alert, console, ajax
from javascript import JSObject, JSConstructor
import time, json, datetime

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
	
# Goes through the rules of a state and marks the conditions/actions 
# that refer to non-existent objects as app.
def check_rules(state):
	

	rules = state["Rules"]
	for rule in rules:	
		
		#Check condition
		for condition in rule.conditions:
			cdSplit = condition.text.split(" ")
			
			# If condition is "Solved Puzzle:"
			if(cdSplit[0] == "Solved"):
				'''
				puzzleName = condition.text.rsplit(':', 1)[1].strip()
				found = False
				for room in state["Rooms"]:
					for wall in room.walls.values():
						if wall.puzzle == puzzleName:
							found = True
						
				condition.app = found
				'''
				
				roomNum = cdSplit[4]
				dir = cdSplit[6]
				
				if(state["Rooms"][int(roomNum)-1].walls[dir].puzzle is None):
					condition.app = False
				#In the off chance that a puzzle is placed, a rule element added to it,
				#And then the puzzle is removed, but then a puzzle is placed in the same spot
				else:
					condition.app = True
					
				'''
				#If we want to check that the puzzle exists at all
				puzzleName = condition.text.rsplit(':', 1)[1].strip()
				console.log(puzzleName)
				if(puzzleName in state['Image_Puzzles'] or puzzleName in state['Music_Puzzles']):
					condition.app = True
				else:
					condition.app = False
				'''	
	
		for action in rule.actions:
			# Check action
			acSplit = action.text.split(" ")
			
			# If action is opening or closing a door:
			if(acSplit[0] == "Open" or acSplit[0] == "Close"):
				roomNum1 = int(acSplit[4])
				roomNum2 = int(acSplit[6])
				
				#switch from visual index to array index
				roomNumFinal = roomNum1 - 1 
				
				if roomNum2 - roomNum1 == 1:
					dir = 'E'
				else:
					dir = 'S'
					
				if state["Rooms"][roomNumFinal].walls[dir].hasDoor is False:
					action.app = False
				else:
					action.app = True
				'''
				roomNum = acSplit[4]
				dir = acSplit[6]
				 
				if(state["Rooms"][int(roomNum)-1].walls[dir].hasDoor is False):
					action.app = False
				'''	
			# If action is "Unsolve Puzzle:"
			if(acSplit[0] == "Unsolve"):
				roomNum = acSplit[4]
				dir = acSplit[6]
				
				if(state["Rooms"][int(roomNum)-1].walls[dir].puzzle is None):
					action.app = False
				#In the off chance that a puzzle is placed, a rule element added to it,
				#And then the puzzle is removed, but then a puzzle is placed in the same spot
				else:
					action.app = True		
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
		and possible ambient audio, and a possible puzzle. """
	def __init__(self, x1, y1, x2, y2, aAudio = None):
		
		# Coordinates for display of the room.
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		
		# Ambient music, contains a url to a piece of music mp3
		self.aAudio = aAudio
		
		# 4 walls. 
		self.walls = {}
		# Horizontal walls.
		self.walls['N'] = Wall(x1 ,y1 ,x2 ,y1, 'N') #top 
		self.walls['S'] = Wall(x1 ,y2 ,x2 ,y2, 'S') #bottom
			
		# Vertical walls.
		self.walls['W'] = Wall(x1 ,y1 ,x1 ,y2, 'W') #left
		self.walls['E'] = Wall(x2 ,y1 ,x2 ,y2, 'E') #right
		
	def copy(self):
			
		newRoom = Room(self.x1, self.y1, self.x2, self.y2, self.aAudio)
		for direction in ['N','S','W','E']:
			newRoom.walls[direction] = self.walls[direction].copy()
		
		return newRoom
		
	def encode(self):
		return {#"Vector Coordinates" : {"x1": self.x1, "y1": self.y1, "x2": self.x2, "y2": self.y2},
				"Walls" : {"N" : self.walls['N'].encode(), "S" : self.walls['S'].encode(),
						   "W" : self.walls['W'].encode(), "E" : self.walls['E'].encode()},
				"Ambient Music" : self.aAudio}
		
""" A wall could contain a door and a wallpaper """	
class Wall:

	def __init__(self, x1, y1, x2, y2, loc, wallpaperurl = "images/wall.jpg", hasDoor = False, doorOpen = None, puzzle = None): 
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.loc = loc
		self.wallpaperurl = wallpaperurl
		
		# Whether the wall contains a door and if its open or not
		self.hasDoor = hasDoor
		self.doorOpen = doorOpen
		
		# Possible puzzle
		self.puzzle = puzzle
		
	# Returns a copy of itself. Does not copy its door.
	def copy(self):
		newWall = Wall(self.x1,self.y1,self.x2,self.y2,self.loc, self.wallpaperurl, self.hasDoor, self.doorOpen, self.puzzle)
		return newWall
	
	def encode(self):
		return 	{#"Vector Coordinates" : {"x1": self.x1, "y1": self.y1, "x2": self.x2, "y2": self.y2},
				 "Location" : self.loc,
				 "Wallpaper" : self.wallpaperurl,
				 "HasDoor" : self.hasDoor,
				 "DoorOpen" : self.doorOpen,
				 "Puzzle" : self.puzzle}
		
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
		
	def encode(self):
		return {"Type" : "image", "URL" : self.url, "Transform List" : self.transformList}
		
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

	def encode(self):
		return {"Type" : "music", "Notes" : self.notes, "Transform List" : self.transformList}		
		
# A rule contains two lists of RuleElements. Conditions and actions.
class Rule:
	def __init__(self, conditions = [], actions = []):
			
		self.conditions = conditions[:]
		self.actions = actions[:]	
		
		self.name = "C: "
		for condition in self.conditions:
			self.name += condition.text + ","
		self.name += " A: "
		for action in self.actions:
			self.name += action.text + ","
		
	
	# Copies the rule, list is used to return a new list
	def copy(self):
		newConditions = []
		newActions = []
		
		for condition in self.conditions:
			newConditions.append(condition.copy())
		for action in self.actions:
			newActions.append(action.copy())
		
		return Rule(newConditions, newActions)

	def encode(self):
		conditionsJSON = [condition.encode() for condition in self.conditions]
		actionsJSON = [action.encode() for action in self.actions]
		return {"Conditions" : conditionsJSON, 
				"Actions" : actionsJSON,
				"Name" : self.name}
				
class RuleElement:
	def __init__(self, text, app = True):
		self.text = text
		self.app = app
		
	def copy(self):
		return RuleElement(self.text, self.app)
		
	def encode(self):
		result = {}
		result["Applicable"] = self.app
		textSplit = self.text.split(" ")
		
		if(textSplit[0] == 'Entered'):
			result["Condition"] = 'Entered Room'
			result["Room"] = int(textSplit[2])
		elif(textSplit[1] == 'puzzle'):
			if(textSplit[0] == 'Solved'):
				result["Condition"] = 'Solved puzzle'
			else:
				result["Action"] = 'Unsolve puzzle'
			result["Room"] = int(textSplit[4])
			result["Wall"] = textSplit[6]
		elif(textSplit[0] == 'Had'):
			result["Condition"] = 'Had Points'
			result["Points"] = int(textSplit[1])
		elif(textSplit[1] == 'minutes'):
			result["Condition"] = 'Minutes elapsed'
			result["Minutes"] = int(textSplit[0])
		elif(textSplit[1] == 'door'):
			result["Action"] = textSplit[0] + ' a door between two rooms'
			result["Room"] = int(textSplit[4])
			result["Room2"] = int(textSplit[6])
		elif(textSplit[0] == 'Display'):
			result["Action"] = 'Display a message'
			result["Message"] = textSplit[2]
			for i in range(3, len(textSplit)):
				result["Message"] += " " + textSplit[i]
		elif(textSplit[1] == 'Sound'):
			result["Action"] = 'Play sound from URL'
			result["URL"] = textSplit[4]
		elif(textSplit[2] == 'Points'):
			result["Action"] = textSplit[0] + " points"
			result["Points"] = int(textSplit[1])
		console.log(result)	
		return result
				
# Takes a room num from 0 to 8 and a side for the door to be on, [N, S, E, W]
# Optional newDoor parameter which allows you to pass which door the walls will point to.
# Is default set to the creation of a new door.
def add_door_to_room(state, room_num, side, openOrClosed):
	ROOMS = state["Rooms"]
	
	ROOMS[room_num].walls[side].hasDoor = True
	ROOMS[room_num].walls[side].doorOpen = openOrClosed
	if side == 'N':
		ROOMS[room_num - 3].walls['S'].hasDoor = True
		ROOMS[room_num - 3].walls['S'].doorOpen = openOrClosed
	elif side == 'S':
		ROOMS[room_num + 3].walls['N'].hasDoor = True
		ROOMS[room_num + 3].walls['N'].doorOpen = openOrClosed
	elif side == 'E':
		ROOMS[room_num + 1].walls['W'].hasDoor = True
		ROOMS[room_num + 1].walls['W'].doorOpen = openOrClosed
	elif side == 'W':
		ROOMS[room_num - 1].walls['E'].hasDoor = True
		ROOMS[room_num - 1].walls['E'].doorOpen = openOrClosed
	else:
		alert("Error: Invalid direction passed to add_door")
	
	check_rules(state)

# Operator version of add door that returns new state
def add_door_operator(state, room_num, side, sendBack):
	def processState(openOrClosed):
		newState = copy_state(state)
		add_door_to_room(newState, room_num, side, openOrClosed)
		sendBack(newState)
		
	open_or_closed_menu(processState)
	
	
# Removes the door between two walls or a puzzle on a wall
def remove_wall_object_from_room(state, side):
	room_num = state["Selected_Room"]
	rooms = state["Rooms"]
	wall = state["Rooms"][room_num].walls[side]
	if(wall.hasDoor):
		wall.hasDoor = False
		if side == 'N':
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
		state["Image_Puzzles"][name] = puzzle
		
	state["Rooms"][room_num].walls[side].puzzle = name
	check_rules(state)
	
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
			room.walls[loc].wallpaperurl = url
		
		return newState
		
	else:
	
		alert("URL was not valid. Try again.")
		
		# Recurse
		return add_wallpaper_to_room(state)

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
	
def check_if_puzzle_copy(state,name):
	# Make sure there are no copies of the name in image puzzles
	imageNames = state["Image_Puzzles"]
	musicNames = state["Music_Puzzles"]
	if(name is None):
		return False
	if(name in imageNames or name in musicNames):
		return True
	return False

def rename_image_puzzle(state, sendBack):
	newName = window.prompt("Enter the new unique name for your puzzle: " + state["Selected_Image"], "")

	while(newName is not None and check_if_puzzle_copy(state,newName) is True):

		newName = window.prompt("There is already a puzzle with that name","")
	
	if(newName is not None):
	
		newState = copy_state(state)
		
		puzzle = newState["Image_Puzzles"][newState["Selected_Image"]]
		newState["Image_Puzzles"].pop(newState["Selected_Image"],None)
		
		newState["Image_Puzzles"][newName] = puzzle
		newState["Selected_Image"] = newName
	
		sendBack(newState)
	
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

def rename_music_puzzle(state, sendBack): 
	newName = window.prompt("Enter the new unique name for your puzzle: " + state["Selected_Image"], "")

	while(newName is not None and check_if_puzzle_copy(state,newName) is True):

		newName = window.prompt("There is already a puzzle with that name","")
	
	if(newName is not None):
	
		newState = copy_state(state)
		
		puzzle = newState["Music_Puzzles"][newState["Selected_Music"]]
		newState["Music_Puzzles"].pop(newState["Selected_Music"],None)
		
		newState["Music_Puzzles"][newName] = puzzle
		newState["Selected_Music"] = newName
	
		sendBack(newState)

		
# Adds ambient audio to a room. The rule designer chose when and if these play.		
def add_ambient_music(state):

	url = window.prompt("Enter a url for an mp3 to attach ambient audio to a room", "music\defaultAmbient.mp3")
	if(url is None):
	
		return None
		
	elif(url_is_valid(url)):
	
		
		newState = copy_state(state)
		room_num = newState["Selected_Room"]
		
		# Add ambient audio to room
		newState["Rooms"][room_num].aAudio = url

		return newState
		
	else:
	
		alert("URL was not valid. Try again.")
		
		# Recurse
		return add_ambient_music(state)

def create_json(state):
	global SOLUZION_VERSION, PROBLEM_NAME, PROBLEM_VERSION, PROBLEM_AUTHORS, PROBLEM_DESC
	
	#get the current date
	now = datetime.datetime.today()
	day = str(now.day)
	month = str(now.month)
	year = str(now.year)
	
	creationDate = month + '-' + day + '-' + year
	
	stateJSON = {"Soluzion Version" : SOLUZION_VERSION, "Problem Name" : PROBLEM_NAME, 
				 "Problem Version" : PROBLEM_VERSION, "Problem Authors"  : PROBLEM_AUTHORS, 
				 "Problem Creation Date" : creationDate, "Problem Description" : PROBLEM_DESC}
	
	#Rooms
	stateJSON["Rooms"] = []
	for room in state["Rooms"]:
		stateJSON["Rooms"].append(room.encode())
		#looks like stateJson = {"Rooms" : {1 : room1, 2 : room2, etc}, etc}

	stateJSON["Rules"] = []
	for rule in state["Rules"]:
		stateJSON["Rules"].append(rule.encode())
	
	stateJSON["Puzzles"] = {}
	for puzzle in state["Image_Puzzles"]:
		stateJSON["Puzzles"][puzzle] = state["Image_Puzzles"][puzzle].encode()
		
	for puzzle in state["Music_Puzzles"]:
		stateJSON["Puzzles"][puzzle] = state["Music_Puzzles"][puzzle].encode()	
	
	window.state_JSON = json.dumps(stateJSON)
	#console.log(window.state_JSON)
	
	req = ajax.ajax()
	req.bind('complete', lambda e: console.log('finished on brython side'))
	req.open('POST', 'dependencies//jsonPatch.php', True)
	req.set_header('content-type','application/x-www-form-urlencoded')
	req.send({'stateJSON' : window.state_JSON})
	
	#Puzzles
	#Rules
	#We don't need to send the selected room, image/music puzzles, role, 
	#the operators, or the action/condition master
	
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
		newState["Rules"][index].conditions.append(RuleElement(condition))
		
		check_rules(newState)
		
		sendBack(newState)
	
	add_condition_menu(state, processCondition)
	
def addAction(state, index, sendBack):
	
	def processAction(action):
		newState = copy_state(state)
		newState["Rules"][index].actions.append(RuleElement(action))

		check_rules(newState)

		sendBack(newState)
	
	add_action_menu(state, processAction)	

# Deletes a condition from the specified rule
def deleteCondition(state, index, sendBack):

	def processDelete(conditionName):
		newState = copy_state(state)
		conditionList = newState["Rules"][index].conditions
		for i, condition in enumerate(conditionList):
			if(condition.text == conditionName):
				conditionList.pop(i)
		
		sendBack(newState)
		
	delete_condition_menu(state, index, processDelete)

# Deletes an action from the specified rule
def deleteAction(state, index, sendBack):
	
	def processDelete(actionName):
		newState = copy_state(state)
		actionList = newState["Rules"][index].actions
		for i, action in enumerate(actionList):
			if(action.text == actionName):
				actionList.pop(i)
		
		sendBack(newState)
		
	delete_action_menu(state, index, processDelete)

			
# Concatenates several operators into one with a central menu.
def editRule(state, index, sendBack):

	def processEdit(edit):
		if(edit == "addAction"):
			addAction(state,index,sendBack)
		elif(edit == "addCondition"):
			addCondition(state,index,sendBack)
		elif(edit == "deleteAction"):
			deleteAction(state,index,sendBack)
		elif(edit == "deleteCondition"):
			deleteCondition(state,index,sendBack)
		elif(edit == "deleteRule"):
			newState = deleteRule(state,index)
			sendBack(newState)
		else:
			pass
	
	edit_rule_menu(state, processEdit)
	
def doNothing():
	pass

#</COMMON_CODE>		

#<OPERATORS>
# Method that can be called to set the Operators 
# of the current Role given the current State.
# Each AsyncOperators state transfer must have a callback function defined.
def set_operators(state):

	# Sendback is the function given by the client which receives the modified state
	sb = None
	
				
	create_json_file =\
		AsyncOperator("Create JSON file for the current state.",
			lambda state: True,
			lambda state, sb: create_json(state))
	
	nothing_selected =\
		[Operator("Nothing Selected", 
			lambda state: True, 
			lambda state: doNothing())]
	
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
			[AsyncOperator("Add door to current room on " + cardinal + " wall.",
				lambda state, c = cardinal: add_doors_is_valid(state, c),
				lambda state, sb, c = cardinal: add_door_operator(state, state["Selected_Room"], c, sb))
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
			Operator("Add ambient audio to current room.",
				lambda state: True,
				lambda state: add_ambient_music(state))
			
		# I don't know why I have to do this, something to do with memory perhaps.
		OPERATORS = nothing_selected	
		OPERATORS += role_operators + create_json_file + selection_operators + add_door_operators
		OPERATORS += remove_object_operators + wallpaper_operators + add_puzzle_operators + add_ambient_music_operator
	
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
				
		rename_puzzle =\
			AsyncOperator("Rename selected puzzle.",
				lambda state: state["Selected_Image"] is not None,
				lambda state, sb: rename_image_puzzle(state, sb))
				
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

		invs_shuff_cols =\
			Operator("Invert Column shuffling",
				lambda state: state["Selected_Image"] is not None,
				lambda state: addImageTransformation(state, "shuffleColumnsInverse"))

		shuff_cols =\
			Operator("Shuffle the columns of the image.",
				lambda state: state["Selected_Image"] is not None,
				lambda state: addImageTransformation(state, "shuffleColumns"))
				
		pixel_crossover =\
			Operator("Perform Pixel Crossover.",
				lambda state: state["Selected_Image"] is not None,
				lambda state: addImageTransformation(state, "pixelCrossover"))
				
		pixel_crossover_inverse =\
			Operator("Inverse Pixel Crossover.",
				lambda state: state["Selected_Image"] is not None,
				lambda state: addImageTransformation(state, "pixelCrossoverInverse"))				
				
		OPERATORS = nothing_selected + create_json_file + role_operators 
		OPERATORS += selection_operators + create_new_puzzle + rename_puzzle
		OPERATORS += [horiz_flip] + vert_flip + shuff_rows + shuff_cols + invs_shuff_rows + invs_shuff_cols + pixel_crossover + pixel_crossover_inverse	
	
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
		
		rename_puzzle =\
			AsyncOperator("Rename selected puzzle.",
				lambda state: state["Selected_Music"] is not None,
				lambda state, sb: rename_music_puzzle(state, sb))
		
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
		
		OPERATORS = nothing_selected + create_json_file
		OPERATORS += role_operators + selection_operators + create_new_puzzle + rename_puzzle + increase_tempo + decrease_tempo + shuffle_notes + increase_pitch + decrease_pitch + reverse_notes        
	
	elif(state['Role'] == "Rules"):
		create_rule =\
			Operator("Create new Rule.",
				lambda state: True,
				lambda state: createRule(state))
				
		edit_rule =\
			[AsyncOperator("Edit Rule " + str(index + 1) + ".",
				lambda state: True,
				lambda state, sb, i = index: editRule(state, i, sb))
			for index, rule in enumerate(state["Rules"])]
		
		OPERATORS = nothing_selected + create_json_file + role_operators + create_rule + edit_rule
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
INITIAL_STATE['ConditionMaster'] = ["Entered Room","Had Points","Time Elapsed", "Solved Puzzle"]
INITIAL_STATE['ActionMaster'] = ["Open Door", "Close Door", "Play Sound", "Display Message", 
								 "Unsolve Puzzle", "Gain Points","Lose Points","Game Ends"]

# Create 9 rooms, add them to the the state.
for j in range(3):
	for i in range(3):
		INITIAL_STATE['Rooms'].append( Room(i, j, i + 1, j + 1) )	

# TEMP DEBUG ADD PUZZLE
#add_puzzle_to_room(0,'E',INITIAL_STATE)

# Temporary addition for debug purposes
#INITIAL_STATE["Rooms"][0].aAudio = "music\defaultAmbient.mp3"
		
# Now initialize operators.
OPERATORS = INITIAL_STATE['Operators']
#</INITIAL_STATE>




