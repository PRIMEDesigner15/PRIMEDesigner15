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

		
