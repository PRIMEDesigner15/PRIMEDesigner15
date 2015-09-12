'''PRIMEDesignerVisForBrython.py

Set up a GUI and handle updates and events during a run of
the PRIMEDesigner template in the Brython environment.
'''

from browser import window, document, html, alert, svg, console
from javascript import JSConstructor

# Used for play button
from PRIMEDesigner15MusicForBrython import handlePlayButtonClick
import re

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
PList = None

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
	loadingDiv = create_menu("loadingDiv",width,height,display = "none")
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

# Returns a popup menu with the specified id
def create_menu(id,width,height,display = "visible"):

	menu = html.DIV(id = id,
							style = {
								'display' : display,
								'position' : 'fixed',
								'padding' : '10px',
								'background' : 'white',
								'border-radius' : '10px',
								'border' : '5px solid grey',
								'left' : '50%',
								'top' : '50%',
								'margin-top' : "-" + str(1/2 * height) + 'px',
								'margin-left' : "-" + str(1/2 * width) + 'px',
								'text-align' : 'center',
								'z-index' : '1003',
								'overflow' : 'auto'
							})

	if(display != "none"):
		disableOpSelect()
	
	return menu
	
# Removes any menu from the gui
def destroy_menu(menuName):	
	try:
		enableOpSelect()
		menu = document.getElementById(menuName)
		gui.removeChild(menu)
	except:
		console.log("Destroy menu was called on a nonexistent object.")

def disableOpSelect():
	# Disable operator controls
	opSel = document.getElementById("theoptselect")
	applyButton = document.getElementById("applyButtonID")
	resetState = document.getElementById("RESET_BUTTONID")
	backTrack = document.getElementById("BACKTRACK_BUTTONID")
	
	opSel.disabled = True
	applyButton.disabled = True
	resetState.disabled = True
	backTrack.disabled = True

def enableOpSelect():		
	# Enable op controls
	opSel = document.getElementById("theoptselect")
	applyButton = document.getElementById("applyButtonID")
	resetState = document.getElementById("RESET_BUTTONID")
	backTrack = document.getElementById("BACKTRACK_BUTTONID")
	
	opSel.disabled = False
	applyButton.disabled = False
	resetState.disabled = False
	backTrack.disabled = False
	
# Creates an architect menu with choices of which puzzle to select.
# The band direction will be disabled when the user tries to choose it.
# calls a callback function, sendBack, when the user hits a button.
def add_puzzle_menu(state, sendBack, bannedDirections = None):


	# Convert to list for easy indexing
	musicPuzzles = list(state["Music_Puzzles"])
	imagePuzzles = list(state["Image_Puzzles"])
	
	
	musLen = len(musicPuzzles)
	imgLen = len(imagePuzzles)
		
	width = 200
	height = 200
	menu = create_menu("addPuzzleMenu", width, height)
							
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
	
	conditionSelect.onchange = lambda e: cFollowUp(state)
	
	conditionDiv = html.DIV()
	
	conditionDiv <= "Condition: "
	conditionDiv <= conditionSelect
	
	conditionForm <= conditionDiv
	
	return conditionForm	
	
def cFollowUp(state):
	cFollowUp = document.getElementById("cFollowUp")
	
	if (cFollowUp is not None):
		cFollowUp.parentNode.removeChild(cFollowUp)

	cFollowUp = html.DIV(id="cFollowUp", style = {"margin" : '10px'})
	
	conditionForm = document.getElementById("conditionForm")
	
	condition = document.getElementById("conditionSelect").value
	cFollowUpSelect = html.SELECT(id = "cFollowUpSelect", style = {"margin-left" : "10px"})	
	
	def numbersOnly(ev):
			input = document.getElementById("textInput")
			text = input.value
			input.value = re.sub(r'\D',"",text)
			
	if(condition == "Entered Room"):
		cFollowUp <= "Pick a room:"
		for num in range(1,10):
			roomNum = html.OPTION("Entered Room " + str(num))
			cFollowUpSelect <= roomNum

		cFollowUp <= cFollowUpSelect
		conditionForm <= cFollowUp
		
	elif(condition == "Solved Puzzle"):
	
		cFollowUp <= "Pick a puzzle:"			
		puzzleOp = html.OPTION("Nothing Selected")
		cFollowUpSelect <= puzzleOp
		
		'''
		allPuzzles = []
		# Add puzzles to list
		for puzzleName in state["Image_Puzzles"]:
			allPuzzles.append(puzzleName)
	
		for puzzleName in state["Music_Puzzles"]:
			allPuzzles.append(puzzleName)
			
		#Changed to no longer care where a puzzle is located		
		for index, puzzle in enumerate(allPuzzles):
			puzzleOp = html.OPTION("Solve Puzzle " + str(index) + " : " + str(puzzle))
			cFollowUpSelect <= puzzleOp
		'''
			
		# Puzzles are gathered by searching rooms that have been placed
		# so the rules designer has context for which puzzles to attach conditions too
		for index, room in enumerate(state["Rooms"]):
			for wall in room.walls.values():
				#if wall.puzzle is not None:
				puzzleOp = html.OPTION("Solved puzzle in room " + str(index + 1) + " on " + wall.loc + " wall.")
				cFollowUpSelect <= puzzleOp
				
		cFollowUp <= cFollowUpSelect
		conditionForm <= cFollowUp
		
	elif(condition == "Had Points"):
		
	
		cFollowUp <= "Enter point amount:"
		textInput = html.INPUT(type="text", id="textInput", name = "hasAPattern", style = {"margin-left" : "10px"})
	
		textInput.bind('keyup',validInput)
		
		cFollowUp <= textInput
		conditionForm <= cFollowUp
		
	elif(condition == "Time Elapsed"):
		
		cFollowUp <= "Enter time in minutes:"
		textInput = html.INPUT(type="text", id="textInput", style = {"margin-left" : "10px"})
		textInput.bind('keyup',validInput)
		cFollowUp <= textInput
		conditionForm <= cFollowUp
		
	else:
		pass #console.log("Debug: No Condition Follow Up expected")	
	
def add_condition_menu(state, sendBack):
		
	width = 200
	height = 200
	menu = create_menu("addConditionMenu",width,height)
	
	conditionTitle = html.P(id="addConditionMenuTitle", style = {"margin-top" : '0'})
	conditionTitle.innerHTML = "Add Condition:"							
	
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
				
			if ((condition == "Entered Room" or condition == "Solved Puzzle") and cFollowUp is False):
				alert("Not enough information was entered.")
			else:
				#console.log("Debug: Enough info was given.")
				
				destroy_menu("addConditionMenu")
				
				enableOpSelect()
				
				if(textF is not None and textF.strip() != ''):
					if(condition == "Had Points"):
						conditionF = "Had " + textF + " Points."
					elif(condition == "Time Elapsed"):
						conditionF = textF + " minutes elapse."
					else:
						alert("invalid condition for follow up.")
				
				if(conditionF is not None):
					condition = conditionF

				sendBack(condition)	
	
	okButton = html.BUTTON(id = "addConditionOkButton", style = {'margin' : '10px'})
	okButton.innerHTML = "Add"
	conditionForm <= okButton
	
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
	
	if(action == "Opened Door"):
		aFollowUp <= "Pick a door:"
		
		doorOp = html.OPTION("Nothing Selected")
		aFollowUpSelect <= doorOp
		
		for index in range(1, 10):
			for side in ['S', 'E']:
				if side == 'S':
					south = index + 3
					if (south < 10):
						doorOp = html.OPTION("Opened door between rooms " + str(index) + " and " + str(south))
						aFollowUpSelect <= doorOp
				if side == 'E':
					east = index + 1
					if (east % 3 is not 1):
						doorOp = html.OPTION("Opened door between rooms " + str(index) + " and " + str(east))
						aFollowUpSelect <= doorOp					
		'''
		for index, room in enumerate(state["Rooms"]):
			for wall in ['N', 'S', 'E', 'W']:
				doorOp = html.OPTION("Open door in room " + str(index + 1) + " on " + wall + " wall.")
				aFollowUpSelect <= doorOp
		'''		
		'''
		for index, room in enumerate(state["Rooms"]):
			for wall in room.walls.values():
				if wall.hasDoor:
					doorOp = html.OPTION("Open door in room " + str(index + 1) + " on " + wall.loc + " wall.")
					aFollowUpSelect <= doorOp
		'''
		aFollowUp <= aFollowUpSelect
		actionForm <= aFollowUp
		
	elif(action == "Closed Door"):
		aFollowUp <= "Pick a door:"
		
		doorOp = html.OPTION("Nothing Selected")
		aFollowUpSelect <= doorOp

		for index in range(1, 10):
			for side in ['S', 'E']:
				if side == 'S':
					south = index + 3
					if (south < 10):
						doorOp = html.OPTION("Closed door between rooms " + str(index) + " and " + str(south))
						aFollowUpSelect <= doorOp
				if side == 'E':
					east = index + 1
					if (east % 3 is not 1):
						doorOp = html.OPTION("Closed door between rooms " + str(index) + " and " + str(east))
						aFollowUpSelect <= doorOp					
		'''
		for index, room in enumerate(state["Rooms"]):
			for wall in room.walls.values():
				if wall.hasDoor:
					doorOp = html.OPTION("Close Door in room " + str(index + 1) + " on " + wall.loc + " wall.")
					aFollowUpSelect <= doorOp
		'''			
		aFollowUp <= aFollowUpSelect
		actionForm <= aFollowUp
		
	elif(action == "Played Sound"):
		aFollowUp <= "Sound Link:"
		textInput = html.INPUT(type="text", id="textInput", style = {"margin-left" : "10px"})
		aFollowUp <= textInput
		actionForm <= aFollowUp
		
	elif(action == "Displayed Message"):
		aFollowUp <= "Enter your message:"
		textInput = html.INPUT(type="text", id="textInput", style = {"margin-left" : "10px"})
		aFollowUp <= textInput
		actionForm <= aFollowUp
		
	elif(action == "Unsolved Puzzle"):
	
		aFollowUp <= "Pick a puzzle:"			
		puzzleOp = html.OPTION("Nothing Selected")
		aFollowUpSelect <= puzzleOp
			
		# Puzzles are gathered by searching rooms that have been placed
		# so the rules designer has context for which puzzles to attach conditions too
		for index, room in enumerate(state["Rooms"]):
			for wall in room.walls.values():
				#if wall.puzzle is not None:
				puzzleOp = html.OPTION("Unsolved puzzle in room " + str(index + 1) + " on " + wall.loc + " wall.")
				aFollowUpSelect <= puzzleOp
				
		aFollowUp <= aFollowUpSelect
		actionForm <= aFollowUp		
		
	elif(action == "Gained Points"):
		aFollowUp <= "Gain how many points?"
		textInput = html.INPUT(type="text", id="textInput", style = {"margin-left" : "10px"})
		aFollowUp <= textInput
		actionForm <= aFollowUp
		
	elif(action == "Lost Points"):
		aFollowUp <= "Lost how many points?"
		textInput = html.INPUT(type="text", id="textInput", style = {"margin-left" : "10px"})
		aFollowUp <= textInput
		actionForm <= aFollowUp
	else:
		pass #console.log("Debug: No Action Follow Up expected")	
	
def add_action_menu(state, sendBack):
		
	width = 200
	height = 200
	menu = create_menu("addActionMenu",width,height)
	
	actionTitle = html.P(id="addActionMenuTitle", style = {"margin-top" : '0'})
	actionTitle.innerHTML = "Add Action:"							
	
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
			if (action == "Opened Door" and aFollowUp is False
				or action == "Closed Door" and aFollowUp is False
				or action == "Displayed Message" and aFollowUp is False):
				alert("Not enough information was entered.")
			elif(action == "Played Sound" and not url_is_valid(textF)):
				alert("File link was invalid.")
			else:
				#console.log("Debug: Enough info was given.")
				
				destroy_menu("addActionMenu")
				
				enableOpSelect()
				
				# Make sure something was actually put into the text box
				if(textF is not None and textF.strip() != ''):
					# Change display of text box information based on action.
					if(action == "Displayed Message"):
						actionF = "Displayed Message: " + "\"" + textF + "\""
					elif(action == "Played Sound"):
						actionF = "Played sound from link: \"" + textF + "\""
					elif(action == "Gained Points"):
						actionF = "Gained " + textF + " Points"
					elif(action == "Lost Points"):
						actionF = "Lost " + textF + " Points"
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

def delete_condition_menu(state, index, sendBack):
		

	width = 200
	height = 200
	menu = create_menu("deleteConditionMenu",width,height)
	deleteTitle = html.P(id="deleteConditionTitle", style = {"margin-top" : '0'})
	deleteTitle.innerHTML = "Which condition?"
	

	conditionSelect = html.SELECT()
	conditionSelect <= html.OPTION("None Selected")
	conditionList = state["Rules"][index].conditions
	for condition in conditionList:
		conditionSelect <= html.OPTION(condition.text)
	
	def destroy():
		destroy_menu("deleteConditionMenu")
	
	def destroyAndSendBack():
		conditionName = conditionSelect.value
		if(conditionName == "None Selected"):
			alert("Select a condition to delete")
		else:
			destroy_menu("deleteConditionMenu")
			sendBack(conditionName)
			
	
	submit = html.BUTTON("Delete selected condition")
	submit.onclick = destroyAndSendBack
	
	cancel = html.BUTTON("Cancel", style = {'display' : 'block', 'margin' : '10px'})
	cancel.onclick = destroy
	
	
	menu <= deleteTitle
	menu <= conditionSelect
	menu <= submit
	menu <= cancel
	
	gui <= menu
	
def delete_action_menu(state, index, sendBack):
		

	width = 200
	height = 200
	menu = create_menu("deleteActionMenu",width,height)
	deleteTitle = html.P(id="deleteActionTitle", style = {"margin-top" : '0'})
	deleteTitle.innerHTML = "Which action?"
	

	actionSelect = html.SELECT()
	actionSelect <= html.OPTION("None Selected")
	actionList = state["Rules"][index].actions
	for action in actionList:
		actionSelect <= html.OPTION(action.text)
	
	def destroy():
		destroy_menu("deleteActionMenu")
	
	def destroyAndSendBack():
		actionName = actionSelect.value
		if(actionName == "None Selected"):
			alert("Select an action to delete")
		else:
			destroy_menu("deleteActionMenu")
			sendBack(actionName)
			
	
	submit = html.BUTTON("Delete Selected Action")
	submit.onclick = destroyAndSendBack
	
	cancel = html.BUTTON("Cancel", style = {'display' : 'block', 'margin' : '10px'})
	cancel.onclick = destroy
	
	
	menu <= deleteTitle
	menu <= actionSelect
	menu <= submit
	menu <= cancel
	
	gui <= menu
	
	
def edit_rule_menu(state, sendBack):
	
	width = 200
	height = 200
	menu = create_menu("editRuleMenu",width,height)
	
	editTitle = html.P(id="editRuleTitle", style = {"margin-top" : '0'})
	editTitle.innerHTML = "What would you like to do?"
	
	
	def processButton(input):
		def processButton2():
			sendBack(input)
			destroy_menu("editRuleMenu")
		return processButton2
	
	addAction = html.BUTTON("Add action to rule", style = {'display' : 'block', 'margin' : '10px'})
	addAction.onclick = processButton("addAction")
	
	addCondition = html.BUTTON("Add condition to rule", style = {'display' : 'block', 'margin' : '10px'})
	addCondition.onclick = processButton("addCondition")
	
	deleteAction = html.BUTTON("Delete action from rule", style = {'display' : 'block', 'margin' : '10px'})
	deleteAction.onclick = processButton("deleteAction")
	
	deleteCondition = html.BUTTON("Delete condition from rule", style = {'display' : 'block', 'margin' : '10px'})
	deleteCondition.onclick = processButton("deleteCondition")
	
	deleteRule = html.BUTTON("Delete rule", style = {'display' : 'block', 'margin' : '20px', 'font-weight' : 'bold'})
	deleteRule.onclick = processButton("deleteRule")
	
	cancel = html.BUTTON("Cancel", style = {'display' : 'block', 'margin' : '10px'})
	cancel.onclick = processButton("cancel")
	
	menu <= editTitle
	menu <= addAction
	menu <= addCondition
	menu <= deleteAction
	menu <= deleteCondition
	menu <= deleteRule
	menu <= cancel
	
	gui <= menu 
	
def open_or_closed_menu(sendBack):
	width = 200
	height = 200
	menu = create_menu("openOrClosedMenu",width,height)
	
	openOrClosedTitle = html.P("Should the door start open or closed?")
	
	open = html.INPUT(type="radio", name = 'direction', value = 'open', checked = True, style = {"display" : 'inline'} )
	closed = html.INPUT(type="radio", name = 'direction', value = 'closed', style = {"display" : 'inline'} )

	
	def destroy():
		destroy_menu("openOrClosedMenu")
		
	def destroyAndSendBack():
		sendBack(open.checked)
		destroy_menu("openOrClosedMenu")
	
	
	submit = html.BUTTON("Submit", style = {'margin' : '10px'})
	submit.onclick = destroyAndSendBack
	
	cancel = html.BUTTON("Cancel", style = {'margin' : '10px'})
	cancel.onclick = destroy
	
	menu <= openOrClosedTitle
	
	menu <= open
	menu <= html.P("Open", style = {'display' : 'inline', 'margin' : '0'})
	menu <= closed
	menu <= html.P("Closed", style = {'display' : 'inline', 'margin' : '0'})
	
	menu <= submit
	menu <= cancel
	
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
	global APANEL, board, PList
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
		
		# Display the SVG
		prepareSVG()
		
		# Remove old puzzle list if it exists
		# Append new puzzle list to Architect role
		remove_puzzle_list()
		create_puzzle_list(state)

		
		# Create the puzzle list so architect can tell which puzzles are which
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
		
# Puzzle list used for Architect to determine which puzzle is which		
def create_puzzle_list(state):

	boardDiv = document.getElementById("boarddivid")

	listDiv = html.DIV(id="puzzleListDiv", width = GAME_WIDTH, height = GAME_HEIGHT)
	puzzleList = html.OL(id="puzzleList")

	tableWrapper = html.DIV(id="tableWrapper", style = {'position' : 'relative', 'height' : 'auto'})
	scrollDiv = html.DIV(id="tableScroll", style = {'height' : str(GAME_HEIGHT) + 'px', 'overflow' : 'auto'})
	puzzleTable = html.TABLE(id="puzzleTable", style = {'width' : str(GAME_WIDTH) + 'px', 'font-size' : '13px','background-color' : 'rgb(220, 238, 251)' , 'text-align' : 'center'})
	headerRow = html.TR(id="puzzleHeaders", style = {'background-color' : 'rgb(200, 218, 231)'})
	
	headerRow <= html.TH("Number")
	headerRow <= html.TH("Puzzle")
	puzzleTable <= headerRow
	
	# Add puzzles to list
	i = 1
	for puzzle in state["Image_Puzzles"]:
		newRow = html.TR(id="puzzleRow"+ str(i))
		newRow <= html.TD(str(i))
		newRow <= html.TD(puzzle + " (Image Puzzle)")
		puzzleTable <= newRow
		i += 1
	for puzzle in state["Music_Puzzles"]:
		newRow = html.TR(id="puzzleRow"+ str(i))
		newRow <= html.TD(str(i))
		newRow <= html.TD(puzzle + " (Music Puzzle)")
		puzzleTable <= newRow
		i += 1
	
	puzzleTable.border = '10px solid white'
	boardDiv <= puzzleTable
	
# Removes a puzzle list if it has been created/exists
def remove_puzzle_list():
	puzzleTable = document.getElementById("puzzleTable")
	if(puzzleTable is not None):
		puzzleTable.parentNode.removeChild(puzzleTable)

	
# Called by the Architect role.
# Returns the corresponding puzzle index from the puzzle list.
# Used so Architect knows which puzzle they've placed is which
def getPuzzleIndex(puzzle):
	
	# Get current list of puzzle names
	puzzleTable = document.getElementById("puzzleTable")
	if(puzzleTable is not None):
		i = 0
		
		# Retrieves the name without the puzzle type description
		def getElementName(puzzle):
			name = ""
			paren = False
			i = 0
			while(paren == False and i < len(puzzle)):
				char = puzzle[i]
				nextChar = puzzle[i+1]
				if(nextChar == "("):
					paren = True
				else:
					name += char
				i += 1
			
			return name
			
		# Brython is being stupid so I have to do this 
		# really inefficient method, im so sorry
		onPuzzle = False
		i = 0
		name = ""
		number = None
		for row in puzzleTable:
			if(i > 0):
				for element in row:
					if(onPuzzle):
						name = getElementName(element.innerHTML)
						if(name == puzzle):
							return number
					else:
						number = element.innerHTML
					
					onPuzzle = not onPuzzle
			i += 1
		else:
			return None

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
			
		newRow = html.TR(id = "ruleRow" + str(index + 1))
		newRow <= html.TD(str(index+1), style = {'color' : "white"})
		
		conditionTD = html.TD()
		conditionP = None
		for condition in rule.conditions:
			if(condition.app):
				color = "white"
			else:
				color = "red"
			conditionP = html.P(condition.text + ", ", style = {'color' : color})
			conditionTD <= conditionP
		# Edge case
		if(conditionP is not None):
			conditionP.innerHTML = conditionP.innerHTML[:-2]
		
		actionTD = html.TD()
		actionP = None
		for action in rule.actions:
			if(action.app):
				color = "white"
			else:
				color = "red"
			actionP = html.P(action.text + ", ", style = {'color' : color})
			actionTD <= actionP
		# Edge case 
		if(actionP is not None):
			actionP.innerHTML = actionP.innerHTML[:-2]
		
		newRow <= conditionTD
		newRow <= actionTD

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
	remove_puzzle_list()
	
	musicDisplay.elt.style.display = "none"
	ruleDisplay.elt.style.display = "none"
	
	# Make canvas visible, call its JavaScript manager
	roleCanvas.elt.style.display = "block"
	setCanvasManager()
	
def prepareMusicDisplay():
	global roleCanvas, board, musicDisplay, ruleDisplay
	
	# Hide svg, roleCanvas
	board.elt.style.display = "none"
	remove_puzzle_list()
	
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
	remove_puzzle_list()
	
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
	global board
	
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
		
		if(wall.loc == 'E'):
			tx = x4 + (1/2) * (wall.x1 - x4)
			ty = wall.y1 + (1/2) * (wall.y2 - wall.y1) + 0.06
		else:
			tx = wall.x1 + (1/2) * (x4 - wall.x1)
			ty = wall.y1 + (1/2) * (wall.y2 - wall.y1) + 0.06
	
	elif (wall.loc == 'N' or wall.loc == 'S'):
		px1 += 1/PUZZLE_SIZE * (1/4)
		px2 -= 1/PUZZLE_SIZE * (1/4)
		px3 -= 1/PUZZLE_SIZE * (1/5)
		px4 += 1/PUZZLE_SIZE * (1/5)
		
		if(wall.loc == 'N'):
			tx = wall.x1 + (1/2) * (wall.x2 - wall.x1)
			ty = wall.y1 + (1/2) * (y3 - wall.y1) + 0.06
		else:
			tx = wall.x1 + (1/2) * (wall.x2 - wall.x1)
			ty = y4 + (1/2) * (wall.y1 - y4) + 0.06
	else:
		alert("drawPuzzle wall location check broke")
	
	# puzzle index number from puzzle list
	number = getPuzzleIndex(wall.puzzle)
	
	# Create puzzle polygon
	fill = "green"	
	puzzleDiv = create_polygon(px1,py1,px2,py2,px3,py3,px4,py4, fill = fill)

	APANEL <= puzzleDiv
	
	if(number is not None):
		textSvg = create_text(number,tx,ty)
		APANEL <= textSvg

# returns an svg text at the given point
def create_text(text, x, y, fontSize = "18"):
	(X1,Y1) = mapCoordsToDIV(x,y)
	textSvg = svg.text(text, x = X1, y = Y1, fill = "black", text_anchor = "middle", font_size = fontSize, font_weight = "bold")
	return textSvg

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
