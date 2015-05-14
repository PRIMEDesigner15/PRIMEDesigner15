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

print("Hello from PRIMEDesigner15.py (after METADATA)")

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>

from browser import document, window
from javascript import JSObject, JSConstructor
import browser



# Preforms a deep copy of the given state. 
def copy_state(state):
	newState = {"Rooms": [], "Doors": []}
	newRooms = []
	newDoors = []

	# Copy the rooms (without doors in their walls) and doors into the newState's dictionary.
	for room in state["Rooms"]:
		newRooms.append(room.copy())
	for door in state["Doors"]:
		newDoors.append(door.copy())
		
	newState["Rooms"] = newRooms
	newState["Doors"] = newDoors
	newState["Selected"] = state["Selected"]	
	newState["Role"] = state["Role"]
		
	# Add in doors to the walls in the rooms.
	door_index = 0
	for room_num in range(9):
		for direction in ['N', 'S', 'E', 'W']:
			if(state["Rooms"][room_num].walls[direction].door is not None and newState["Rooms"][room_num].walls[direction].door is None):
				add_door_to_room(room_num, direction, newState, state["Doors"][door_index])
				door_index += 1
	
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
#except Exception as e:
#  print("There was an exception when trying to communicate back from Python to Javascript.")
#  print(e)

print("Hello from Mondrian.py (after INITIAL_STATE)")

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
		self.music = Music()
		
	def copy(self):
		newRoom = Room(self.x1, self.y1, self.x2, self.y2)
		for direction in ['N','S','W','E']:
			newRoom.walls[direction] = self.walls[direction].copy()
		if(self.music is None):
			newRoom.music = None
		else:
			newRoom.music = self.music.copy()
		
		return newRoom
				
	
		
""" A wall could contain a door or a wallpaper """	
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
	
	def __init__(self, url = "wall.jpg"):
		self.url = url
	
	# Returns a copy of itself.
	def copy(self):
		return Wallpaper(self.url)

class Door:
	
	def __init__(self, isOpen = True, url="door.jpg"):
		self.isOpen = isOpen
		self.url = url
		
	# Closes the door if it is open.
	# Opens the door if it is closed.
	def open_or_close(self):
		self.isOpen = not isOpen
	
	# Returns a copy of itself.
	def copy(self):
		return Door(self.isOpen, self.url)

class Puzzle:
	
	def __init__(self):
		pass# nothing happens right now
		
	def copy(self):
		return Puzzle() # nothing happens right now
		
class Music:

	def __init__(self):
		pass# nothing happens right now
	
	def copy(self):
		return Music() # nothing happens right now
	
#ask steve about what the Operator class in 05 does
class Operator:
  
	def __init__(self, name, precond, state_transf):
		self.name = name
		self.precond = precond
		self.state_transf = state_transf

	def is_applicable(self, state):
		return self.precond(state)

	def apply(self, state):
		return self.state_transf(state)

# Takes a room num from 0 to 8 and a side for the door to be on, [N, S, E, W]
# Optional newDoor parameter which allows you to pass which door the walls will point to.
# Is default set to the creation of a new door.
def add_door_to_room(room_num, side, state, newDoor = Door()):
	
	ROOMS = state["Rooms"]
	DOORS = state["Doors"]
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
	DOORS.append(newDoor)
	
def add_door_operator(room_num, side, state):
	
	newState = copy_state(state)
	add_door_to_room(room_num, side, newState)
	return newState
	
def doors_is_valid(side, state):
	
	ROOMS = state["Rooms"]
	DOORS = state["Doors"]
	room_num = state["Selected"]
	
	if side == 'N':
		north_room = room_num - 3
		if (north_room < 0):
			return False
		elif (ROOMS[room_num].walls['N'].door is not None or ROOMS[north_room].walls['S'].door is not None):
			return False
		else:
			return True
	elif side == 'S':
		south_room = room_num + 3
		if (south_room > 8):
			return False
		elif (ROOMS[room_num].walls['S'].door is not None or ROOMS[south_room].walls['N'].door is not None):
			return False
		else:
			return True
	elif side == 'E':
		east_room = room_num + 1
		if (room_num + 1) % 3 is 0:
			return False
		elif (ROOMS[room_num].walls['E'].door is not None or ROOMS[east_room].walls['W'].door is not None): 	
			return False
		else:
			return True
	elif side == 'W':
		west_room = room_num - 1
		if (room_num + 1) % 3 is 1:
			return False
		elif (ROOMS[room_num].walls['W'].door is not None or ROOMS[west_room].walls['E'].door is not None):	
			return False
		else: 
			return True
	else:
		return False
	
# takes a room num from 0 to 8 and prompts the user for a url for the wallpaper
def add_wallpaper_to_room(room_num, state):
	url = prompt("Enter a complete URL for a wallpaper. Say 'cancel' to cancel.", "wall.jpg")
	if(url == "cancel"):
		
		newState = copy_state(state)
		
	elif(url_is_valid(url)):	
	
		newState = copy_state(state)
		ROOMS = newState["Rooms"]
		picked = ROOMS[room_num]
		for loc in picked.walls:
			picked.walls[loc].wallpaper.url = url
	
	else:
	
		alert("URL was not valid. Try again.")
		return add_wallpaper_to_room(room_num, state)
	
	return newState
	
def url_is_valid(url):	
	try:
		fileContents = open(url)
		return True
	except OSError:
		return False
	
def change_selection(room_num, state):
	newState = copy_state(state)
	newState["Selected"] = room_num
	return newState
	
def change_role(role, state):
	newState = copy_state(state)
	newState['Role'] = role
	return newState

def darkenCJS(state):
	newState = copy_state(state)
	#CamanComms = JSConstructor(window.CamanComms)
	#CamanComms("roleCanvas").darkenImg()
	
	CAMANCOMMS = window.CamanComms
	alert(CAMANCOMMS)
	
	
	
	'''camanComm = JSConstructor(window.CamanComms)
	window.console.log("camanComm constructor: ")
	window.console.log(camanComm)
	translator = camanComm("#roleCanvas")
	window.console.log("translator with id: ")
	window.console.log(translator)
	translator.command("function(){this.brightness(-20).render();}")'''
	return newState
	
#</COMMON_CODE>		
	
print("Hello from PRIMEDesigner15.py (after COMMON_CODE)")

#<OPERATORS>
def set_operators(state):
#Method that can be called to set the Operators 
#of the current Role given the current State
	role_operators =\
		[Operator("Change Role to " + role + ".",
			lambda state: state['Role'] is not role,
			lambda state: change_role(role, state))
		for role in ["Architect", "Image Puzzle", "Music Puzzle", "Rules"]] 	
			
	if (state['Role'] == "Architect"):
		selection_operators =\
			[Operator("Switch to room numbered " + str(num + 1) + " for editing.",
				lambda state: num is not state["Selected"],
				lambda state: change_selection(num, state))
			for num in range(9)]

		door_operators =\
			[Operator("Add door to current room on " + cardinal + " wall.",
				lambda state: doors_is_valid(cardinal, state),
				lambda state: add_door_operator(state["Selected"], cardinal, state))
			for cardinal in ['N', 'S', 'E', 'W']]		

		wallpaper_operators =\
			Operator("Add wallpaper to current room.",
				lambda state: True,
				lambda state: add_wallpaper_to_room(state["Selected"], state))
					
		OPERATORS = selection_operators	+ door_operators + wallpaper_operators + role_operators
		
	elif(state['Role'] == "Image Puzzle"):
		darken_test =\
			Operator("Darken the image.",
				lambda state: True,
				lambda state: darkenCJS(state))
				
		OPERATORS = [darken_test] # + role_operators
		
	elif(state['Role'] == "Music Puzzle"):
		OPERATORS = role_operators
	elif(state['Role'] == "Rules"):
		OPERATORS = role_operators
	else:
		alert("unsupported role")
	
	return OPERATORS
#</OPERATORS>
	
#<INITIAL_STATE> The game is a list of 9 rooms stored a list.
INITIAL_STATE = {}
INITIAL_STATE['Rooms'] = []
INITIAL_STATE['Doors'] = []
INITIAL_STATE['Selected'] = 0
INITIAL_STATE['Role'] = "Image Puzzle"

# Create 9 rooms, add them to the list.
for j in range(3):
	for i in range(3):
		INITIAL_STATE['Rooms'].append( Room(i, j, i + 1, j + 1) )	
# Now initialize operators.
OPERATORS = set_operators(INITIAL_STATE)		
#</INITIAL_STATE>

if "BRYTHON" in globals():
 from PRIMEDesigner15VisForBrython import set_up_gui as set_up_user_interface
 from PRIMEDesigner15VisForBrython import render_state_svg_graphics as render_state


