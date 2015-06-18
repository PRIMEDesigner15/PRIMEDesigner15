svgNS = "http://www.w3.org/2000/svg";

var board = document.createElementNS(svgNS,'svg');
board.setAttributeNS(null,'id','board');
board.setAttributeNS(null,'width','400');
board.setAttributeNS(null,'height','400');
board.setAttributeNS(null,'backgroundColor','#AAAABB');

var pattern = document.createElementNS(svgNS, "pattern");
pattern.setAttributeNS(null,'id','wallpaper');
pattern.setAttributeNS(null,'width','100%');
pattern.setAttributeNS(null,'height','100%');
pattern.setAttributeNS(null,'fill','#95B3D7');
pattern.setAttributeNS(null,'patternContentUnits','objectBoundingBox')

var img = document.createElementNS(svgNS, "image");
img.setAttributeNS(null,'id','image')
img.setAttributeNS("http://www.w3.org/1999/xlink",'xlink:href','force.jpg')
img.setAttributeNS(null,'width','1')
img.setAttributeNS(null,'height','1')
img.setAttributeNS(null,'preserveAspectRatio','none')


pattern.appendChild(img)
board.appendChild(pattern)
document.body.appendChild(board)


//svg.pattern(id="wallpaper", width = "100%", height= "100%", patternContentUnits = "objectBoundingBox")
//img = svg.image(xlink_href="force.jpg", width = "100", height = "100", preserveAspectRatio = "none")
//board = svg.svg(Id = "svgboard", 
//	style = {"width":400, "height":400,
//				"backgroundColor":"#AAAABB",})