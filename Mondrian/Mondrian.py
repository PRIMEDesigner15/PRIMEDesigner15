"""Mondrian.py
A SOLUZION problem formulation.
The XML-like tags used here may not be necessary, in the end.
But for now, they serve to identify key sections of this 
problem formulation.  It is important that COMMON_CODE come
before all the other sections (except METADATA), including COMMON_DATA.
"""
#<METADATA>
SOLUZION_VERSION = "0.1"
PROBLEM_NAME = "The Mondrian Design Problem"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ["S. Tanimoto"]
PROBLEM_CREATION_DATE = "08-JUN-2014"
PROBLEM_DESC=\
"""This version is mainly for the Brython version of the solving client
and the Brython version of Python.
However, it should all be generic Python 3, and this file is intended
to work a future Python+Tkinter client that runs on the desktop.
Anything specific to the Brython context should be in the separate 
file MondrianVisForBRYTHON.py, which is imported by this file when
being used in the Brython SOLUZION client."""
#</METADATA>

print("Hello from Mondrian.py (after METADATA)")

#<COMMON_DATA>
#</COMMON_DATA>

#<COMMON_CODE>


def copy_state(s):
  # Performs an appropriately deep copy of a state,
  # for use by operators in creating new states.
  news = {}
  boxlist = []
  for box in s["boxes"]:
    boxlist.append(box.copy())
  news["boxes"]=boxlist
  news["selected"]=s["selected"]
  return news

def describe_state(state):
  """ Produces a textual description of a state.
      Might not be needed in normal operation with GUIs."""
  txt = "\n"
  for box in state["boxes"]:
      txt += str(box) + "\n"
  txt += "selected: "+state["selected"]
  return txt

class MondRect:
  """A box that represents a basic structural element in this
     particular form of graphic art."""
  """It is important for the myjson.py module that the constructor
	 have arguments for each instance component, because it will
     use this __init__ method to reconstruct arbitrary instances
     for the class from json representations in a database.
     Except for the self argument and any keyword arguments,
     there must be a 1-to-1 correspondence between parameters
     in the __init__ method and the actual instance items."""
  #def __init__(self, x1, y1, x2, y2, parentRect=None, color="white"):
  def __init__(self, x1, y1, x2, y2, color):
    self.x1 = x1
    self.y1 = y1
    self.x2 = x2
    self.y2 = y2
    self.color = color
    #self.parentRect = parentRect # Not actually used in this version,
     # but which could be useful if a richer set of navigation operators
     # were to be added.
    #The parentRect field is problematic with the new SOLUZION, because
    # it sets up circular reference chains that break the JSON encoder/decoder.

  def setColor(self, color):
    self.color = color

  def subdivide(self, use_horizontal_divider, fraction):
    """This method returns a list of
     two new rectangles, obtained by subdividing, either
     horizontally or vertically, where the subdivision
     occurs so as to make the first rectangle have an
     area that is the given fraction of the original."""
    if use_horizontal_divider:
      ymid = self.y1 + fraction*(self.y2 - self.y1)
      R1 = MondRect(self.x1, self.y1, self.x2, ymid, self.color)
      R2 = MondRect(self.x1, ymid, self.x2, self.y2, self.color)
    else:
      xmid = self.x1 + fraction*(self.x2 - self.x1)
      R1 = MondRect(self.x1, self.y1, xmid, self.y2, self.color)
      R2 = MondRect(xmid, self.y1, self.x2, self.y2, self.color)
    return [R1, R2]
     
  def copy(self):
    #if (not hasattr(self, "parentRect")): self.parentRect = None
    #newb = MondRect(self.x1, self.y1, self.x2, self.y2, self.parentRect)
    newb = MondRect(self.x1, self.y1, self.x2, self.y2, self.color)
    return newb

def goal_test(s):
  """Somewhat arbirarily, we'll say a goal has been reached
     when the number of rectangles is at least 6."""
  nrect = len(s["boxes"])
  return nrect > 5

def goal_message(s):
  return "A masterpiece!"

class Operator:
  def __init__(self, name, precond, state_transf):
    self.name = name
    self.precond = precond
    self.state_transf = state_transf

  def is_applicable(self, s):
    return self.precond(s)

  def apply(self, s):
    return self.state_transf(s)

def selected_box_is_large_enough(s):
  sb = s["boxes"][s["selected"]]
  dx = sb.x2-sb.x1
  dy = sb.y2-sb.y1
  THRESHOLD = 0.04
  if dx < THRESHOLD: return False
  if dy < THRESHOLD: return False
  return True

def subdivide(state, hv, fraction):
  boxlist = state["boxes"]
  sel = state["selected"]
  selectedBox = boxlist[sel]
  horiz = True
  if hv=="vertical": horiz=False
  newBoxes = selectedBox.subdivide(horiz, fraction)
  newBoxList = boxlist[:sel]+newBoxes+boxlist[sel+1:]
  newState = copy_state(state)
  newState["boxes"]=newBoxList
  return newState

def change_selection(state, incr):
  newState = copy_state(state)
  newState["selected"] = int(newState["selected"])+incr
  return newState

def recolor(state, color):
  newState = copy_state(state)
  box = newState["boxes"][newState["selected"]]
  box.setColor(color)
  return newState
#</COMMON_CODE>

print("Hello from Mondrian.py (after COMMON_CODE)")


#<INITIAL_STATE>
INITIAL_STATE =\
  {"boxes":[MondRect(0.0, 0.0, 1.0, 1.0, "white")],
   # The list of boxes give a structural representation of the painting
   # The initial state has one large box, ready to be subdivided.
   "selected": 0}

# The following is some extra stuff for trying to make the template
# work with Javascript.

try:
  from browser import window, alert
  window.SOLUZION_INITIAL_STATE = INITIAL_STATE
  window.IS_JSON = json_encode(INITIAL_STATE)
  #alert("Inside of the template Mondrian.py, the INITIAL_STATE JSON is "+window.IS_JSON)
  #print(INITIAL_STATE)
except Exception as e:
  print("There was an exception when trying to communicate back from Python to Javascript.")
  print(e)

#</INITIAL_STATE>

print("Hello from Mondrian.py (after INITIAL_STATE)")

#<OPERATORS>
available_fractions = [0.25, 0.3333, 0.5, 0.6667, 0.75]
subdivision_operators =\
  [Operator("Divide with "+hv+" line at fraction "+str(f),
            lambda s: selected_box_is_large_enough(s),
            lambda s: subdivide(s, hv, f))
   for hv in ["horizontal", "vertical"]
   for f in available_fractions]
selection_operators =\
  [Operator("Select next box for alteration",
            lambda s: s["selected"] < len(s["boxes"])-1,
            lambda s: change_selection(s, 1)),
   Operator("Select previous box for alteration",
            lambda s: s["selected"] > 0,
            lambda s: change_selection(s, -1))]
color_operators =\
  [Operator("Recolor the selected box to "+color,
            lambda s: not color==s["boxes"][s["selected"]].color,
            lambda s: recolor(s, color))
  for color in ["white", "red", "blue", "yellow"]]
OPERATORS = subdivision_operators + selection_operators + color_operators
#</OPERATORS>
print("Hello from Mondrian.py (AFTER OPERATORS)")


#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>

#<STATE_VIS>
if "BRYTHON" in globals():
 from MondrianVisForBrython import set_up_gui as set_up_user_interface
 from MondrianVisForBrython import render_state_svg_graphics as render_state

# if 'TKINTER' in globals(): from MondrianVisForTKINTER import set_up_gui
#</STATE_VIS>

print("Goodbye from Mondrian.py (DONE LOADING IT)")

