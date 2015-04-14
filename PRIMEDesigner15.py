<<<<<<< HEAD
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

def copy_state(s):
	# Performs an appropriately deep copy of a state,
	# for use by operators in creating new states.

def describe_state(state):
	""" Produces a textual description of a state.
    Might not be needed in normal operation with GUIs."""	
	
class Game
	"""A game that represents the 9 rooms, all the doors, and various
     particular form of graphic art."""
	"""It is important for the myjson.py module that the constructor
     have arguments for each instance component, because it will
     use this __init__ method to reconstruct arbitrary instances
     for the class from json representations in a database.
     Except for the self argument and any keyword arguments,
     there must be a 1-to-1 correspondence between parameters
     in the __init__ method and the actual instance items."""
	 
	 
	 
#<INITIAL_STATE>
INITIAL_STATE =\
	{
	}

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

#</INITIAL_STATE>

print("Hello from Mondrian.py (after INITIAL_STATE)")
=======
	""" A note on the coordinate system used; 
	Each room is of size 1.
	The game is thus of width 3 and height 3"""

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
		
		# 4 walls
		self.walls = [];
		
		# Horizontal walls
		self.walls.append(Wall(x1 ,y1 ,x2 , y1))
		self.walls.append(Wall(x1 ,y2 ,x2 ,y2 ))
		
		# Vertical walls
		self.walls.append(Wall(x1 ,y1 ,x1 ,y2 ))
		self.walls.append(Wall(x2 ,y1 ,x2 ,y2 ))
		
		# Possible puzzle
		self.puzzle = null
	
		# Possible ambient soundtrack
		self.music = null
		
""" A wall could contain a door or a wallpaper """	
class Wall:

	def __init__(self, x1, y1, x2, y2):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.door = null
		self.wallpaper = null
		
#<INITIAL_STATE> The game is a list of 9 rooms stored a list
INITIAL_STATE = []

# Create 9 rooms, add them to the list.
for i in range(3):
	for j in range(3):
		INITIAL_STATE.append( Room(i,i,j,j) )

		
>>>>>>> origin/master
