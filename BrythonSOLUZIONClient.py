# BrythonSOLUZIONClient.py
# Ver 0.9, June 23, 2014.
# (C) S. Tanimoto, 2014

from browser import doc, alert, html, console
from PRIMEDesigner15VisForBrython import set_up_gui as set_up_user_interface
from PRIMEDesigner15VisForBrython import render_state_svg_graphics as render_state
from PRIMEDesigner15 import INITIAL_STATE


opSelect = None
STATE_STACK = []
RESET_BUTTON = None
BACKTRACK_BUTTON = None
Operators = INITIAL_STATE["Operators"]


if not 'PROBLEM_NAME' in globals():
	PROBLEM_NAME = "Problems"
  

#sdoc['pagetitle'].text = "Solving "+PROBLEM_NAME+\
#" in the Brython SOLUZION Client"'''

def set_up_Operators_interface():
	global opSelect # make available for interaction.
	opSelectdiv = html.DIV(Id="spselectdivid", style={"backgroundColor":"#AAFFFF"})
	opSelectdiv <= html.I("Operator selection:")
	opSelect = html.SELECT(Id="theoptselect")
	for i, elt in enumerate(Operators):
		opSelect <= html.OPTION(elt.name, value = i)
	applybutton = html.BUTTON(Id="applyButtonID")
	applybutton.text = "Apply selected operator"
	applybutton.bind('click',handleApplyButtonClick)
	opSelectdiv <= opSelect
	opSelectdiv <= applybutton
	return opSelectdiv  # A container to be inserted into the GUI.

def repopulate_operator_choices(current_state):
	global opSelect, Operators
	got_one_selected = False

	Operators = current_state["Operators"]
	
	opSelect.innerHTML = ''
	for i, elt in enumerate(Operators):
		opSelect <= html.OPTION(elt.name, value = i)
	
	#magic ziperino
	for item in opSelect:
		if Operators[int(item.value)].precond(current_state):
			item.disabled = False
			if not got_one_selected:
				item.selected = True
				got_one_selected = True
		else:
			item.disabled = True
			item.selected = False

def handleApplyButtonClick(evt):
	# get selected operator.
	global Operators, opSelect, current_state, STATE_STACK
	global BACKTRACK_BUTTON, RESET_BUTTON

	# Get Operators
	i = opSelect.selectedIndex
	op = Operators[i]
	try:
		new_state = op.state_transf(current_state)
		current_state = new_state
		render_state(current_state)
		STATE_STACK.append(new_state) # Push.
		BACKTRACK_BUTTON.disabled = False
		RESET_BUTTON.disabled = False
		if GOAL_TEST(current_state):
			# If the current state is a goal state, issue a message.
			# The message may be provided by the template.
			# Otherwise, we use a default message.
			global statusline
			if 'GOAL_MESSAGE_FUNCTION' in globals():
				mes = GOAL_MESSAGE_FUNCTION(current_state)
				statusline.text = mes
				alert(mes)
			else:
				mes = "Congratulations! You have reached a goal state."
				statusline.text = mes
				alert("You have achieved a goal state!")
		else:
			statusline.text = "Solving is in progress."
			repopulate_operator_choices(current_state)
	except (Exception) as e:
		alert("An error occured when applying this operator. Error: "+str(e))

opSelectdiv = set_up_Operators_interface()

def set_up_status_line():
	global gui, statusline
	statuslinediv = html.DIV(Id="statuslinediv", style={"backgroundColor":"#CCCCFF"})
	statuslabel = html.I("Status Line: ")
	statusline = html.B(Id="statustext")
	statusline.text="Solving Is Open"
	statuslinediv <= statuslabel
	statuslinediv <= statusline
	return statuslinediv

def handleresetbuttonclick(e):
	initialize()

def handlebacktrackbuttonclick(e):
	global current_state, STATE_STACK
	global RESET_BUTTON, BACKTRACK_BUTTON
	if len(STATE_STACK) > 2:
		STATE_STACK.pop()
		current_state = STATE_STACK[-1]
		render_state(current_state)
		repopulate_operator_choices(current_state)
	else: 
		initialize()

def set_up_reset_and_backtrack_div():
	global gui, reset_and_backtrack_div
	global RESET_BUTTON, BACKTRACK_BUTTON
	reset_and_backtrack_div =\
		html.DIV(Id="reset_and_backtrack_div", style={"backgroundColor":"#CCCCFF"})
	RESET_BUTTON = html.BUTTON(Id="RESET_BUTTONID")
	RESET_BUTTON.text = "Reset to initial state!"
	RESET_BUTTON.bind('click',handleresetbuttonclick)
	reset_and_backtrack_div <= RESET_BUTTON

	BACKTRACK_BUTTON = html.BUTTON(Id="BACKTRACK_BUTTONID")
	BACKTRACK_BUTTON.text ="Backtrack to previous state."
	BACKTRACK_BUTTON.disabled = True
	BACKTRACK_BUTTON.bind('click',handlebacktrackbuttonclick)
	reset_and_backtrack_div <= BACKTRACK_BUTTON

	return reset_and_backtrack_div

def initialize():
	global current_state, STATE_STACK
	global RESET_BUTTON, BACKTRACK_BUTTON
	current_state = INITIAL_STATE # comes from the problem template file.
	STATE_STACK = [INITIAL_STATE]
	render_state(current_state)
	repopulate_operator_choices(current_state)
	RESET_BUTTON.disabled = True
	BACKTRACK_BUTTON.disabled = True

statuslinediv = set_up_status_line()
set_up_user_interface(opSelectdiv, statuslinediv) # Handled in separate Python file.
reset_and_backtrack_div = set_up_reset_and_backtrack_div()
statuslinediv <= reset_and_backtrack_div

if not 'GOAL_TEST' in globals():
	def GOAL_TEST(s): return False # Default goal-testing function-can be overridden.

initialize()
