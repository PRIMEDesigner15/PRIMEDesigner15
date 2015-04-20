'''PRIMEDesignerVisForBrython.py

Set up a GUI and handle updates and events during a run of
the PRIMEDesigner template in the Brython environment.
'''

from browser import doc, html, alert, svg

ROOM_SIZE = 100
GAME_SIZE = ROOM_SIZE * 9
MARGIN = 20

print("Hello from PRIMEDesignerVisForBrython!  Starting to process it.")

LINE_WIDTH = 10
def set_up_gui(opselectdiv, statuslinediv):
	print("Entering set_up_gui in PRIMEDesignerVisForBrython.")
	global gui
	gui = html.DIV(Id="thegui")
	#setupboard
	gui <= opselectdiv
	gui <= statuslinediv
	doc <= gui
	print("Leaving set_up_gui in PRIMEDesignerVisForBrython.")

def draw(state):
	for room in state:
		draw(room)
		
# draws a room.		
def draw(room):
	# thickness of a rooms walls.
	def THICKNESS = .2
	
	# draws top horizontal wall
	def wall = room.walls[0]
	def x3 = wall.x1 + THICKNESS/math.sqrt(2)
	def y3 = wall.y1 + THICKNESS/math.sqrt(2)
	def x4 = wall.x2 - THICKNESS/math.sqrt(2)
	def y4 = wall.y3
	draw(wall,x3,y3,x4,y4)
	
	# draws bottom horizontal wall
	wall = room.walls[1]
	def x3 = wallpaper.x1 + THICKNESS/math.sqrt(2)
	def y3 = wallpaper.y1 - THICKNESS/math.sqrt(2)
	def x4 = wall.x2 - THICKNESS/math.sqrt(2)
	def y4 = wall.y3
	draw(wall,x3,y3,x4,y4)
	
	# draws left vertical wall
	wall = room.walls[2]
	def x3 = wallpaper.x1 + THICKNESS/math.sqrt(2)
	def y3 = wallpaper.y1 + THICKNESS/math.sqrt(2)
	def x4 = wall.x3
	def y3 = wallpaper.y1 - THICKNESS/math.sqrt(2)
	draw(wall,x3,y3,x4,y4)
	
	# draws right vertical wall
	wall = room.walls[3]
	def x3 = wallpaper.x1 - THICKNESS/math.sqrt(2)
	def y3 = wallpaper.y1 + THICKNESS/math.sqrt(2)
	def x4 = wall.x3
	def y3 = wallpaper.y1 - THICKNESS/math.sqrt(2)
	draw(wall,x3,y3,x4,y4)
		
# draws a wall, requires 2 more points to form trapezoidal 3d shape.
def draw(wall,x3,y3,x4,y4):
	draw(wall.wallpaper,x3,y3,x4,y4)

# draws a wallpaper, requires 2 more points to form trapezoidal 3d shape.	
def draw(wallpaper,x3,y3,x4,y4):
	# Create 2 more points to form a trapezoidal false 3d shape.
	
	
	
	
	