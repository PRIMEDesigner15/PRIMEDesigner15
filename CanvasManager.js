function CanvasManager(canvas, imagePath) {
	this.canvasM = canvas
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
			
			//if a function "cb" is null then it is not run, otherwise it is run
			cb && cb()
		}.bind(this)
	}
	this.horizFlip = function() {
		var w = this.canvasM.width;
		var h = this.canvasM.height;
		var imgData0 = this.ctxM.getImageData(0,0,w,h);
		var imgData1 = this.ctxM.getImageData(0,0,w,h);
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
		var w = this.canvasM.width;
		var h = this.canvasM.height;
		var imgData0 = this.ctxM.getImageData(0,0,w,h);
		var imgData1 = this.ctxM.getImageData(0,0,w,h);
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
		var w = this.canvasM.width;
		var h = this.canvasM.height;
		var i0;
		var imgData0 = this.ctxM.getImageData(0,0,w,h);
		var imgData1 = this.ctxM.getImageData(0,0,w,h);		
		for (var i = 0; i < w; i++) {
			i0 = 2 * i;
			if (i >= w / 2) {
				i0 = w - 1 - (2 * (w - 1 - i0));
			}
			for (var j = 0; j < h; j++) {
				for (var k = 0; k < 4; k++) {
					imgData1.data[(j * w) * 4 + i * 4 + k] = imgData0.data[(j * w) * 4 + i0 * 4 + k];
				}
			}
		}
		this.ctxM.putImageData(imgData1, 0, 0);
	}
	this.shuffleColumns = function() {
		var w = this.canvasM.width;
		var h = this.canvasM.height;
		var j0;
		var imgData0 = this.ctxM.getImageData(0,0,w,h);
		var imgData1 = this.ctxM.getImageData(0,0,w,h);		
		for (var j = 0; j < h; j++) {
			j0 = 2 * j;
			if (j >= h / 2) {
				j0 = h - 1 - (2 * (h - 1 - j0));
			}
			for (var i = 0; i < w; i++) {
				for (var k = 0; k < 4; k++) {
					imgData1.data[(j * w) * 4 + i * 4 + k] = imgData0.data[(j0 * w) * 4 + i * 4 + k];
				}
			}
		}
		this.ctxM.putImageData(imgData1, 0, 0);		
	}
	this.shuffleRowsInverse = function() {
		var w = this.canvasM.width;
		var h = this.canvasM.height;
		var i0;
		var imgData0 = this.ctxM.getImageData(0,0,w,h);
		var imgData1 = this.ctxM.getImageData(0,0,w,h);	
		for (var i = 0; i < w; i++) {
			if (i % 2 == 1) {
				i0 = w - (w - i + 1) / 2;
			}
			else {
				i0 = i / 2;
			}
			for (var j = 0; j < h; j++) {
				imgData1.data[(j * w) * 4 + i * 4 + k] = imgData0.data[(j * w) * 4 + i0 * 4 + k];
			}
		}
		this.ctxM.putImageData(imgData1, 0, 0);
	}
	this.shuffleColumnsInverse = function() {
		
	}
	this.pixelCrossover = function() {
		
	}
}
console.log("Big ol' howdy from CanvasManager");