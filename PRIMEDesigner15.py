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

#def copy_state(s):
	# Performs an appropriately deep copy of a state,
	# for use by operators in creating new states.

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
		self.walls['N'] = (Wall(x1 ,y1 ,x2 ,y1, 'N')) #top 
		self.walls['S'] = (Wall(x1 ,y2 ,x2 ,y2, 'S')) #bottom
			
		# Vertical walls.
		self.walls['W'] = (Wall(x1 ,y1 ,x1 ,y2, 'W')) #left
		self.walls['E'] = (Wall(x2 ,y1 ,x2 ,y2, 'E')) #right
	
		# Possible ambient soundtrack.
		self.music = None
		
""" A wall could contain a door or a wallpaper """	
class Wall:

	def __init__(self, x1, y1, x2, y2, loc): 
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.loc = loc
		# Start a wall of with a door, TEMPORARY FOR DEVELOPEMENT
		self.door = Door()
		
		# Possible puzzle
		self.puzzle = None
		
		# Creates a wallpaper, default picture is wall.jpg
		self.wallpaper = Wallpaper()
		
# Default url is wall.jpg
# Test url is stripes.jpg for transformation testing.
class Wallpaper:
	
	def __init__(self, url = "wall.jpg"):
		self.url = url
	
class Door:
	
	# Default open state should be FALSE, true IS FOR DEVELOPEMENT
	def __init__(self, isOpen = True, url="door.jpg"):
		self.isOpen = isOpen
		self.url = url
		
	# Closes the door if it is open.
	# Opens the door if it is closed.
	def open_or_close(self):
		self.isOpen = not isOpen

class Puzzle:
	
	def __init__(self):
	
	def copy(self):

class Music:

	def __init__(self):
	
	def copy(self):
	
		
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

# takes a room num from 0 to 8 and a side for the door to be on, [N, S, E, W]
def add_door_to_room(room_num, side):
	global DOORS, ROOMS
	newDoor = Door(isOpen = False) # Doors are initialized as closed
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

# takes a room num from 0 to 8 and a url for a wallpaper
def add_wallpaper_to_room(room_num, url):
	global ROOMS
	picked = ROOMS[room_num]
	for loc in picked.walls:
		picked.walls[loc].wallpaper = Wallpaper(url)

def change_selection(state, room_num):
	newState = copy_state(state)
	newState["Selected"] = newState['Rooms'][room_num]
	return newState
#</COMMON_CODE>		
	
print("Hello from PRIMEDesigner15.py (after COMMON_CODE)")
	
#<INITIAL_STATE> The game is a list of 9 rooms stored a list.
INITIAL_STATE = {}
ROOMS = []
DOORS = []
Selected = 0
# Create 9 rooms, add them to the list.
for j in range(3):
	for i in range(3):
		ROOMS.append( Room(i, j, i + 1, j + 1) )
INITIAL_STATE['Rooms'] = ROOMS
INITIAL_STATE['Doors'] = DOORS
INITIAL_STATE['Selected'] = selected		
#</INITIAL_STATE>

#It seems to me like the way this worked before is that in COMMON_CODE were all
#the functions for operators, and then in OPERATORS it is determined which are
#valid to use in the current state. We should double check with Steve but
#I'll be running with this interpretation. 
#<OPERATORS>
selection_operators =\
	[Operator("Switch to room numbered " + num + 1 + " for editing",
			lambda state: num is not state["Selected"]
			lambda state: change_selection(state, num)
	for num in range(9)]
	
OPERATORS = selection_operators
#</OPERATORS>

if "BRYTHON" in globals():
 from PRIMEDesigner15VisForBrython import set_up_gui as set_up_user_interface
 from PRIMEDesigner15VisForBrython import render_state_svg_graphics as render_state


