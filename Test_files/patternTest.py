from browser import window, document, html, alert, svg, console
from javascript import JSConstructor

def mapCoordsToDIV(x1,y1):
	return (x1,y1)

# returns an svg polygon at the given 4 points.
def create_polygon(x1,y1,x2,y2,x3,y3,x4,y4, fill = "black", stroke = "black", transform = "rotate(0)", id = "polygon"):
	
	# Maps points to Div
	(X1,Y1) = mapCoordsToDIV(x1,y1)
	(X2,Y2) = mapCoordsToDIV(x2,y2)
	(X3,Y3) = mapCoordsToDIV(x3,y3)
	(X4,Y4) = mapCoordsToDIV(x4,y4)
	
	# Create string of points for svg_polygon
	Points = str(X1) + "," + str(Y1) + " " + str(X2) + "," + str(Y2) + " " + str(X3) + "," + str(Y3) + " " + str(X4) + "," + str(Y4)
	
	# Create polygon
	poly = svg.polygon(id=id,fill = fill, stroke = stroke, stroke_width = "1",
					points=Points)				
	# return polygon
	return poly


x1 = 50
y1 = 50

x2 = 50
y2 = 150

x3 = 150
y3 = 150

x4 = 150
y4 = 50

board = svg.svg(Id = "svgboard",
	style = {"width":400, "height":400,
				"backgroundColor":"#AAAABB"})
window.addAttribute(board,"viewBox","0,0,400,400")


defs = svg.defs()
pattern = svg.pattern(id="wallpaper", width = "100%", height= "100%")
img = svg.image(xlink_href="force.jpg", width = "1", height = "1", transform = "translate(1,1) , rotate(180)")
window.addAttribute(pattern,"patternContentUnits","objectBoundingBox")
window.addAttribute(img,"preserveAspectRatio","none")

# Append
pattern <= img
board <= pattern

#img.transform = "rotate(180,1,1)"

#board = document.getElementById('board')
#img = document.getElementById('image')
#pattern = document.getElementById('pattern')

text1 = svg.text(str(x1) + " " + str(y1), x = x1, y=y1, fill  = "#FFFFFF")
text2 = svg.text(str(x2) + " " + str(y2), x = x2, y=y2, fill  = "#FFFFFF")
text3 = svg.text(str(x3) + " " + str(y3), x = x3, y=y3, fill  = "#FFFFFF")
text4 = svg.text(str(x4) + " " + str(y4), x = x4, y=y4, fill  = "#FFFFFF")
	
# Create string of points for svg_polygon
Points = str(x1) + "," + str(y1) + " " + str(x2) + "," + str(y2) + " " + str(x3) + "," + str(y3) + " " + str(x4) + "," + str(y4)
	
# Create polygon
WallpaperDiv = svg.polygon(id="no id",fill = "url(#wallpaper)", stroke = "black", stroke_width = "1",
					points=Points)


board <= WallpaperDiv
board <= text1
board <= text2
board <= text3
board <= text4
document <= board



