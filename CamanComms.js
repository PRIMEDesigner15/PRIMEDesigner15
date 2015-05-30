
var globalImg = [];
var globalCounter = 0;

function PixelWrapper(r,g,b,a) {
	
	this.r = r;
	this.g = g;
	this.b = b;
	this.a = a;
	
};

function once(f) {
	var called = false;
	var returnValue;
	return function() {
		if(called) {
			return returnValue;
		}
		called = true;
		return returnValue = f.apply(this, arguments);
	};
}

function CamanComms(canvasId, imagePath) {
	this.canvasId = canvasId;
	this.imagePath = imagePath;
	this.img = document.createElement("img");
	this.img.src = this.imagePath;
	this.nohashtagsallowed = this.canvasId.slice(1);
	this.setURL = function(url) {
		this.imagePath = url
	};
	this.resetCamanImage = function() {
		document.getElementById(this.nohashtagsallowed).removeAttribute("data-caman-id");
	};
	this.CamanFunction = function(command) {
		Caman(this.canvasId, this.imagePath, function() {
			eval(command);
		});
	};
	this.setImg = function() {
		this.img.src = this.imagePath;
		var canImg = this.img;
		this.img.onload = function() {
			var can = document.getElementById("roleCanvas");
			can.width = canImg.width;
			can.height = canImg.height;
			var ctx = can.getContext('2d');
			ctx.drawImage(canImg, 0, 0);
		}
		//alert("setImg")
	}
	this.rotate180 = function() {
		var can = document.getElementById("roleCanvas");
		var ctx = can.getContext('2d');
		var imgData0;
		var imgData1;
		var canImg = this.img;
		canImg.onload = function() {
			ctx.drawImage(canImg, 0, 0);
			imgData0 = ctx.getImageData(0,0,300,300);
			imgData1 = ctx.getImageData(0,0,300,300);
			for (var i = 0; i < can.width; i++) {
				for(var j = 0; j < can.height; j++) {
					for(var k = 0; k < 4; k++) {
						imgData1.data[(j * can.width) * 4 + i * 4 + k] = imgData0.data[(can.height - 1 - j) * can.width * 4 + (can.width - 1 - i) * 4 + k];
					}
				}
			}
			ctx.putImageData(imgData1, 0, 0);
		}
	}

	this.CamanFlip180 = function() {
		Caman(this.canvasId, this.imagePath, function () {
			var w = this.imageWidth()
			var h = this.imageHeight()
			for(x = 1; x < w + 1; x++) {
				globalImg[x] = [];
			}
			//globalImg[1].push(new PixelWrapper(100,101,102,103));
			Caman.Event.listen(this, "processComplete", once(function () {
				console.log("getpixels done");
				console.log(globalImg[5][5]);
				//console.log(globalImg[5]);
				//console.log(globalImg);
				var flippedImg = []
				for(x = 1; x < w + 1; x++) {
					flippedImg[x] = [];
					for(y = 1; y < h + 1; y++) {
						flippedImg[x][y] = globalImg[w + 1 - x][h + 1 - y]
					}
				}
				//console.log(flippedImg);
				globalImg = flippedImg;
				Caman.Event.listen(this, "processComplete", once(function() {
					console.log("putpixels is done");
					this.render();
				}));
				this.putPixels();
			}));
			this.getPixels();
		});	
	};
};

	
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

Caman.Filter.register("getPixels", function () {
	this.process("getPixels", function (rgba) {
		Y = rgba.locationXY().y; // e.g. {x: 0, y: 0}
		//alert("r = " + rgba.r);
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
