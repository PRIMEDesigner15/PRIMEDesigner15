# BrythonSOLUZIONClient.py
# Ver 0.9, June 23, 2014.
# (C) S. Tanimoto, 2014

from browser import doc, alert, html
OPSELECT = None
STATE_STACK = []
RESET_BUTTON = None
BACKTRACK_BUTTON = None

if not 'PROBLEM_NAME' in globals():
  PROBLEM_NAME = "Problems"

doc['pagetitle'].text = "Solving "+PROBLEM_NAME+\
" in the Brython SOLUZION Client"

def set_up_operators_interface():
  global OPSELECT # make available for interaction.
  global OPERATORS
  opselectdiv = html.DIV(Id="spselectdivid", style={"backgroundColor":"#AAFFFF"})
  opselectdiv <= html.I("Operator selection:")
  OPSELECT = html.SELECT(Id="theoptselect")
  for i, elt in enumerate(OPERATORS):
    OPSELECT <= html.OPTION(elt.name, value = i)
  applybutton = html.BUTTON(Id="applyButtonID")
  applybutton.text ="Apply selected operator"
  applybutton.bind('click',handleApplyButtonClick)
  opselectdiv <= OPSELECT
  opselectdiv <= applybutton
  return opselectdiv  # A container to be inserted into the GUI.

def find_applicable_op_indexes(OPERATORS, current_state):
  res = []
  for idx, op in enumerate(OPERATORS):
    try:
      pre = op.precond
    except:
      alert("No precondition for operator: "+str(op))
      return
    try:
      if pre(current_state):
      	res += [idx]
    except (Exception) as e:
      alert("Bad state or bad precondition with operator "+op.name+" and current state.")
  return res

def repopulate_operator_choices(choices):
  noptions = len(OPSELECT)
  got_one_selected = False
  for i in range(noptions):
    item = OPSELECT[i]
    if i in choices:
        item.disabled = False
        if not got_one_selected:
          item.selected = True
          got_one_selected = True
    else:
        item.disabled = True
        item.selected = False

def handleApplyButtonClick(evt):
  # get selected operator.
  global OPSELECT, CURRENT_STATE, STATE_STACK
  global BACKTRACK_BUTTON, RESET_BUTTON
  i = OPSELECT.selectedIndex
  op = OPERATORS[i]
  try:
    new_state = op.state_transf(CURRENT_STATE)
    CURRENT_STATE = new_state
    render_state(CURRENT_STATE)
    STATE_STACK.append(new_state) # Push.
    BACKTRACK_BUTTON.disabled = False
    RESET_BUTTON.disabled = False
    if GOAL_TEST(CURRENT_STATE):
      # If the current state is a goal state, issue a message.
      # The message may be provided by the template.
      # Otherwise, we use a default message.
      global statusline
      if 'GOAL_MESSAGE_FUNCTION' in globals():
        mes = GOAL_MESSAGE_FUNCTION(CURRENT_STATE)
        statusline.text = mes
        alert(mes)
      else:
        mes = "Congratulations! You have reached a goal state."
        statusline.text = mes
        alert("You have achieved a goal state!")
    else:
      statusline.text = "Solving is in progress."
    repopulate_operator_choices(find_applicable_op_indexes(OPERATORS, CURRENT_STATE))
  except (Exception) as e:
    alert("An error occured when applying this operator. Error: "+str(e))

opselectdiv = set_up_operators_interface()

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
  global CURRENT_STATE, STATE_STACK
  global RESET_BUTTON, BACKTRACK_BUTTON
  if len(STATE_STACK)>2:
    STATE_STACK.pop()
    CURRENT_STATE = STATE_STACK[-1]
    render_state(CURRENT_STATE)
    repopulate_operator_choices(find_applicable_op_indexes(OPERATORS, CURRENT_STATE))
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
  global CURRENT_STATE, INITIAL_STATE, STATE_STACK
  global RESET_BUTTON, BACKTRACK_BUTTON

  CURRENT_STATE = INITIAL_STATE # comes from the problem template file.
  STATE_STACK = [INITIAL_STATE]
  render_state(CURRENT_STATE)
  choices = find_applicable_op_indexes(OPERATORS, CURRENT_STATE)
  repopulate_operator_choices(choices)
  RESET_BUTTON.disabled = True
  BACKTRACK_BUTTON.disabled = True

statuslinediv = set_up_status_line()
set_up_user_interface(opselectdiv, statuslinediv) # Handled in separate Python file.
reset_and_backtrack_div = set_up_reset_and_backtrack_div()
statuslinediv <= reset_and_backtrack_div

if not 'GOAL_TEST' in globals():
  def GOAL_TEST(s): return False # Default goal-testing function-can be overridden.

initialize()
