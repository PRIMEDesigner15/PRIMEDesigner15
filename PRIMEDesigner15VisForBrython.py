'''PRIMEDesignerVisForBrython.py

Set up a GUI and handle updates and events during a run of
the PRIMEDesigner template in the Brython environment.
'''

from browser import doc, html, alert, svg

ROOM_SIZE = 100
GAME_SIZE = ROOM_SIZE * 9
MARGIN = 20

print("Hello from PRIMEDesignerVisForBrython!  Starting to process it.")

LINE_WIDTH = 10
def set_up_gui(opselectdiv, statuslinediv):
	print("Entering set_up_gui in PRIMEDesignerVisForBrython.")
	global gui
	gui = html.DIV(Id="thegui")
	#setupboard
	gui <= opselectdiv
	gui <= statuslinediv
	doc <= gui
	print("Leaving set_up_gui in PRIMEDesignerVisForBrython.")

def draw(state):
	for room in state:
		draw(room)
		
def draw(room):
	for wall in room.walls:
		draw(wall)

def draw(wall):
	draw wall.wallpaper

def draw(wallpaper):
	# Create 2 more points to form a trapezoidal false 3d shape.
	def THICKNESS = .2
	def x3 = wallpaper.x1 + .2/math.sqrt(2)
	def y3 = wallpaper.y1 + .2/math.sqrt(2)
	def x4 = x2 - .2/math.sqrt(2)
	def y3 = y4
	
	
	
	