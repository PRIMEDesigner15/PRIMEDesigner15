'''MondrianVisForBrython.py

Set up a GUI and handle updates and events during a run of
the Mondrian template in the Brython environment.
'''
from browser import doc, html, alert, svg
# Not used in the new client:
#from Mondrian import *

gui = None
board=statusline=opselect=None
APANEL = None
# The following control the layout of the TOH state displays.
MARGIN = 20

PAINTING_HEIGHT = 400
PAINTING_WIDTH  = 600

LAST_STATE = None # cache of current state for use in refresh of display after selection hiding button click.

print("Hello from MondrianVisForBrython!  Starting to process it.")

LINE_WIDTH = 10
def set_up_gui(opselectdiv, statuslinediv):
  print("Entering set_up_gui in MondrianVisForBrython.")
  global gui
  gui = html.DIV(Id="thegui")
  #set_up_board_ascii_art()
  set_up_board_svg_graphics()
  #alert("SVG stuff should now be set up.")
  gui <= opselectdiv
  gui <= statuslinediv
  doc <= gui
  print("Leaving set_up_gui in MondrianVisForBrython.")

# The following is not used in the SVG graphics version of the display.
def set_up_board_ascii_art():
  global gui, board
  boarddiv = html.DIV("Current state", Id="boarddivid", 
                      style={"backgroundColor":"#CCFFCC"})
  board = html.TEXTAREA(Id="board", style={"width":100, "height":100})
  boarddiv <= board
  gui <= boarddiv

def set_up_board_svg_graphics():
  # alternative graphics method.
  global APANEL, SHOW_SELECTION_Button, board
  boarddiv = html.DIV(Id="boarddivid", style={"backgroundColor":"#CCFFCC"})
  boarddiv <= html.I("Puzzle state:")
  APANEL = svg.g(Id="panel")
  board = svg.svg(Id="svgboard", 
                  style={"width":PAINTING_WIDTH, "height":PAINTING_HEIGHT, 
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

def render_state_ascii_art(s):
  t = describe_state(s)
  global board
  board.text = t

def mapCoordsToDIV(x, y):
  '''Convert x coordinate from the range [0.0, 1.0] to
     the range [MARGIN, PAINTING_WIDTH - MARGIN], and
     the y coordinate to the range [MARGIN, PAINTING_HEIGHT - MARGIN].'''
  global PAINTING_WIDTH, PAINTING_HEIGHT
  newX = int(MARGIN + x*(PAINTING_WIDTH - 2*MARGIN))
  newY = int(MARGIN + y*(PAINTING_HEIGHT - 2*MARGIN))
  return (newX, newY)

def render_state_svg_graphics(state):
  global APANEL, LINE_WIDTH, board
  # Clear out any graphic elements from a previous state display:
  # Note: This method doesn't work correctly, due to possible automatic
  # restructuring of part of the DOM, and subsequent failure to remove
  # all of the graphic elements consistently:
    #for idx, child in enumerate(APANEL): APANEL.removeChild(APANEL.lastChild)
  # The following line was used for testing:
    #print("Removed "+str(idx)+" elements")
  # The following method works fine:
  while APANEL.lastChild:
    APANEL.removeChild(APANEL.lastChild)
  # Draw all the boxes.
  for box in state['boxes']:
    (X1, Y1) = mapCoordsToDIV(box.x1, box.y1)
    (X2, Y2) = mapCoordsToDIV(box.x2, box.y2)
    rect_style = {"stroke":"black", "stroke-width": LINE_WIDTH}
    rect = svg.rect(x=X1,y=Y1, width=X2-X1, height=Y2-Y1, fill=box.color,
                    style=rect_style)
    APANEL <= rect

  # Highlight selected box if that option is on.
  global SHOWING_SELECTION
  if SHOWING_SELECTION:
    selected_box = state['boxes'][state['selected']]
    b = selected_box
    (X1, Y1) = mapCoordsToDIV(b.x1, b.y1)
    (X2, Y2) = mapCoordsToDIV(b.x2, b.y2)
    selected_rect_style = {"stroke": "#8800CC", "stroke-width": LINE_WIDTH/2}
    selected_rect = svg.rect(x=X1,y=Y1, width=X2-X1, height=Y2-Y1, fill=b.color,
                             style=selected_rect_style)
    APANEL <= selected_rect
    diagline_style = {"stroke": "green", "stroke-width": LINE_WIDTH}
    diagline = svg.line(x1=X1,y1=Y1, x2=X2, y2=Y2,
                    style=diagline_style)
    APANEL <= diagline

  global LAST_STATE
  LAST_STATE = state
  window.makeNeededPNGs(board)
