'''PRIMEDesignerVisForBrython.py

Set up a GUI and handle updates and events during a run of
the PRIMEDesigner template in the Brython environment.
'''

from browser import doc, html, alert, svg

gui = None
#is this saying that all of these are now 'None'?
board = None
statusline = None
opselect = None
APANEL = None
MARGIN = 20
ROOM_SIZE = 100
GAME_WIDTH = ROOM_SIZE * 3
GAME_HEIGHT = ROOM_SIZE * 3

LAST_STATE = None # cache of current state for use in 
				#refresh of display after selection hiding button click.

print("Hello from PRIMEDesignerVisForBrython!  Starting to process it.")

LINE_WIDTH = 15
def set_up_gui(opselectdiv, statuslinediv):
	print("Entering set_up_gui in PRIMEDesignerVisForBrython.")
	global gui
	gui = html.DIV(Id = "thegui")
	set_up_board_svg_graphics()
	alert("SVG stuff should now be set up.")
	gui <= opselectdiv
	gui <= statuslinediv
	doc <= gui
	print("Leaving set_up_gui in PRIMEDesignerVisForBrython.")

def set_up_board_svg_graphics():
	#SHOW_SELECTION_Button isn't initialized before this call.
	#Does this mean that with the global keyword, you can either 
	#refer to a global variable or initialize a new one?
	global APANEL, SHOW_SELECTION_Button, board
	boarddiv = html.DIV(Id = "boarddivid", style = {"backgroundColor":"#CCFFCC"})
	boarddiv <= html.I("Puzzle state:")
	#what is APANEL intended to be
	APANEL = svg.g(Id = "panel")
	board = svg.svg(Id = "svgboard", 
					style = {"width":GAME_WIDTH, "height":GAME_HEIGHT,
							"backgroundColor":"#AAAABB"})
	board <= APANEL		
	boarddiv <= board
	# Put in a button for controlling whether or not the currently selected box is highlighted.
	SHOW_SELECTION_Button = html.BUTTON("Hide/Show selected box", Id="HideOrShowSelected")
	SHOW_SELECTION_Button.bind('click', hideOrShowSelection)
	boarddiv <= SHOW_SELECTION_Button
	gui <= boarddiv

SHOWING_SELECTION = True
def hideOrShowSelection(event):
  global SHOWING_SELECTION, SHOW_SELECTION_Button
  SHOWING_SELECTION = not SHOWING_SELECTION
  if SHOWING_SELECTION:
    SHOW_SELECTION_Button.text = "Turn off highlighting of the selected box."    
  else:
    SHOW_SELECTION_Button.text = "Enable highlighting of the selected box."    
  render_state_svg_graphics(LAST_STATE)
		
# draws the game
def render_state_svg_graphics(state):
	for room in state['Rooms']:
		drawRoom(room)
		
# draws a room.		
def drawRoom(room):
	# thickness of a room's walls.
	THICKNESS = .2
	
	# draws north wall
	wall = room.walls['N']
	x3 = wall.x2 - THICKNESS/pow(2,1/2)
	y3 = wall.y1 + THICKNESS/pow(2,1/2)
	x4 = wall.x1 + THICKNESS/pow(2,1/2)
	y4 = y3
	drawWall(wall,x3,y3,x4,y4)
	
	# draws south wall
	wall = room.walls['S']
	x3 = wall.x2 - THICKNESS/pow(2,1/2)
	y3 = wall.y1 - THICKNESS/pow(2,1/2)
	x4 = wall.x1 + THICKNESS/pow(2,1/2)
	y4 = y3
	drawWall(wall,x3,y3,x4,y4)
	
	# draws west wall
	wall = room.walls['W']
	x3 = wall.x2 + THICKNESS/pow(2,1/2)
	y3 = wall.y2 - THICKNESS/pow(2,1/2)
	x4 = x3
	y4 = wall.y1 + THICKNESS/pow(2,1/2)
	drawWall(wall,x3,y3,x4,y4)
	
	# draws east wall
	wall = room.walls['E']
	x3 = wall.x2 - THICKNESS/pow(2,1/2)
	y3 = wall.y2 - THICKNESS/pow(2,1/2)
	x4 = x3
	y4 = wall.y1 + THICKNESS/pow(2,1/2)
	drawWall(wall,x3,y3,x4,y4)
		
# draws a wall, requires 2 more points to form trapezoidal 3d shape.
# Temporary optional color for walls.
def drawWall(wall,x3,y3,x4,y4):
	drawWallpaper(wall,x3,y3,x4,y4)
	#if not (wall.door is None):
	drawDoor(wall,x3,y3,x4,y4)
	
# draws a wallpaper, requires 2 more points to form trapezoidal 3d shape.	
def drawWallpaper(wall,x3,y3,x4,y4):
	global LINE_WIDTH, APANEL
	
	# Create pattern for image representation.
	defs = svg.defs()
	pattern = svg.pattern(id="image",height="100",width = "50")
	img = svg.image(xlink_href=wall.wallpaper.url, x="0",y="0", width="100", height="100")
	
	# Append
	pattern <= img
	defs <= pattern
	APANEL <= defs
	
	# TODO: Tranform pattern based on wall orientation.
	# The thing below doesn't work for some reason...
	#transform = svg.animateTransform(attributeType = "XML", attributeName="transform", type="rotate",From="0,200,200",to="360,200,200",begin="0s", dur="1s", repeatCount="indefinite")

	WallpaperDiv = create_polygon(wall.x1,wall.y1,wall.x2,wall.y2,x3,y3,x4,y4,fill="url(#image)" )
					
	# Append polygon to svg panel
	APANEL <= WallpaperDiv

# 	
def drawDoor(wall,fx3,fy3,fx4,fy4):

	DOOR_SIZE = (1/3)

	# map coords independently of object values and reassign
	(fx1,fy1,fx2,fy2) = (wall.x1,wall.y1,wall.x2,wall.y2)
	
	if (wall.loc == 'E' or wall.loc == 'W'):
		fy1 += DOOR_SIZE
		fy2 -= DOOR_SIZE
		fy3 -= DOOR_SIZE * (4/5)
		fy4 += DOOR_SIZE * (4/5)
		
	if (wall.loc == 'N' or wall.loc == 'S'):
		fx1 += DOOR_SIZE
		fx2 -= DOOR_SIZE
		fx3 -= DOOR_SIZE * (4/5)
		fx4 += DOOR_SIZE * (4/5)
	
	(dx1,dy1,dx2,dy2,dx3,dy3,dx4,dy4) = (fx1,fy1,fx2,fy2,fx3,fy3,fx4,fy4)
	
	if(wall.loc == 'E'):
		if(wall.door.isOpen):
			dx1 = fx1
			dy1 = fy1
			dx2 = fx4 - DOOR_SIZE * (1/2)
			dy2 = fy1
			dx3 = dx2
			dy3 = fy4
			dx4 = fx4
			dy4 = fy4
		else:
			dx1 = fx1
			dy1 = fy1
			dx2 = fx2 - .05 
			dy2 = fy2
			dx3 = fx3 - .05
			dy3 = fy3
			dx4 = fx4
			dy4 = fy4
	if(wall.loc == 'W'):
		if(not wall.door.isOpen):
			dx1 = fx1
			dy1 = fy2
			dx2 = fx4 + DOOR_SIZE * (1/2)
			dy2 = fy2
			dx3 = dx2
			dy3 = fy3
			dx4 = fx4
			dy4 = fy3
		else:
			dx1 = fx1
			dy1 = fy1
			dx2 = fx2 + .05 
			dy3 = fy2
			dx3 = fx3 + .05
			dy3 = fy3
			dx4 = fx4
			dy4 = fy4
	# TODO: add West and East door representations.
		
	
	
	frameDiv = create_polygon(fx1,fy1,fx2,fy2,fx3,fy3,fx4,fy4, fill = "black")
	doorDiv = create_polygon(dx1,dy1,dx2,dy2,dx3,dy3,dx4,dy4, fill = "brown")				
	# Append polygon to svg panel
	APANEL <= frameDiv
	APANEL <= doorDiv

# returns a div representing a polygon at the given 4 points.
def create_polygon(x1,y1,x2,y2,x3,y3,x4,y4, fill = "black"):
	
	# Maps points to Div
	(X1,Y1) = mapCoordsToDIV(x1,y1)
	(X2,Y2) = mapCoordsToDIV(x2,y2)
	(X3,Y3) = mapCoordsToDIV(x3,y3)
	(X4,Y4) = mapCoordsToDIV(x4,y4)
	
	# Create string of points for svg_polygon
	Points = str(X1) + "," + str(Y1) + " " + str(X2) + "," + str(Y2) + " " + str(X3) + "," + str(Y3) + " " + str(X4) + "," + str(Y4)
	
	# Create polygon
	poly = svg.polygon(fill= fill,stroke="white",stroke_width=LINE_WIDTH,
					points=Points)
					
	# Append polygon to svg panel
	return poly
	
# Convert x coordinate from the range [0.0, 3.0] to 
# the range [0,GAME_WIDTH] and the y coordinate to the
# range [0,GAME_HEIGHT].
def mapCoordsToDIV(x, y):
	global GAME_WIDTH, GAME_HEIGHT
	newX = int( (x * GAME_WIDTH)/3) 
	newY = int( (y * GAME_HEIGHT)/3) 
	return (newX, newY)

	
	
	
	