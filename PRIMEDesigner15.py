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

#</INITIAL_STATE>

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
		self.walls = [];
		
		# Horizontal walls.
		self.walls.append(Wall(x1 ,y1 ,x2 ,y2 )) 
		self.walls.append(Wall(x1 ,y2 ,x2 ,y2 ))
		
		# Vertical walls.
		self.walls.append(Wall(x1 ,y1 ,x1 ,y2 ))
		self.walls.append(Wall(x2 ,y1 ,x2 ,y2 ))
	
		# Possible ambient soundtrack.
		self.music = null
		
""" A wall could contain a door or a wallpaper """	
class Wall:

	def __init__(self, x1, y1, x2, y2): 
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.door = null
		
		# Possible puzzle
		self.puzzle = null
		
		# Possible wallpaper.
		self.wallpaper = null
		
class WallPaper:
	
	def __init__(self, x1, y1, x2, y2):
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.url = null

		
#<INITIAL_STATE> The game is a list of 9 rooms stored a list.
INITIAL_STATE = []

# Create 9 rooms, add them to the list.
<<<<<<< HEAD
for i in range(3):
	for j in range(3):
		INITIAL_STATE.append( Room(i,i,j,j) )
#</INITIAL_STATE>

#<OPERATORS>
class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)
	
# Operators is temporarily an empty list.
OPERATORS = []
#</OPERATORS>

if "BRYTHON" in globals():
 from PRIMEDesigner15VisForBrython import set_up_gui as set_up_user_interface
 from PRIMEDesigner15VisForBrython import render_state_svg_graphics as render_state

=======
for j in range(3):
	for i in range(3):
		INITIAL_STATE.append( Room(i, j, i + 1, j + 1) )
# rooms: 
# (0,0),(1,1);(1,0),(2,1);(2,0),(3,1);
# (0,1),(1,2);(1,1),(2,2);(2,1),(3,2);
# (0,2),(1,3);(1,2),(2,3);(2,2),(3,3);
>>>>>>> origin/master
