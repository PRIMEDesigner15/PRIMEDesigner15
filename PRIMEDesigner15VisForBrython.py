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

# The svg element used for the architect role
board = None

# The canvas and its context will go here when initialized for manipulation
roleCanvas = None
ctx = None

# The display div used for the music role display
musicDisplay = None

# The display div used for the rule role display
ruleDisplay = None

LAST_STATE = None # cache of current state for use in 
				#refresh of display after selection hiding button click.

LINE_WIDTH = 4


# Should've done this a million years ago. Makes it easy
# to remove debug alerts.
def dAlert(string):
	alert(string)

brythonTitle = html.P(id = "pagetitle", style = {"background": "black", 
								"color" : "white", 
								"text-align" : "center",
								"font-size" : "30px"
								})
brythonTitle.innerHTML = "Brython Prime Client"

document <= brythonTitle
	
def url_is_valid(url):	
	# Note: Only works with Brython Implemented
	# if not, only returns true
	try:
		fileContents = open(url)
		return True
	except OSError:
		return False
	else:
		return False	
	
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
	
# Bad 0(n) operation to check if an element is in a list
def isWithin(item, list):
	found = False
	for element in list:
		if(item == element):
			found = True
	return found

# Returns a form containing a list of radio button elements 
# with no ids for each of the four cardinal directions AND
# descriptive paragraph tags in between the radio buttons.
# The banned directions, given as a list of characters, will grey out their respective radioButtons
def create_direction_form(bannedDirections = None):

	# List comprehension to construct inputs
	directionForm = html.FORM()
	directionInputs =\
		[html.INPUT(type="radio", name = 'direction', value = nme, style = {"display" : 'inline'} )
		for nme in ["North Wall", "East Wall", "South Wall", "West Wall"]]
	
	# Make first one checked
	#directionInputs[0].checked = True
	
	# Append radio buttons to form, 
	# some string manipulation to make the values easier to handle
	checked = False
	for radioButton in directionInputs:
		directionForm <= radioButton
		directionForm <= html.P(radioButton.value, style = {"display" : "inline", "padding-right" : "10px"})
		radioButton.value = radioButton.value[0]
		# Disable the radio button with the banned direction
		# and make the next available radioButton checked
		if(bannedDirections is not None):
			if(isWithin(radioButton.value, bannedDirections)):
				radioButton.disabled = True
			elif(not checked):
				radioButton.checked = True
				checked = True
	
	
	return directionForm

# Creates an image puzzle name list and a music puzzle name list.
# Returns a div containing both the lists.
def create_puzzle_lists(imagePuzzles,musicPuzzles):
	
	
	lists = html.DIV(id = "create_puzzle_lists")
	imageList = html.DIV(id = "create_puzzle_image_list")
	musicList = html.DIV(id = "Create_puzzle_music_list")

	title1 = html.P("Image Puzzles:")
	title2 = html.P("Music Puzzles:")
	# Enables image select, disables music select	
	def enableImageSelect():
		imageSelect = document.getElementById("imageSelect")
		musicSelect = document.getElementById("musicSelect")
		imageSelect.disabled = False
		musicSelect.disabled = True
	
	# Enables music select, disables image select
	def enableMusicSelect():
		imageSelect = document.getElementById("imageSelect")
		musicSelect = document.getElementById("musicSelect")
		imageSelect.disabled = True
		musicSelect.disabled = False

	imageList <= title1	
	musicList <= title2

	listSelect = html.SELECT(id = "imageSelect", disabled = True)

	# Create the image puzzle divs
	if(len(imagePuzzles) == 0):
		listSelect <= html.OPTION("No image puzzles created")
	else:
		i = 1
		rad1 = html.INPUT(type = "radio", name = "whichList")
		rad1.onclick = enableImageSelect
		for imagePuzzle in imagePuzzles:
			
			optionText = "Image puzzle " + str(i) + ", '" + imagePuzzle + "'"
			listSelect <= html.OPTION(optionText)
			i = i + 1
		
		imageList <= rad1
		
	imageList <= listSelect
	
	listSelect = html.SELECT(id = "musicSelect", disabled = True)
	# Create the music puzzle divs
	if(len(musicPuzzles) == 0):
		listSelect <= html.OPTION("No music puzzles created")
		listSelect.disabled = True
	else:
		i = 1
		rad2 = html.INPUT(type = "radio", name = "whichList")
		rad2.onclick = enableMusicSelect
		for musicPuzzle in musicPuzzles:
			
			optionText = "Music puzzle " + str(i) + ", '" + musicPuzzle + "'"
			listSelect <= html.OPTION(optionText)
			i = i + 1
		
		musicList <= rad2

	musicList <= listSelect
	
	lists <= imageList
	lists <= musicList
	
	return lists
	
# Removes any menu from the gui
def destroy_menu(menuName):	
	try:
		menu = document.getElementById(menuName)
		gui.removeChild(menu)
	except:
		console.log("Destroy menu was called on a nonexistent object.")

def disableOpSelect():
	# Disable operator controls
	opSel = document.getElementById("theoptselect")
	applyButton = document.getElementById("applyButtonID")
	
	opSel.disabled = True
	applyButton.disabled = True

def enableOpSelect():		
	# Enable op controls
	opSel = document.getElementById("theoptselect")
	applyButton = document.getElementById("applyButtonID")
	
	opSel.disabled = False
	applyButton.disabled = False
	
# Creates an architect menu with choices of which puzzle to select.
# The band direction will be disabled when the user tries to choose it.
# calls a callback function, sendBack, when the user hits a button.
def add_puzzle_menu(state, sendBack, bannedDirections = None):

	disableOpSelect()

	# Convert to list for easy indexing
	musicPuzzles = list(state["Music_Puzzles"])
	imagePuzzles = list(state["Image_Puzzles"])
	
	
	musLen = len(musicPuzzles)
	imgLen = len(imagePuzzles)
	
	width = 200
	height = 200
	menu = html.DIV(id = "addPuzzleMenu",
							style = {
								'text-align' : 'center',
								'position' : 'fixed',
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
							
	title1 = html.P(id="addPuzzleTitle1", style = {"margin-top" : '0', 'text-align' : 'left', 'font-size' : '13px'})
	title1.innerHTML = "Place Puzzle:"
	
	title2 = html.P(id="addPuzzleTitle2")
	title2.innerHTML = "Which puzzle would you like to place?"
	
	title3 = html.P(id="addPuzzleTitle3")
	title3.innerHTML = "Which wall of the room?"
	
	direction = "N"
	
	
	# Create the list of puzzle names for the user to chose from
	lists = create_puzzle_lists(imagePuzzles,musicPuzzles)
	
	# Create Direction Form
	directionForm = create_direction_form(bannedDirections)
	#print(directionForm)
	
	
	def destroyAndSendBack():
		
		# Get which direction is checked in the directionForm
		for element in directionForm:
			if(element.tagName == 'INPUT'):
				if(element.checked == True):
					direction = element.value
		
		#Get chosen puzzle
		chosen = None
		imgSelect = document.getElementById("imageSelect")
		musSelect = document.getElementById("musicSelect")
		
		if(imgSelect.disabled != musSelect.disabled):
			
			if(imgSelect.disabled):
				chosenNum = musSelect.selectedIndex
				chosen = musicPuzzles[chosenNum]
			else:
				chosenNum = musSelect.selectedIndex
				chosen = imagePuzzles[chosenNum]
			
			# Send back information and destroy the state
			destroy_menu("addPuzzleMenu")
			
			enableOpSelect()
			
			sendBack(state,direction,chosen)
		else:
			alert("No puzzle selected")	
		
	okButton = html.BUTTON(id = "addPuzzleOkButton", style = {"margin-top" : "10px", "margin-right" : "10px"})
	okButton.innerHTML = "Place Puzzle"
	okButton.onclick = destroyAndSendBack
	
	cancelButton = html.BUTTON(id = "addPuzzleCancelButton", style = {"margin-top" : "10px"})
	cancelButton.innerHTML = "Cancel"
	cancelButton.onclick = lambda e: cancelAddPuzzle()
	
	# Append
	menu <= title1
	menu <= title2
	menu <= lists
	menu <= title3
	menu <= directionForm
	menu <= okButton
	menu <= cancelButton
	gui <= menu

def cancelAddPuzzle():
	destroy_menu("addPuzzleMenu")
	enableOpSelect()	

def add_condition_form(state):		

	conditions = state['ConditionMaster']	
	
	# List comprehension to construct inputs
	conditionForm = html.FORM(id = "conditionForm")
	conditionSelect = html.SELECT(id = "conditionSelect")
	conditionSelect.style = {'margin-right' : '10px'}
	
	conditionOpt = html.OPTION("Nothing Selected")
	conditionSelect <= conditionOpt
	
	for condition in conditions:
		conditionOpt = html.OPTION(condition)
		conditionSelect <= conditionOpt 
	
	conditionOpt = html.OPTION("Solve Puzzle")
	conditionSelect <= conditionOpt 
	
	conditionSelect.onchange = cFollowUp(state)
	
	conditionDiv = html.DIV()
	
	conditionDiv <= "Condition: "
	conditionDiv <= conditionSelect
	
	conditionForm <= conditionDiv
	
	return conditionForm	
	
def cFollowUp(state):
	
	def cFollowUp2():
		cFollowUp = document.getElementById("cFollowUp")
		
		if (cFollowUp is not None):
			cFollowUp.parentNode.removeChild(cFollowUp)

		
		cFollowUp = html.DIV(id="cFollowUp", style = {"margin" : '10px'})
		
		conditionForm = document.getElementById("conditionForm")
		
		condition = document.getElementById("conditionSelect").value
		cFollowUpSelect = html.SELECT(id = "cFollowUpSelect", style = {"margin-left" : "10px"})	
		if(condition == "Enter Room"):
			cFollowUp <= "Pick a room:"
			for num in range(1,10):
				roomNum = html.OPTION("Enter Room " + str(num))
				cFollowUpSelect <= roomNum

			cFollowUp <= cFollowUpSelect
			conditionForm <= cFollowUp
		elif(condition == "Solve Puzzle"):
		
			cFollowUp <= "Pick a puzzle:"			
			puzzleOp = html.OPTION("Nothing Selected")
			cFollowUpSelect <= puzzleOp
			
			# Puzzles are gathered by searching rooms that have been placed
			# so the rules designer has context for which puzzles to attach conditions too
			for index, room in enumerate(state["Rooms"]):
				for wall in room.walls.values():
					if wall.puzzle is not None:
						puzzleOp = html.OPTION("Solve puzzle in room " + str(index + 1) + " on " + wall.loc + " wall.")
						cFollowUpSelect <= puzzleOp
					
			cFollowUp <= cFollowUpSelect
			conditionForm <= cFollowUp
		elif(condition == "Have Points"):
		
			cFollowUp <= "Enter point amount:"
			textInput = html.INPUT(type="text", id="textInput", style = {"margin-left" : "10px"})
			cFollowUp <= textInput
			conditionForm <= cFollowUp
			
		elif(condition == "Time Elapses"):
			
			cFollowUp <= "Enter time in minutes:"
			textInput = html.INPUT(type="text", id="textInput", style = {"margin-left" : "10px"})
			cFollowUp <= textInput
			conditionForm <= cFollowUp
			
		else:
			pass #console.log("Debug: No Condition Follow Up expected")	
	
	return cFollowUp2
	
def add_condition_menu(state, sendBack):
	width = 200
	height = 200
	menu = html.DIV(id = "addConditionMenu",
							style = {
								#'display' : 'none',
								'position' : 'fixed',
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

	conditionTitle = html.P(id="addConditionMenuTitle", style = {"margin-top" : '0'})
	conditionTitle.innerHTML = "Add Condition:"							
	
	disableOpSelect()
	
	#Create and populate conditionSelect
	conditionForm = add_condition_form(state)	
	
	def destroyAndSendBack():
	
		if (document.getElementById("conditionSelect") is not None):
			condition = document.getElementById("conditionSelect").value
		else:
			condition = None

		if (document.getElementById("cFollowUpSelect") is not None):
			conditionF = document.getElementById("cFollowUpSelect").value
		else:
			conditionF = None
		
		if (document.getElementById("textInput") is not None):
			textF = document.getElementById("textInput").value
		else:
			textF = None
		
		cFollowUp = False
		if (condition is None or condition == "Nothing Selected"):
			alert("No condition was selected.")
		else:
			if (conditionF is not None and conditionF != 'Nothing Selected'):
				cFollowUp = True
				
			if ((condition == "Enter Room" or condition == "Solve Puzzle") and cFollowUp is False):
				alert("Not enough information was entered.")
			else:
				#console.log("Debug: Enough info was given.")
				
				destroy_menu("addConditionMenu")
				
				enableOpSelect()
				
				if(textF is not None and textF.strip() != ''):
					if(condition == "Have Points"):
						conditionF = "Have " + textF + " Points."
					elif(condition == "Time Elapses"):
						conditionF = textF + " minutes elapse."
					else:
						alert("invalid condition for follow up.")
				
				if(conditionF is not None):
					condition = conditionF

				
				sendBack(condition)	
	
	okButton = html.BUTTON(id = "addConditionOkButton", style = {'margin' : '10px'})
	okButton.innerHTML = "Add"
	okButton.onclick = destroyAndSendBack
	
	cancelButton = html.BUTTON(id = "addConditionCancelButton")
	cancelButton.innerHTML = "Cancel"
	cancelButton.onclick = lambda e: cancelMenu(menu.id)

	menu <= conditionTitle
	menu <= conditionForm
	menu <= okButton
	menu <= cancelButton

	gui <= menu

def add_action_form(state):
	actions = state["ActionMaster"]
	
	# List comprehension to construct inputs
	actionForm = html.FORM(id = "actionForm")
	actionSelect = html.SELECT(id = "actionSelect")
	actionSelect.style = {'margin-right' : '10px'}
	
	actionOpt = html.OPTION("Nothing Selected")
	actionSelect <= actionOpt
	
	for action in actions:
		actionOpt = html.OPTION(action)
		actionSelect <= actionOpt
	
	actionSelect.onchange = lambda e: aFollowUp(state)
	
	actionDiv = html.DIV()
	
	actionDiv <= "Action: "
	actionDiv <= actionSelect
	
	actionForm <= actionDiv
	
	return actionForm

def aFollowUp(state):

	aFollowUp = document.getElementById("aFollowUp")
	
	if (aFollowUp is not None):
		aFollowUp.parentNode.removeChild(aFollowUp)
	
	aFollowUp = html.DIV(id="aFollowUp", style = {"margin" : '10px'})

	actionForm = document.getElementById("actionForm")
	
	action = document.getElementById("actionSelect").value
	
	aFollowUpSelect = html.SELECT(id = "aFollowUpSelect", style = {"margin-left" : "10px"})
	
	if(action == "Open Door"):
		aFollowUp <= "Pick a door:"
		
		doorOp = html.OPTION("Nothing Selected")
		aFollowUpSelect <= doorOp
		
		for index, room in enumerate(state["Rooms"]):
			for wall in room.walls.values():
				if wall.hasDoor:
					doorOp = html.OPTION("Open door in room " + str(index + 1) + " on " + wall.loc + " wall.")
					aFollowUpSelect <= doorOp
		aFollowUp <= aFollowUpSelect
		actionForm <= aFollowUp
		
	elif(action == "Close Door"):
		aFollowUp <= "Pick a door:"
		
		doorOp = html.OPTION("Nothing Selected")
		aFollowUpSelect <= doorOp
		
		for index, room in enumerate(state["Rooms"]):
			for wall in room.walls.values():
				if wall.hasDoor:
					doorOp = html.OPTION("Close Door in room " + str(index + 1) + " on " + wall.loc + " wall.")
					aFollowUpSelect <= doorOp
		aFollowUp <= aFollowUpSelect
		actionForm <= aFollowUp
		
	elif(action == "Play Sound"):
		aFollowUp <= "Sound Link:"
		textInput = html.INPUT(type="text", id="textInput", style = {"margin-left" : "10px"})
		aFollowUp <= textInput
		actionForm <= aFollowUp
	elif(action == "Display Message"):
		aFollowUp <= "Enter your message:"
		textInput = html.INPUT(type="text", id="textInput", style = {"margin-left" : "10px"})
		aFollowUp <= textInput
		actionForm <= aFollowUp
	elif(action == "Gain Points"):
		aFollowUp <= "Gain how many points?"
		textInput = html.INPUT(type="text", id="textInput", style = {"margin-left" : "10px"})
		aFollowUp <= textInput
		actionForm <= aFollowUp
	elif(action == "Lose Points"):
		aFollowUp <= "Lose how many points?"
		textInput = html.INPUT(type="text", id="textInput", style = {"margin-left" : "10px"})
		aFollowUp <= textInput
		actionForm <= aFollowUp
	else:
		pass #console.log("Debug: No Action Follow Up expected")	
	
def add_action_menu(state, sendBack):
	width = 200
	height = 200
	menu = html.DIV(id = "addActionMenu",
							style = {
								#'display' : 'none',
								'position' : 'fixed',
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

	actionTitle = html.P(id="addActionMenuTitle", style = {"margin-top" : '0'})
	actionTitle.innerHTML = "Add Action:"							
	
	disableOpSelect()
	
	#Create and populate actionSelect
	actionForm = add_action_form(state)	
	
	def destroyAndSendBack():

		if (document.getElementById("actionSelect") is not None):
			action = document.getElementById("actionSelect").value
		else:
			action = None

		if (document.getElementById("aFollowUpSelect") is not None):
			actionF = document.getElementById("aFollowUpSelect").value
		else:
			actionF = None

		if (document.getElementById("textInput") is not None):
			textF = document.getElementById("textInput").value
		else:
			textF = None
		
		aFollowUp = False
		if (action is None or action == "Nothing Selected"):
			alert("No action was selected.")
		else:
			if ((textF is not None and textF.strip() != '') or (actionF is not None and actionF != 'Nothing Selected')):
				aFollowUp = True	
			if (action == "Open Door" and aFollowUp is False
				or action == "Close Door" and aFollowUp is False
				or action == "Display Message" and aFollowUp is False):
				alert("Not enough information was entered.")
			elif(action == "Play Sound" and not url_is_valid(textF)):
				alert("File link was invalid.")
			else:
				#console.log("Debug: Enough info was given.")
				
				destroy_menu("addActionMenu")
				
				enableOpSelect()
				
				# Make sure something was actually put into the text box
				if(textF is not None and textF.strip() != ''):
					# Change display of text box information based on action.
					if(action == "Display Message"):
						actionF = "Display Message: " + "\"" + textF + "\""
					elif(action == "Play Sound"):
						actionF = "Play sound from link: \"" + textF + "\""
					elif(action == "Gain Points"):
						actionF = "Gain " + textF + " Points"
					elif(action == "Lose Points"):
						actionF = "Lose " + textF + " Points"
				if(actionF is not None):
					action = actionF
				
				sendBack(action)	
	
	okButton = html.BUTTON(id = "addActionOkButton", style = {'margin' : '10px'})
	okButton.innerHTML = "Add"
	okButton.onclick = destroyAndSendBack
	
	cancelButton = html.BUTTON(id = "addActionCancelButton")
	cancelButton.innerHTML = "Cancel"
	cancelButton.onclick = lambda e: cancelMenu(menu.id)
	
	menu <= actionTitle
	menu <= actionForm
	menu <= okButton
	menu <= cancelButton

	gui <= menu
	
def cancelMenu(id):
	destroy_menu(id)
	enableOpSelect()
	
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
	boarddiv = html.DIV(Id = "boarddivid", style = {"backgroundColor":"rgb(180,198,211)"})
	
	# Create canvas
	global ctx, roleCanvas
	roleCanvas = html.CANVAS(id = "roleCanvas", width = GAME_WIDTH, height = GAME_HEIGHT)
	ctx = roleCanvas.getContext("2d")
	
	# Create svg board
	global APANEL, board
	board = svg.svg(Id = "svgboard", 
					style = {"width":GAME_WIDTH, "height":GAME_HEIGHT,
							"backgroundColor":"rgb(190,208,221)"})
	board.elt.style.display = "none"
	APANEL = svg.g(Id = "panel", style = {"text-align" : "center"})
	
	# Create music divs
	global musicDisplay
	musicDisplay = html.DIV(id ="musicDisplay")
	musicDisplay.style = {  'width' : str(GAME_WIDTH) + "px", 
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
	
	# Create rule divs
	global ruleDisplay
	ruleDisplay = html.DIV(id="ruleDisplay")
	ruleDisplay.style = {  'width' : str(GAME_WIDTH) + "px", 
							'height' : str(GAME_HEIGHT) + "px",
							"backgroundColor":"black",
							'display' : 'none',
							'color' : 'white',
							'text-align' : 'center', 
							'font-weight' : 'bold',
							'font-size' : '28pt'}
	
	
	board <= APANEL	
	boarddiv <= board
	boarddiv <= roleCanvas
	musicDisplay <= songSelected
	musicDisplay <= playButton
	
	boarddiv <= musicDisplay
	boarddiv <= ruleDisplay
	
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
	global roleCanvas, ctx, APANEL, selected_image, musicDisplay, ruleDisplay
	# Clear svg panel
	while APANEL.lastChild is not None:
		APANEL.removeChild(APANEL.elt.lastChild)
	# Clear the roleCanvas
	ctx.clearRect(0,0, GAME_WIDTH, GAME_HEIGHT)
	# Clear the ruleDisplay
	while ruleDisplay.lastChild is not None:
		ruleDisplay.removeChild(ruleDisplay.childNodes[0])
		
	if(state['Role'] == "Architect"):
		prepareSVG()
		
		# Draw all the rooms.
		for room_num, room in enumerate(state['Rooms']):
			drawRoom(room,room_num)
		
		#add outline to selected room
		THICKNESS = 1.5
		selected_room = state['Rooms'][state['Selected_Room']]
			
		(x1, y1) = mapCoordsToDIV(selected_room.x1, selected_room.y1)
		(x2, y2) = mapCoordsToDIV(selected_room.x2, selected_room.y2)
			
		outline = svg.rect(x = x1, y = y1, width = x2 - x1, height = y2 - y1, fill = "none",
						style = {"stroke": "gold", "stroke-width": THICKNESS})
		APANEL <= outline
	elif(state['Role'] == "Image Puzzle"):
		prepareCanvas()	
		if(state["Selected_Image"] is not None):
			puzzle = state["Image_Puzzles"][state["Selected_Image"]]
			canMan.setURL(puzzle.url)
			drawImagePuzzle(puzzle)
	elif(state['Role'] == "Music Puzzle"):
		
		prepareMusicDisplay()
		songName = state["Selected_Music"]
		
		songSelected = document.getElementById("songSelected")
		playButton = document.getElementById("playButton")
		
		if(songName is not None):
			songSelected.innerHTML = "Song: \"" + songName + "\" selected"
			
			# Bind the correct play song button to the button.
			playButton.unbind('click')
			playButton.bind('click', handlePlayButtonClick(state))
			playButton.disabled = False
		else:
			songSelected.innerHTML = "No song selected"
			playButton.disabled = True
		
	elif(state['Role'] == "Rules"):
		prepareRuleDisplay()
		
		# Draw all the rooms in architect view.
		for room_num, room in enumerate(state['Rooms']):
			drawRoom(room,room_num)
		
		rulesTitle = html.P(id="rulesTitle", style = {'margin' : 0, 'border-bottom' : '5px solid white'})
		
		# If no rules then display message
		if(len(state["Rules"]) == 0):
			rulesTitle.innerHTML = "There are no Rules."
			ruleDisplay <= rulesTitle
			
		# Otherwise display all rules with delete buttons
		else:	
			rulesTitle.innerHTML = "Rules:"
			ruleDisplay <= rulesTitle
			populateRuleDisplay(state)

	else:
		pass

def populateRuleDisplay(state):
	global ruleDisplay
	
	rHeight = ruleDisplay.height
	tHeight = document.getElementById("rulesTitle").height
	
	tableWrapper = html.DIV(id="tableWrapper", style = {'position' : 'relative', 'height' : 'auto'})
	scrollDiv = html.DIV(id="tableScroll", style = {'height' : str(rHeight - tHeight) + 'px', 'overflow' : 'auto'})
	ruleTable = html.TABLE(id="ruleTable", style = {'width' : '100%', 'font-size' : '13px'})
	headerRow = html.TR(id="ruleHeaders")
	
	headerRow <= html.TH("Number")
	headerRow <= html.TH("Conditions")
	headerRow <= html.TH("Actions")
	
	ruleTable <= headerRow

	for index, rule in enumerate(state["Rules"]):
		color = 'white'
		if(rule.defunct):
			color = 'red'
			
		newRow = html.TR(id = "ruleRow" + str(index + 1))
		newRow <= html.TD(str(index+1), style = {'color' : color})
		newRow <= html.TD(str(rule.conditions)[1:-1], style = {'color' : color})
		newRow <= html.TD(str(rule.actions)[1:-1], style = {'color' : color})

		
		#ruleItem = html.DIV(str(index) + ": " + str(rule.name), style = {"font-size" : "13px"})
		#ruleDisplay <= ruleItem
		
		ruleTable <= newRow
	
	ruleTable.border = '10px solid white'
	scrollDiv <= ruleTable
	tableWrapper <= scrollDiv
	ruleDisplay <= tableWrapper
	
def prepareSVG():
	global roleCanvas, board, musicDisplay, ruleDisplay
	
	# Hide canvas, musicDisplay
	roleCanvas.elt.style.display = "none"
	musicDisplay.elt.style.display = "none" 
	ruleDisplay.elt.style.display = "none" 
	
	# Make sure svg stuff visible
	board.elt.style.display = "block"	

def prepareCanvas():
	global roleCanvas, board, musicDisplay, ruleDisplay
	
	# Hide svg, musicDisplay
	board.elt.style.display = "none"
	musicDisplay.elt.style.display = "none"
	ruleDisplay.elt.style.display = "none"
	
	# Make canvas visible, call its JavaScript manager
	roleCanvas.elt.style.display = "block"
	setCanvasManager()
	
def prepareMusicDisplay():
	global roleCanvas, board, musicDisplay, ruleDisplay
	
	# Hide svg, roleCanvas
	board.elt.style.display = "none"
	roleCanvas.elt.style.display = "none"
	ruleDisplay.elt.style.display = "none"
	
	# Make musicDisplay visible
	musicDisplay.style.display = "block"

def prepareRuleDisplay():
	global roleCanvas, board, musicDisplay, ruleDisplay
	
	# Hide music and image displays
	roleCanvas.elt.style.display = "none"
	musicDisplay.elt.style.display = "none"
	
	# Make ruleDisplay visible
	ruleDisplay.style.display = "block"
	# Make Architect display visible
	board.elt.style.display = "block"
	
# draws a room.		
def drawRoom(room,room_num):
	
	if(room.aMusic is not None):
		# Create a pattern for image representation.
		pattern = svg.pattern(id="ambientMusic",width = "100%",height = "100%")
		window.addAttribute(pattern,"patternContentUnits","objectBoundingBox")
		
		img = svg.image(xlink_href="images/note.png", x= "0" ,y = "0", width = '1', height = '1')
		window.addAttribute(img,"preserveAspectRatio","none")
		(x1,y1) = mapCoordsToDIV(room.walls['N'].x1,room.walls['E'].y1)
		(x2,y2) = mapCoordsToDIV(room.walls['N'].x2,room.walls['E'].y2)
		ambientDiv = svg.rect(x = x1, y = y1, width = x2 - x1, height = y2 - y1, fill = "url(#ambientMusic)")
		
		
		# Append
		pattern <= img
		APANEL <= pattern
		APANEL <= ambientDiv
	
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
	
	if (wall.hasDoor):
		drawDoor(wall,x3,y3,x4,y4)

	if (wall.puzzle is not None):
		type = "imagePuzzle"
		drawPuzzle(wall,type,x3,y3,x4,y4)

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
	
	img = svg.image(xlink_href=wall.wallpaperurl, x= "0" ,y = "0", width = '1', height = '1', transform = transform)
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
	if(wall.doorOpen):
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
	
	img = svg.image(xlink_href="images/door.jpg", x="0",y="0", height="1", width="1")
	window.addAttribute(img,"preserveAspectRatio","none")
	
	pattern <= img
	defs <= pattern
		
	# Append polygon to svg panel
	APANEL <= defs
	APANEL <= frameDiv
	APANEL <= doorDiv
	
# Draws a wall on a wall with the given wall coordinates.
# Fills in the polygon green for image puzzles and blue for music puzzles.
def drawPuzzle(wall,type,x3,y3,x4,y4):
	# Caution: Sensitive variable, keep it around 1 for a good sized puzzle.
	PUZZLE_SIZE = 1.2
	# map (p)uzzle coords to wall coords before translation
	(px1,py1,px2,py2,px3,py3,px4,py4) = (wall.x1,wall.y1,wall.x2,wall.y2,x3,y3,x4,y4)
	
	# fit the (p)uzzle into a smaller trapezoid
	if (wall.loc == 'E' or wall.loc == 'W'):
		py1 += 1/PUZZLE_SIZE * (1/4)
		py2 -= 1/PUZZLE_SIZE * (1/4)
		py3 -= 1/PUZZLE_SIZE * (1/5)
		py4 += 1/PUZZLE_SIZE * (1/5)
		
	elif (wall.loc == 'N' or wall.loc == 'S'):
		px1 += 1/PUZZLE_SIZE * (1/4)
		px2 -= 1/PUZZLE_SIZE * (1/4)
		px3 -= 1/PUZZLE_SIZE * (1/5)
		px4 += 1/PUZZLE_SIZE * (1/5)
	else:
		alert("drawPuzzle wall location check broke")
			
	# Create puzzle polygon
	fill = "green"	
	puzzleDiv = create_polygon(px1,py1,px2,py2,px3,py3,px4,py4, fill = fill)
	
	APANEL <= puzzleDiv

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
	
def drawImagePuzzle(puzzle):
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
