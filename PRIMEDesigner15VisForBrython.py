'''PRIMEDesignerVisForBrython.py

Set up a GUI and handle updates and events during a run of
the PRIMEDesigner template in the Brython environment.
'''

from browser import window, document, html, alert, svg, console
from javascript import JSConstructor


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


CamanCommConstructor = JSConstructor(window.CamanComms)
camanTranslator = CamanCommConstructor("#roleCanvas", "none.jpg")

camanTranslator.CamanFunction("this.render()")
# Store the selected puzzle to reset CamanJS when it changes
selected_puzzle = -1

#The canvas and its context will go here when initialized for manipulation
roleCanvas = None
ctx = None

LAST_STATE = None # cache of current state for use in 
				#refresh of display after selection hiding button click.

print("Hello from PRIMEDesignerVisForBrython!  Starting to process it.")
LINE_WIDTH = 4
def set_up_gui(opselectdiv, statuslinediv):
	print("Entering set_up_gui in PRIMEDesignerVisForBrython.")
	global gui
	gui = html.DIV(Id = "thegui")
	set_up_board_svg_graphics()
	gui <= opselectdiv
	gui <= statuslinediv
	document <= gui
	print("Leaving set_up_gui in PRIMEDesignerVisForBrython.")

def set_up_board_svg_graphics():
	#SHOW_SELECTION_Button isn't initialized before this call.
	#Does this mean that with the global keyword, you can either 
	#refer to a global variable or initialize a new one?
	boarddiv = html.DIV(Id = "boarddivid", style = {"backgroundColor":"#CCFFCC"})
	boarddiv <= html.I("Puzzle state:")
	#what is APANEL intended to be
	
	global ctx, roleCanvas
	roleCanvas = html.CANVAS(id = "roleCanvas", width = GAME_WIDTH, height = GAME_HEIGHT)
	ctx = roleCanvas.getContext("2d")
	
	global APANEL, board
	board = svg.svg(Id = "svgboard", 
					style = {"width":GAME_WIDTH, "height":GAME_HEIGHT,
							"backgroundColor":"#AAAABB",})
	board.elt.style.display = "none"
	APANEL = svg.g(Id = "panel")
	
	board <= APANEL	
	boarddiv <= board
	boarddiv <= roleCanvas
	gui <= boarddiv
		
# draws the game
def render_state_svg_graphics(state):
	global roleCanvas, ctx, APANEL, selected_puzzle
	
	# Clear svg panel
	while APANEL.lastChild:
		APANEL.removeChild(APANEL.lastChild)
	
	# Clear the roleCanvas
	ctx.clearRect(0,0, GAME_WIDTH, GAME_HEIGHT)
	#alert("canvas was cleared")

	alert(state['Role'])
	if(state['Role'] == "Architect"):
		prepareSVG()
		
		# Draw all the rooms.
		room_num = 1
		for room in state['Rooms']:
			drawRoom(room,room_num)
			room_num += 1
			
		THICKNESS = 1.5
		selected_room = state['Rooms'][state['Selected_Room']]
			
		(x1, y1) = mapCoordsToDIV(selected_room.x1, selected_room.y1)
		(x2, y2) = mapCoordsToDIV(selected_room.x2, selected_room.y2)
			
		outline = svg.rect(x = x1, y = y1, width = x2 - x1, height = y2 - y1, fill = "none",
						style = {"stroke": "gold", "stroke-width": THICKNESS})
		APANEL <= outline
	elif(state['Role'] == "Image Puzzle"):
		prepareCanvas()	
		if(state["Selected_Puzzle"] != selected_puzzle):
			camanTranslator.resetCamanImage()
		if(state["Selected_Puzzle"] != -1):
			puzzle = state["Puzzles"][state["Selected_Puzzle"]]
			camanTranslator.setURL(puzzle.url)
			selected_puzzle = state["Selected_Puzzle"]
			drawPuzzle(puzzle)
	elif(state['Role'] == "Music Puzzle"):
		prepareCanvas()
	elif(state['Role'] == "Rules"):
		prepareSVG()
	else:
		pass
		
def prepareSVG():
	global roleCanvas, board
	#Hide canvas, make sure svg stuff visible
	roleCanvas.elt.style.display = "none"
	board.elt.style.display = "initial"	

def prepareCanvas():
	global roleCanvas, board
	#Hide svg stuff, make canvas visible
	board.elt.style.display = "none"
	roleCanvas.elt.style.display = "initial"
	
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

	if (wall.loc == 'S'):
		transform = "rotate(180, 50, 50)"
	elif (wall.loc == 'E'):
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
	#fill="url(#wallpaper" + str(room_num) + wall.loc  + ")"				
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
	global LINE_WIDTH
	
	# Maps points to Div
	(X1,Y1) = mapCoordsToDIV(x1,y1)
	(X2,Y2) = mapCoordsToDIV(x2,y2)
	(X3,Y3) = mapCoordsToDIV(x3,y3)
	(X4,Y4) = mapCoordsToDIV(x4,y4)
	
	# Create string of points for svg_polygon
	Points = str(X1) + "," + str(Y1) + " " + str(X2) + "," + str(Y2) + " " + str(X3) + "," + str(Y3) + " " + str(X4) + "," + str(Y4)
	
	# Create polygon
	poly = svg.polygon(id=id,fill = fill, stroke = stroke, stroke_width = LINE_WIDTH,
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
	
def drawPuzzle(puzzle):
	global camanTranslator
	# Testing out pixel retrieving 
	global ctx, roleCanvas
	imgData0 = None
	imgData1 = None
	imgData0 = ctx.getImageData(0,0,roleCanvas.width,roleCanvas.height)
	imgData1 = ctx.getImageData(0,0,roleCanvas.width,roleCanvas.height)
	#imgData2 = ctx.createImageData(canvas.width,canvas.height)
	data0 = imgData0.data
	data1 = imgData1.data
	pixel = data0[1]
	#pixel = data0[1]
	#alert(pixel)
	#alert("before the nested loop")
	#for i in range(roleCanvas.width):
	#	for j in range(roleCanvas.height):
	#		for k in range(4):
	#			pass
				#set_pixel(imgData2,5,5,255,0,0,255)
				#data1[(j * roleCanvas.width) * 4 + i * 4 + k] = data0[(roleCanvas.height - 1 - j) * roleCanvas.width * 4 + (roleCanvas.width - 1 - i) * 4 + k]
				#imgData1.data[(j * roleCanvas.width) * 4 + i * 4 + k] = imgData0.data[(roleCanvas.height - 1 - j) * roleCanvas.width * 4 + (roleCanvas.width - 1 - i) * 4 + k]
	#ctx.putImageData(imgData1, 0, 0);
	# END TESTING
	
	camanTranslator.setImg()
	transformations = "this.revert();\n"
	for transform in puzzle.transformList:
		if (transform == "darkenImage"):
			transformations = transformations + "this.brightness(-20);\n"
		elif (transform == "brightenImage"):
			transformations = transformations + "this.brightness(20);\n"
		elif (transform == "rotate180"):
			#camanTranslator.rotate180()
			global ctx, roleCanvas
			imgData0 = None
			imgData1 = None
			imgData0 = ctx.getImageData(0,0,roleCanvas.width,roleCanvas.height)
			imgData1 = ctx.getImageData(0,0,roleCanvas.width,roleCanvas.height)
			#imgData2 = ctx.createImageData(canvas.width,canvas.height)
			imgTest = JSConstructor(imgData0)
			data0 = imgData0.data
			data1 = imgData1.data
			pixel = data0[1]
			alert(pixel)
			#alert("before the nested loop")
			for i in range(roleCanvas.width):
				for j in range(roleCanvas.height):
					for k in range(4):
						pass
						#set_pixel(imgData2,5,5,255,0,0,255)
						#data1[(j * roleCanvas.width) * 4 + i * 4 + k] = data0[(roleCanvas.height - 1 - j) * roleCanvas.width * 4 + (roleCanvas.width - 1 - i) * 4 + k]
						#imgData1.data[(j * roleCanvas.width) * 4 + i * 4 + k] = imgData0.data[(roleCanvas.height - 1 - j) * roleCanvas.width * 4 + (roleCanvas.width - 1 - i) * 4 + k]
			#ctx.putImageData(imgData1, 0, 0);
		else:
			alert("Not supported transform")
	transformations = transformations + "this.render()"
	#camanTranslator.CamanFunction(transformations)
	#alert("finished rendering")

def my_range(stard, end, step):
	while(start <= end):
		yield start
		start += step

def set_pixel(image_data,x,y,r,g,b,a):
	index = (x + y * image_data.width) * 4
	image_data.data[index+0] = r
	image_data.data[index+1] = g
	image_data.data[index+2] = b
	image_data.data[index+3] = a