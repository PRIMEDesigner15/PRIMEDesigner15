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
	#alert("SVG stuff should now be set up.")
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
	global SHOWING_SELECTION
	
	# Clear svg panel
	while APANEL.lastChild:
		APANEL.removeChild(APANEL.lastChild)
	
	
	# Draw all the rooms.
	room_num = 1
	for room in state['Rooms']:
		drawRoom(room,room_num)
		room_num += 1
		
	# Draws a selection box
	if SHOWING_SELECTION:
		
		#Thickness of the selection box 
		THICKNESS = 1.5
		selected_room = state['Rooms'][state['Selected']]
		
		(x1, y1) = mapCoordsToDIV(selected_room.x1, selected_room.y1)
		(x2, y2) = mapCoordsToDIV(selected_room.x2, selected_room.y2)
		
		outline = svg.rect(x = x1, y = y1, width = x2 - x1, height = y2 - y1, fill = "none",
					style = {"stroke": "gold", "stroke-width": THICKNESS})
		APANEL <= outline

# Maps coordinates in range
def mapCoordsToDIV(x, y):
  global GAME_WIDTH, GAME_HEIGHT
  newX = int(MARGIN + x*(GAME_WIDTH - 2*MARGIN))
  newY = int(MARGIN + y*(GAME_HEIGHT - 2*MARGIN))
  return (newX, newY)
		
# draws a room.		
def drawRoom(room,room_num):
	# thickness of a room's walls.
	THICKNESS = .2
	
	#(x3,y3) and (x4,y4) make up the shorter end of the trapezoid
	# draws north wall
	wall = room.walls['N']
	x3 = wall.x2 - THICKNESS/pow(2,1/2)
	y3 = wall.y1 + THICKNESS/pow(2,1/2)
	x4 = wall.x1 + THICKNESS/pow(2,1/2)
	y4 = y3
	drawWall(wall,x3,y3,x4,y4,room_num)
	
	# draws south wall
	wall = room.walls['S']
	x3 = wall.x2 - THICKNESS/pow(2,1/2)
	y3 = wall.y1 - THICKNESS/pow(2,1/2)
	x4 = wall.x1 + THICKNESS/pow(2,1/2)
	y4 = y3
	drawWall(wall,x3,y3,x4,y4,room_num)
	
	# draws west wall
	wall = room.walls['W']
	x3 = wall.x2 + THICKNESS/pow(2,1/2)
	y3 = wall.y2 - THICKNESS/pow(2,1/2)
	x4 = x3
	y4 = wall.y1 + THICKNESS/pow(2,1/2)
	drawWall(wall,x3,y3,x4,y4,room_num)
	
	# draws east wall
	wall = room.walls['E']
	x3 = wall.x2 - THICKNESS/pow(2,1/2)
	y3 = wall.y2 - THICKNESS/pow(2,1/2)
	x4 = x3
	y4 = wall.y1 + THICKNESS/pow(2,1/2)
	drawWall(wall,x3,y3,x4,y4,room_num)
		
# draws a wall, requires 2 more points to form trapezoidal 3d shape.
# Temporary optional color for walls.
def drawWall(wall,x3,y3,x4,y4,room_num):
	drawWallpaper(wall,x3,y3,x4,y4,room_num)
	if (wall.door is not None):
		drawDoor(wall,x3,y3,x4,y4)
	
# draws a wallpaper, requires 2 more points to form trapezoidal 3d shape.	
def drawWallpaper(wall,x3,y3,x4,y4,room_num):
	global LINE_WIDTH, APANEL

	#alert("wall loc is = " + wall.loc)
	if (wall.loc == 'S'):
		transform = "rotate(180, 50, 50)"
	elif (wall.loc == 'E'):
		#alert("East walls triggered")
		transform = "rotate(90, 50, 50)"
	elif (wall.loc == 'W'):
		transform = "rotate(270, 50, 50)"
	else:
		transform = "rotate(0)"
	
	# Create a pattern for image represntation.
	pattern = svg.pattern(id="wallpaper" + str(room_num) + wall.loc,height="100",width = "50")
	img = svg.image(xlink_href=wall.wallpaper.url, x="0",y="0", width="100", height="100", transform = transform)
	
	# Append
	pattern <= img
	APANEL <= pattern
	
	WallpaperDiv = create_polygon(wall.x1, wall.y1, wall.x2, wall.y2, x3, y3, x4, y4,
								  fill="url(#wallpaper" + str(room_num) + wall.loc  + ")", id = wall.loc)
					
	# Append polygon to svg panel
	APANEL <= WallpaperDiv

# Draws a door frame on a wall with the given wall coordinates.
# and then draws a door on that frame.
def drawDoor(wall,x3,y3,x4,y4):

	# Caution: Sensitive variable, keep it around 3 for a good sized door.
	DOOR_SIZE = 1

	# map (f)rame coords to wall coords before translation
	(fx1,fy1,fx2,fy2,fx3,fy3,fx4,fy4) = (wall.x1,wall.y1,wall.x2,wall.y2,x3,y3,x4,y4)
	
	# fit the door (f)rame into a smaller trapezoid
	if (wall.loc == 'E' or wall.loc == 'W'):
		fy1 += 1/DOOR_SIZE * (1/3)
		fy2 -= 1/DOOR_SIZE * (1/3)
		fy3 -= 1/DOOR_SIZE * (4/15)
		fy4 += 1/DOOR_SIZE * (4/15)
		
	elif (wall.loc == 'N' or wall.loc == 'S'):
		fx1 += 1/DOOR_SIZE * (1/3)
		fx2 -= 1/DOOR_SIZE * (1/3)
		fx3 -= 1/DOOR_SIZE * (4/15)
		fx4 += 1/DOOR_SIZE * (4/15)
	else:
		alert("drawDoor wall location check broke")
	# Map default (d)oor coords to (f)rame coords. 
	(dx1,dy1,dx2,dy2,dx3,dy3,dx4,dy4) = (fx1,fy1,fx2,fy2,fx3,fy3,fx4,fy4)
	
	# Map (d)oor coordinates based off (f)rame's
	if(wall.door.isOpen):
		if(wall.loc == 'E'):
			dx2 = fx4 - DOOR_SIZE * (1/5)
			dy2 = fy1
			dx3 = dx2
			dy3 = fy4
		elif(wall.loc == 'W'):
			dy1 = fy2
			dx2 = fx4 + DOOR_SIZE * (1/5)
			dx3 = dx2
			dy4 = fy3
		elif(wall.loc == 'N'):
			dx2 = fx1
			dy2 = fy1 + DOOR_SIZE * (2/5)
			dx3 = fx4 
			dy3 = dy2
		elif(wall.loc == 'S'):
			dx1 = fx2
			dy1 = fy2
			dy2 = fy2 - DOOR_SIZE * (2/5)
			dy3 = dy2
			dx4 = fx3
		else:
			alert("wall door isOpen location broke")
	# Create frame and door polygons
	frameDiv = create_polygon(fx1,fy1,fx2,fy2,fx3,fy3,fx4,fy4, fill = "black")
	doorDiv = create_polygon(dx1,dy1,dx2,dy2,dx3,dy3,dx4,dy4, fill = "url(#door)") #fill = "#c9731e"	
	
	defs = svg.defs()
	pattern = svg.pattern(id="door",height="100",width = "100")
	img = svg.image(xlink_href=wall.door.url, x="0",y="0", height="100", width="100")
	pattern <= img
	defs <= pattern
		
	# Append polygon to svg panel
	APANEL <= defs
	APANEL <= frameDiv
	APANEL <= doorDiv

# returns an svg polygon at the given 4 points.
def create_polygon(x1,y1,x2,y2,x3,y3,x4,y4, fill = "black", stroke = "black", transform = "rotate(0)", id = "polygon"):
	
	# Maps points to Div
	(X1,Y1) = mapCoordsToDIV(x1,y1)
	(X2,Y2) = mapCoordsToDIV(x2,y2)
	(X3,Y3) = mapCoordsToDIV(x3,y3)
	(X4,Y4) = mapCoordsToDIV(x4,y4)
	
	# Create string of points for svg_polygon
	Points = str(X1) + "," + str(Y1) + " " + str(X2) + "," + str(Y2) + " " + str(X3) + "," + str(Y3) + " " + str(X4) + "," + str(Y4)
	
	# Create polygon
	poly = svg.polygon(id=id,style = {"fill" : fill},stroke=stroke,stroke_width=LINE_WIDTH,
					points=Points, transform=transform)
					
	# return polygon
	return poly
	
# Convert x coordinate from the range [0.0, 3.0] to 
# the range [0,GAME_WIDTH] and the y coordinate to the
# range [0,GAME_HEIGHT].
def mapCoordsToDIV(x, y):
	global GAME_WIDTH, GAME_HEIGHT
	newX = int( (x * GAME_WIDTH)/3) 
	newY = int( (y * GAME_HEIGHT)/3) 
	return (newX, newY)

	
	
	
	