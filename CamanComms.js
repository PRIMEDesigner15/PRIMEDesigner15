
var globalImg = [];
var globalCounter = 0;

function PixelWrapper(r,g,b,a) {
	
	this.r = r;
	this.g = g;
	this.b = b;
	this.a = a;
	
};

function CamanComms(canvasId, imagePath) {
	this.canvasId = canvasId
	this.imagePath = imagePath
	this.setURL = function(url) {
		this.imagePath = url
	};
	this.resetCamanImage = function() {
		nohashtagsallowed = canvasId.slice(1);
		document.getElementById(nohashtagsallowed).removeAttribute("data-caman-id");
	};
	this.CamanFunction = function(command) {
		Caman(this.canvasId, this.imagePath, function() {
			eval(command);
		});
	};
	this.CamanFlip180 = function() {

		Caman(this.canvasId, this.imagePath, function () {
			var w = this.imageWidth()
			var h = this.imageHeight()
			alert("width = " + this.imageWidth())
			for(var x = 1; x < w + 1; x++) {
				globalImg[x] = [];
			}
			alert("globalImg has space!")
			console.log(globalImg)
			globalImg[1].push(new PixelWrapper(100,101,102,103));
			console.log(globalImg)
			/*this.getPixels("test");
			console.log(globalImg)
			alert("globalImg is full of pixels!")
			
			var flippedImg = []
			for(var x = 1; x < w + 1; x++) {
				flippedImg[x] = [];
				for(var y = 1; y < h + 1; y++) {
					flippedImg[x][y] = globalImg[w + 1 - x][h + 1 - y]
				}
			}
			
			alert("we made a flipped img!")
			globalImg = flippedImg
			alert("we gave the flipped img to the glbal one")
			this.putPixels().render();
			alert("we put them into the caman pixels")
			this.render();*/
		});
	};
};

window.onload = function() {
	
	Caman.Pixel.prototype.coordinatesToLocation = Caman.Pixel.coordinatesToLocation
    Caman.Pixel.prototype.locationToCoordinates = Caman.Pixel.locationToCoordinates
	Caman.Pixel.prototype.putPixelRelative = function(horiz, vert, rgba) {
	  var newLoc;   // this variable is now consistently named, not newLoc and nowLoc

      if (this.c == null) {
        throw "Requires a CamanJS context";
      }
      newLoc = this.loc + (this.c.dimensions.width * 4 * (vert * -1)) + (4 * horiz);
      if (newLoc > this.c.pixelData.length || newLoc < 0) {
        return;
      }
      this.c.pixelData[newLoc] = rgba.r;
      this.c.pixelData[newLoc + 1] = rgba.g;
      this.c.pixelData[newLoc + 2] = rgba.b;
      this.c.pixelData[newLoc + 3] = rgba.a;
      return true;
    };
	
	Caman.Filter.register("getPixels", function (test) {
		this.process("getPixels", function (rgba) {
			Y = rgba.locationXY().y; // e.g. {x: 0, y: 0}
			alert("r = " + rgba.r);
			globalImg[Y].push(new PixelWrapper(rgba.r,rgba.g,rgba.b,rgba.a));
		});
		return this;
	});
	
	Caman.Filter.register("putPixels", function () {
		this.process("putPixels", function (rgba) {
			X = rgba.locationXY().x; // e.g. {x: 0, y: 0}
			Y = rgba.locationXY().y;
			//console.log(globalImg[X,Y])
			rgba.putPixel(X, Y, {r : globalImg[X,Y].r, g : globalImg[X,Y].g,
						b : globalImg[X,Y].b, a : globalImg[X,Y].a});
		});
		return this;
	});
	console.log("HELLO from CamanComms!")
};