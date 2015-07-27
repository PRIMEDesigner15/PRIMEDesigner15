'''PRIMEDesignerVisForBrython.py

Set up a GUI and handle updates and events during a run of
the PRIMEDesigner template in the Brython environment.
'''

from browser import window, document, html, alert, svg, console
from javascript import JSConstructor

# Used for play button
from PRIMEDesigner15MusicForBrython import handlePlayButtonClick


canMan = None
gui = None


statusline = None
opselect = None
APANEL = None
MARGIN = 20
ROOM_SIZE = 100
GAME_WIDTH = ROOM_SIZE * 3
GAME_HEIGHT = ROOM_SIZE * 3

# The svg element used for the archetect role
board = None

# The canvas and its context will go here when initialized for manipulation
roleCanvas = None
ctx = None

# The display div used for the music role display
musicDisplay = None

LAST_STATE = None # cache of current state for use in 
				#refresh of display after selection hiding button click.

LINE_WIDTH = 4

# Sets up the gui
def set_up_gui(opselectdiv, reset_and_backtrack_div):
	global gui
	gui = html.DIV(Id = "thegui")
	render_state()
	gui <= opselectdiv
	gui <= reset_and_backtrack_div
	document <= gui

def set_up_black_overlay():
	
	gui = document.getElementById("thegui")
	blackOverlay = html.DIV(id = "blackOverlay",
							style = {
								'display' : 'none',
								'position' : 'fixed',
								'top' : '0%',
								'left' : '0%',
								'width' : '100%',
								'height' : '100%',
								'background-color' : 'black',
								'z-index' : '1001',
								'-moz-opacity' : '0.8',
								'opacity' : '.80',
								'filter' : 'alpha(opacity=80)'
								})
	
	gui <= blackOverlay
	
# Sets up the loading div for asynchronous calls
def set_up_loading_div():

	width = 200
	height = 100
	loadingDiv = html.DIV(id = "loadingDiv",
							style = {
								'display' : 'none',
								'position' : 'fixed',
								'background-image' : 'url(images/loading.gif)',
								'border-radius' : '10px',
								'border' : '5px solid grey',
								'left' : '50%',
								'top' : '50%',
								'margin-top' : "-" + str(1/2 * height) + 'px',
								'margin-left' : "-" + str(1/2 * width) + 'px',
								'z-index' : '1002',
								'overflow' : 'auto'
							})
	loadingImg = html.IMG(id = "loadingImg", 
						src = "images/loading.gif", 
						style = {
								'display' : 'block',
								'width' : str(width) + "px",
								'height' : str(height) + "px",
								'margin' : 'auto'
								})


	loadingDiv <= loadingImg						
	gui <= loadingDiv
	
# Returns a form containing a list of radio button elements 
# with no ids for each of the four cardinal directions AND
# descriptive paragraph tags in between the radio buttons.
def create_direction_form():

	# List comprehension to construct inputs
	directionForm = html.FORM()
	directionInputs =\
		[html.INPUT(type="radio", name = 'direction', value = nme, style = {"display" : 'inline'} )
		for nme in ["North Wall", "East Wall", "South Wall", "West Wall"]]
	
	# Make first one checked
	directionInputs[0].checked = True
	
	# Append radio buttons to form, 
	# some string manipulation to make the values easier to handle
	for radioButton in directionInputs:
		directionForm <= radioButton
		directionForm <= html.P(radioButton.value, style = {"display" : "inline", "padding-right" : "10px"})
		radioButton.value = radioButton.value[0]
		
	return directionForm

# Creates an image puzzle list and a music puzzle list.
# Returns a div containing both the lists
def create_puzzle_lists(state):
	lists = html.DIV()
	imageList = html.DIV()
	musicList = html.DIV()
	

	title1 = html.P("Image Puzzles")
	title2 = html.P("Music Puzzles")

	imageList <= title1
	musicList <= title2
	
	# Create the image puzzle divs
	if(len(state["Image_Puzzles"]) == 0):
		title3 = html.P("No image puzzles created")
	else:
		for imagePuzzle in state["Image_Puzzles"]:
		
			listDiv = html.DIV()
			name = html.P(imagePuzzle.name)
			
			listDiv <= name
			imageList <= listDiv
	
	'''		
	# Create the music puzzle divs
	if(len(state["Music_Puzzle"]) == 0):
		title3 = html.P("No music puzzles created")
	else:
		for musicPuzzle in state["Music_Puzzles"]:
			
			listDiv = html.DIV()
			name = html.P(musicPuzzle.name)
			
			listDiv <= name
			musicList <= listDiv
		
	lists <= imageList
	lists <= musicList
	
	return lists'''
	
	
	
# Removes the add puzzle menu from the gui
def destroy_menu(menuName):
	menu = document.getElementById(menuName)
	gui.removeChild(menu)

# Creates an architect menu with choices of which puzzle to select.
# calls a callback function, sendBack, when the user hits a button.
def add_puzzle_menu(state, sendBack):
	musicPuzzles = state["Music_Puzzles"]
	imagePuzzles = state["Image_Puzzles"]
	
	width = 200
	height = 200
	menu = html.DIV(id = "addPuzzleMenu",
							style = {
								#'display' : 'none',
								'position' : 'fixed',
								#'width' : str(width) + "px",
								#'height' : str(height) + "px",
								'padding' : '10px',
								'background' : 'white',
								'border-radius' : '10px',
								'border' : '5px solid grey',
								'left' : '50%',
								'top' : '50%',
								'margin-top' : "-" + str(1/2 * height) + 'px',
								'margin-left' : "-" + str(1/2 * width) + 'px',
								'z-index' : '1003',
								'overflow' : 'auto'
							})
							
	title1 = html.P(id="addPuzzleTitle1", style = {"margin-top" : '0'})
	title1.innerHTML = "Place Puzzle:"
	
	title2 = html.P(id="addPuzzleTitle2")
	title2.innerHTML = "Which puzzle would you like to place?"
	
	title3 = html.P(id="addPuzzleTitle3")
	title3.innerHTML = "Which wall of the room?"
	
	direction = "N"
	alert("got here1")
	
	# Create the list of puzzles for the user to chose from
	create_puzzle_lists(state)
	
	
	directionForm = create_direction_form()
	#print(directionForm)
	
	def destroyAndSendBack():
		destroy_menu("addPuzzleMenu")
		
		# Get which direction is checked in the directionForm
		for elt in directionForm:
			if(elt.tagName == 'INPUT'):
				if(elt.checked == True):
					direction = elt.value
				
		sendBack(state,direction,"lolol")
	
	okButton = html.BUTTON(id = "addPuzzleOkButton")
	okButton.innerHTML = "Place Puzzle"
	okButton.onclick = destroyAndSendBack
	
	cancelButton = html.BUTTON(id = "addPuzzleCancelButton")
	cancelButton.innerHTML = "Cancel"
	cancelButton.onclick = lambda e: destroy_menu("addPuzzleMenu")
	
	# Append
	menu <= title1
	menu <= title2
	menu <= title3
	menu <= directionForm
	menu <= okButton
	menu <= cancelButton
	gui <= menu
	alert("appended")
	
def create_rule_menu(state, sendBack):
	rules = state["Rules"]
	
	width = 200
	height = 200
	menu = html.DIV(id = "createRuleMenu",
							style = {
								#'display' : 'none',
								'position' : 'fixed',
								#'width' : str(width) + "px",
								#'height' : str(height) + "px",
								'padding' : '10px',
								'background' : 'white',
								'border-radius' : '10px',
								'border' : '5px solid grey',
								'left' : '50%',
								'top' : '50%',
								'margin-top' : "-" + str(1/2 * height) + 'px',
								'margin-left' : "-" + str(1/2 * width) + 'px',
								'z-index' : '1003',
								'overflow' : 'auto'
							})

	title1 = html.P(id="createRuleTitle1", style = {"margin-top" : '0'})
	title1.innerHTML = "New Rule:"							

	def destroyAndSendBack():
		destroy_menu("createRuleMenu")
		
		# Get which direction is checked in the directionForm
		for elt in directionForm:
			if(elt.tagName == 'INPUT'):
				if(elt.checked == True):
					direction = elt.value
				
		sendBack(state,direction,"lolol")
	
	okButton = html.BUTTON(id = "createRuleOkButton")
	okButton.innerHTML = "Create Rule"
	okButton.onclick = destroyAndSendBack
	
	cancelButton = html.BUTTON(id = "createRuleCancelButton")
	cancelButton.innerHTML = "Cancel"
	cancelButton.onclick = lambda e: destroy_menu("createRuleMenu")
	
# Display the black overlay
def show_overlay():
	blackOverlay = document.getElementById("blackOverlay")
	blackOverlay.style.display = "initial"
	
# Show the loading screen and overlay
def show_loading():
	show_overlay()
	loadingDiv = document.getElementById("loadingDiv")
	loadingDiv.style.display = "initial"
	
# Hide the black overlay
def hide_overlay():
	blackOverlay = document.getElementById("blackOverlay")
	blackOverlay.style.display = "none"

# Hide the loading screen and overlay
def hide_loading():
	hide_overlay()
	loadingDiv = document.getElementById("loadingDiv")
	loadingDiv.style.display = "none"


# renders the state
def render_state():
	
	boarddiv = html.DIV(Id = "boarddivid", style = {"backgroundColor":"#CCFFCC"})
	boarddiv <= html.I("Puzzle state:")
	
	# Create canvas
	global ctx, roleCanvas
	roleCanvas = html.CANVAS(id = "roleCanvas", width = GAME_WIDTH, height = GAME_HEIGHT)
	ctx = roleCanvas.getContext("2d")
	
	# Create svg board
	global APANEL, board
	board = svg.svg(Id = "svgboard", 
					style = {"width":GAME_WIDTH, "height":GAME_HEIGHT,
							"backgroundColor":"#AAAABB"})
	board.elt.style.display = "none"
	APANEL = svg.g(Id = "panel")
	
	# Create music divs
	global musicDisplay
	musicDisplay = html.DIV(id ="musicDisplay")
	musicDisplay.style = { 'width' : str(GAME_WIDTH) + "px", 
							'height' : str(GAME_HEIGHT) + "px",
							"backgroundColor":"black",
							'display' : 'none',
							'color' : 'white',
							'text-align' : 'center', 
							'font-weight' : 'bold',
							'font-size' : '28pt'}
							
	playButton = html.BUTTON(id = "playButton", type = "button")
	playButton.style = {'width' : str( 1/4 *GAME_WIDTH) + "px",
						'height' : str( 1/5 * GAME_HEIGHT) + "px",
						'position' : 'absolute',
						'top' : str(GAME_HEIGHT + 10) + "px",
						'left' : "28px"
						}
	playButton.innerHTML = "Play Song"
	playButton.bind('click',handlePlayButtonClick)
	
	
	songSelected = html.P(id = "songSelected")
	songSelected.style = {'margin' : 0}
	songSelected.innerHTML = "No Song Selected"
	
		
	board <= APANEL	
	boarddiv <= board
	boarddiv <= roleCanvas
	musicDisplay <= songSelected
	musicDisplay <= playButton
	
	boarddiv <= musicDisplay
	
	gui <= boarddiv
	
	# Javascript that manages canvas.
	setCanvasManager()

def setCanvasManager():
	global canMan
	CanvasManagerConstructor = JSConstructor(window.CanvasManager)
	canMan = CanvasManagerConstructor(roleCanvas, "images/none.jpg")
	canMan.setImg()
		
# draws the game
def render_state_svg_graphics(state):
	global roleCanvas, ctx, APANEL, selected_image, musicDisplay
	# Clear svg panel
	while APANEL.lastChild is not None:
		APANEL.removeChild(APANEL.elt.lastChild)
	# Clear the roleCanvas
	ctx.clearRect(0,0, GAME_WIDTH, GAME_HEIGHT)

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
		if(state["Selected_Image"] != -1):
			puzzle = state["Image_Puzzles"][state["Selected_Image"]]
			canMan.setURL(puzzle.url)
			drawPuzzle(puzzle)
	elif(state['Role'] == "Music Puzzle"):
		prepareMusicDisplay()
		puzzle_num = state["Selected_Music"]
		
		songSelected = document.getElementById("songSelected")
		playButton = document.getElementById("playButton")
		
		if(puzzle_num > -1):
			songName = state["Music_Puzzles"][puzzle_num].name
			songSelected.innerHTML = "Song number " + str(puzzle_num + 1) + " selected \"" + songName + "\""
			
			# Bind the correct play song button to the button.
			playButton.unbind('click')
			playButton.bind('click', handlePlayButtonClick(state))
			playButton.disabled = False
		else:
			songSelected.innerHTML = "No song selected"
			playButton.disabled = True
		
	elif(state['Role'] == "Rules"):
		prepareSVG()
	else:
		pass
		
def prepareSVG():
	global roleCanvas, board, musicDisplay
	
	# Hide canvas, musicDisplay
	roleCanvas.elt.style.display = "none"
	musicDisplay.elt.style.display = "none" 
	
	# Make sure svg stuff visible
	board.elt.style.display = "block"	

def prepareCanvas():
	global roleCanvas, board, musicDisplay
	
	# Hide svg, musicDisplay
	board.elt.style.display = "none"
	musicDisplay.elt.style.display = "none"
	
	# Make canvas visible, call its JavaScript manager
	roleCanvas.elt.style.display = "block"
	setCanvasManager()
	
def prepareMusicDisplay():
	global roleCanvas, board, musicDisplay
	
	# Hide svg, roleCanvas
	board.elt.style.display = "none"
	roleCanvas.elt.style.display = "none"
	
	# Make musicDisplay visible
	musicDisplay.style.display = "block"
	
	
# draws a room.		
def drawRoom(room,room_num):
	# thickness of a room's walls.
	THICKNESS = .3
	
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
	global LINE_WIDTH, APANEL, board
	
	if (wall.loc == 'S'):
		transform = "translate(1,1),rotate(180)"
	elif (wall.loc == 'E'):
		transform = "translate(1,0),rotate(90)"
	elif (wall.loc == 'W'):
		transform = "translate(0,1),rotate(-90)"
	else:
		transform = "rotate(0)"
	
	# Create a pattern for image representation.
	pattern = svg.pattern(id="wallpaper" + str(room_num) + wall.loc,width = "100%",height = "100%")
	window.addAttribute(pattern,"patternContentUnits","objectBoundingBox")
	
	img = svg.image(xlink_href=wall.wallpaper.url, x= "0" ,y = "0", width = '1', height = '1', transform = transform)
	window.addAttribute(img,"preserveAspectRatio","none")
	
	# Append
	pattern <= img
	APANEL <= pattern
	WallpaperDiv = create_polygon(wall.x1, wall.y1, wall.x2, wall.y2, x3, y3, x4, y4,
								  fill="url(#wallpaper" + str(room_num) + wall.loc  + ")", id = wall.loc)
	#fill="url(#wallpaper" + str(room_num) + wall.loc  + ")"				
	# Append polygon to svg panel
	APANEL <= WallpaperDiv
	#board <= WallpaperDiv

# Draws a door frame on a wall with the given wall coordinates.
# and then draws a door on that frame.
def drawDoor(wall,x3,y3,x4,y4):

	# Caution: Sensitive variable, keep it around 2 for a good sized door.
	DOOR_SIZE = 1.2

	# map (f)rame coords to wall coords before translation
	(fx1,fy1,fx2,fy2,fx3,fy3,fx4,fy4) = (wall.x1,wall.y1,wall.x2,wall.y2,x3,y3,x4,y4)
	
	# fit the door (f)rame into a smaller trapezoid
	if (wall.loc == 'E' or wall.loc == 'W'):
		fy1 += 1/DOOR_SIZE * (3/8)
		fy2 -= 1/DOOR_SIZE * (3/8)
		fy3 -= 1/DOOR_SIZE * (4/15)
		fy4 += 1/DOOR_SIZE * (4/15)
		
	elif (wall.loc == 'N' or wall.loc == 'S'):
		fx1 += 1/DOOR_SIZE * (3/8)
		fx2 -= 1/DOOR_SIZE * (3/8)
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
	
	pattern = svg.pattern(id="door",height="100%",width = "100%")
	window.addAttribute(pattern,"patternContentUnits","objectBoundingBox")
	
	img = svg.image(xlink_href=wall.door.url, x="0",y="0", height="1", width="1")
	window.addAttribute(img,"preserveAspectRatio","none")
	
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
	newX = mapNumToDiv(x) 
	newY = mapNumToDiv(y)
	return (newX, newY)
	
def mapNumToDiv(x):
	global GAME_WIDTH, GAME_HEIGHT
	return int( (x * GAME_WIDTH)/3)
	
def drawPuzzle(puzzle):
	global canMan
	
	def done():
		for transform in puzzle.transformList:
			if (transform == "vertFlip"):
				canMan.vertFlip()
			elif (transform == "horizFlip"):
				canMan.horizFlip()
			elif (transform == "shuffleRows"):
				canMan.shuffleRows()
			elif (transform == "shuffleRowsInverse"):
				canMan.shuffleRowsInverse()
			elif (transform == "shuffleColumns"):
				canMan.shuffleColumns()
			else:
				alert("Not supported transform")

	canMan.setImg(done)
