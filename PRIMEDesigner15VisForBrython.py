'''PRIMEDesignerVisForBrython.py

Set up a GUI and handle updates and events during a run of
the PRIMEDesigner template in the Brython environment.
'''

from browser import doc, html, alert, svg

gui = None
ROOM_SIZE = 100
GAME_WIDTH = ROOM_SIZE * 9
GAME_HEIGHT = ROOM_SIZE * 9

print("Hello from PRIMEDesignerVisForBrython!  Starting to process it.")

LINE_WIDTH = 10
def set_up_gui(opselectdiv, statuslinediv):
	print("Entering set_up_gui in PRIMEDesignerVisForBrython.")
	global gui
	gui = html.DIV(Id="thegui")
	gui <= opselectdiv
	gui <= statuslinediv
	doc <= gui
	print("Leaving set_up_gui in PRIMEDesignerVisForBrython.")

def render_state_svg_graphics(state):
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
	global LINE_WIDTH, gui
	# Maps points to Div
	(X1,Y1) = mapCoordsToDiv(wallpaper.x1,wallpaper.y1)
	(X2,Y2) = mapCoordsToDiv(wallpaper.x2,wallpaper.y2)
	(X3,Y3) = mapCoordsToDiv(x3,y3)
	(X4,Y4) = mapCoordsToDiv(x4,y4)
	
	# Create string of points for svg_polygon
	Points =\ 
			X1 + "," + Y1 + " " + X2 + "," + Y2 + " " +
			X3 + "," + Y3 + " " + X4 + "," + Y4
	
	# Create div
	wallPaperDiv = svg_polygon(fill="black",stroke="red",stroke_width=LINE_WIDTH,
					points=Points)
					
	# Append div to gui
	gui <= wallPaperDiv
	

def mapCoordsToDIV(x, y):
	'''Convert x coordinate from the range [0.0, 1.0] to
     the range [MARGIN, PAINTING_WIDTH - MARGIN], and
     the y coordinate to the range [MARGIN, PAINTING_HEIGHT - MARGIN].'''
  global GAME_WIDTH, GAME_HEIGHT
  newX = int( (x * GAME_WIDTH)/3) )
  newY = int( (y * GAME_HEIGHT/3) )
  return (newX, newY)
	
	
	
	