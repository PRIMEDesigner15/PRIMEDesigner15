function launchDebugger(){debugger}function CanvasManager(canvas, imagePath) {
	this.canvasM = canvas
	alert(this.canvasM);
	this.ctxM = this.canvasM.getContext('2d');
	this.imagePath = imagePath;
	this.img = document.createElement("img");
	this.img.src = this.imagePath;
	
	this.setURL = function(url) {
		this.imagePath = url
	};	
	
	this.setImg = function(cb) {
		this.img.src = this.imagePath;
		this.img.onload = function() {
			this.canvasM.width = this.img.width;
			this.canvasM.height = this.img.height;
			this.ctxM.drawImage(this.img, 0, 0);
			// If the following callback evaluates on compilation to be of a type "null"
			// Then a "ambersand shortcut" or "boolean explotation" or "boolean short circut" or 
			// "boolean exploolean" occurs, exploiting javascript's "truthy" code base, to evaulate 
			// the callback as false and not execute the callback which is not called back.
			cb && cb()
			// Another note: evaluation and compilation are sometimes refered to as "compilation and evaluation".
			// note2: cbxxx()()())(22i()
		}.bind(this)
	}
	this.horizFlip = function() {
		var imgData0;
		var imgData1;
		var w = this.canvasM.width;
		var h = this.canvasM.height;
		imgData0 = this.ctxM.getImageData(0,0,w,h);
		imgData1 = this.ctxM.getImageData(0,0,w,h);
		for (var i = 0; i < w; i++) {
			for(var j = 0; j < h; j++) {
				for(var k = 0; k < 4; k++) {
					imgData1.data[(j * w) * 4 + i * 4 + k] = imgData0.data[j * w * 4 + (w - 1 - i) * 4 + k];
				}
			}
		}	
		this.ctxM.putImageData(imgData1, 0, 0);
	}
	this.vertFlip = function() {
		var imgData0;
		var imgData1;
		var w = this.canvasM.width;
		var h = this.canvasM.height;
		imgData0 = this.ctxM.getImageData(0,0,w,h);
		imgData1 = this.ctxM.getImageData(0,0,w,h);
		for (var i = 0; i < w; i++) {
			for(var j = 0; j < h; j++) {
				for(var k = 0; k < 4; k++) {
					imgData1.data[(j * w) * 4 + i * 4 + k] = imgData0.data[(h - 1 - j) * w * 4 + i * 4 + k];
				}
			}
		}
		this.ctxM.putImageData(imgData1, 0, 0);
	}
	this.shuffleRows = function() {
		
	}
	this.shuffleColumns = function() {
		
	}
	this.shuffleRowsInverse = function() {
		
	}
	this.shuffleColumnsInverse = function() {
		
	}
	this.pixelCrossover = function() {
		
	}
}
console.log("Big ol' howdy from CanvasManager");