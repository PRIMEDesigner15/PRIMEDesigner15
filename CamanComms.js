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
	console.log("HELLO from CamanComms!")
}


	
function CamanComms(canvasId, imagePath) {
	this.canvasId = canvasId
	this.imagePath = imagePath
	this.i = 0
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
	this.Caman180Flip = function() {
		Caman.Filter.register("example", function (adjust) {
	  this.process("example", function (rgba) {
		rgba.locationXY(); // e.g. {x: 0, y: 0}

		// Gets the RGBA object for the pixel that is 2 rows down
		// and 3 columns to the right.
		rgba.getPixelRelative(-2, 3);

		// Sets the color for the pixel that is 2 rows down and
		// 3 columns to the right.
		rgba.putPixelRelative(-2, 3, {
		  r: 100,
		  g: 120,
		  b: 140,
		  a: 255
		});

		// Gets the RGBA object for the pixel at the given absolute
		// coordinates. Rgba is relative to the top left corner.
		rgba.getPixel(20, 50);

		// Sets the color for the pixel at the given absolute coordinates.
		// Also relative to the top left corner.
		rgba.putPixel(20, 50, {
		  r: 100,
		  g: 120,
		  b: 140,
		  a: 255
		});
	  });
	  return this;
	});


		Caman(this.canvasId, function () {

		  // // this works
		  this.brightness(5).render();
		  alert("brightened")
		  // this doesn't :(
		  this.example().render();
		});
		/*myCaman = Caman(this.canvasId, function() {});
		Caman.Filter.register("Flip180", function (adjust) {
			console.log(this.getPixel(10,15));
			this.process("Flip180", function(this) {
				return this
			});
		});
		myCaman.Flip180("test");
		var height = myCaman.imageHeight();
		var width = myCaman.imageWidth();
		console.log("height: " + height + " width: " + width);
		console.log(myCaman.getPixel(10,15));
		/*var originalImg = [[],[]];
		for(var x = 0; x < w; x++) {
			for(var y = 0; y < h; y++) {
				originalImg[x][y] = myCaman.Pixel.getPixel(x,y)
			}
		}
		*/
	}
};