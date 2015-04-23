'''PRIMEDesignerVisForBrython.py

Set up a GUI and handle updates and events during a run of
the PRIMEDesigner template in the Brython environment.
'''

from browser import doc, html, alert, svg

gui = None
#is this saying that all of these are now 'None'?
board=statusline=opselect=None
APANEL = None
MARGIN = 20
ROOM_SIZE = 100
GAME_WIDTH = ROOM_SIZE * 3
GAME_HEIGHT = ROOM_SIZE * 3

LAST_STATE = None # cache of current state for use in 
				#refresh of display after selection hiding button click.

print("Hello from PRIMEDesignerVisForBrython!  Starting to process it.")

LINE_WIDTH = 10
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
		
def render_state_svg_graphics(state):
	for room in state.ROOMS:
		drawRoom(room)
		
# draws a room.		
def drawRoom(room):
	# thickness of a room's walls.
	THICKNESS = .2
	
	# draws north wall
	wall = room.walls['N']
	x3 = wall.x1 + THICKNESS/pow(2,1/2)
	y3 = wall.y1 + THICKNESS/pow(2,1/2)
	x4 = wall.x2 - THICKNESS/pow(2,1/2)
	y4 = y3
	drawWall(wall,x3,y3,x4,y4)
	
	# draws south wall
	wall = room.walls['S']
	x3 = wall.x1 + THICKNESS/pow(2,1/2)
	y3 = wall.y1 - THICKNESS/pow(2,1/2)
	x4 = wall.x2 - THICKNESS/pow(2,1/2)
	y4 = y3
	drawWall(wall,x3,y3,x4,y4)
	
	# draws west wall
	wall = room.walls['W']
	x3 = wall.x1 + THICKNESS/pow(2,1/2)
	y3 = wall.y1 + THICKNESS/pow(2,1/2)
	x4 = x3
	y3 = wall.y1 - THICKNESS/pow(2,1/2)
	drawWall(wall,x3,y3,x4,y4)
	
	# draws east wall
	wall = room.walls['E']
	x3 = wall.x1 - THICKNESS/pow(2,1/2)
	y3 = wall.y1 + THICKNESS/pow(2,1/2)
	x4 = x3
	y3 = wall.y1 - THICKNESS/pow(2,1/2)
	drawWall(wall,x3,y3,x4,y4)
		
# draws a wall, requires 2 more points to form trapezoidal 3d shape.
def drawWall(wall,x3,y3,x4,y4):
	drawWallpaper(wall,x3,y3,x4,y4)

	
# draws a wallpaper, requires 2 more points to form trapezoidal 3d shape.	
def drawWallpaper(wall,x3,y3,x4,y4):
	global LINE_WIDTH, gui
	# Maps points to Div
	(X1,Y1) = mapCoordsToDIV(wall.x1,wall.y1)
	(X2,Y2) = mapCoordsToDIV(wall.x2,wall.y2)
	(X3,Y3) = mapCoordsToDIV(x3,y3)
	(X4,Y4) = mapCoordsToDIV(x4,y4)
	
	# Create string of points for svg_polygon
	Points = str(X1) + "," + str(Y1) + " " + str(X2) + "," + str(Y2) + " " + str(X3) + "," + str(Y3) + " " + str(X4) + "," + str(Y4)
	
	# Create div
	#WallpaperDiv = svg_polygon(fill="black",stroke="red",stroke_width=LINE_WIDTH,
	#				points=Points)
	star = svg.polygon(fill="red", stroke="blue", stroke_width="10",
                   points=""" 75,38  90,80  135,80  98,107
                             111,150 75,125  38,150 51,107
                              15,80  60,80""")
				
	
					
	# Append div to gui
	gui <= star
	
def mapCoordsToDIV(x, y):
	'''Convert x coordinate from the range [0.0, 1.0] to
    the range [MARGIN, PAINTING_WIDTH - MARGIN], and
    the y coordinate to the range [MARGIN, PAINTING_HEIGHT - MARGIN].'''
	global GAME_WIDTH, GAME_HEIGHT
	newX = int( (x * GAME_WIDTH)/3) 
	newY = int( (y * GAME_HEIGHT)/3) 
	return (newX, newY)

	
	
	
	