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
		for (var col = 0; col < w; col++) {
			for(var row = 0; row < h; row++) {
				for(var k = 0; k < 4; k++) {
					imgData1.data[(row * w + col) * 4 + k] = imgData0.data[(row * w + (w - 1 - col)) * 4 + k];
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
		for (var col = 0; col < w; col++) {
			for(var row = 0; row < h; row++) {
				for(var k = 0; k < 4; k++) {
					imgData1.data[(row * w + col) * 4 + k] = imgData0.data[((h - 1 - row) * w + col) * 4 + k];
				}
			}
		}
		this.ctxM.putImageData(imgData1, 0, 0);
	}
	
	this.shuffleRows = function() {
		var w = this.canvasM.width;
		var h = this.canvasM.height;
		var col0;
		var imgData0 = this.ctxM.getImageData(0,0,w,h);
		var imgData1 = this.ctxM.getImageData(0,0,w,h);		
		//console.log(w)
		for (var col = 0; col < w; col++) {
			col0 = 2 * col;
			if (col >= w / 2) {
				col0 = w - 1 - (2 * (w - 1 - col));
			}
			for (var row = 0; row < h; row++) {
				for (var k = 0; k < 4; k++) {
					imgData1.data[(row * w + col) * 4 + k] =
					imgData0.data[(row * w + col0) * 4 + k];
				}
			}
		}
		this.ctxM.putImageData(imgData1, 0, 0);
		
	}
	
	this.shuffleColumns = function() {
		var w = this.canvasM.width;
		var h = this.canvasM.height;
		var row0;
		var imgData0 = this.ctxM.getImageData(0,0,w,h);
		var imgData1 = this.ctxM.getImageData(0,0,w,h);		
		for (var row = 0; row < h; row++) {
			row0 = 2 * row;
			if (row >= h / 2) {
				row0 = h - 1 - (2 * (h - 1 - row));
			}
			for (var col = 0; col < w; col++) {
				for (var k = 0; k < 4; k++) {
					imgData1.data[(row * w) * 4 + col * 4 + k] = imgData0.data[(row0 * w) * 4 + col * 4 + k];
				}
			}
		}
		this.ctxM.putImageData(imgData1, 0, 0);		
	}
	
	this.shuffleRowsInverse = function() {
		var w = this.canvasM.width;
		var h = this.canvasM.height;
		var col0;
		var imgData0 = this.ctxM.getImageData(0,0,w,h);
		var imgData1 = this.ctxM.getImageData(0,0,w,h);	
		for (var col = 0; col < w; col++) {
			if (col % 2 == 1) {
				col0 = w - (w - col + 1) / 2;
			}
			else {
				col0 = col / 2;
			}
			for (var row = 0; row < h; row++) {
				for (var k = 0; k < 4; k++) {
					imgData1.data[(row * w + col) * 4 + k] = 
					imgData0.data[(row * w + col0) * 4 + k];
				}
			}
		}
		this.ctxM.putImageData(imgData1, 0, 0);
	}
	
	this.shuffleColumnsInverse = function() {
		var w = this.canvasM.width;
		var h = this.canvasM.height;
		var row0;
		var imgData0 = this.ctxM.getImageData(0,0,w,h);
		var imgData1 = this.ctxM.getImageData(0,0,w,h);	
		for (var row = 0; row < h; row++) {
			if (row % 2 == 1) {
				row0 = h - (h - row + 1) / 2;
			}
			else {
				row0 = row / 2;
			}
			for (var col = 0; col < w; col++) {
				for (var k = 0; k < 4; k++) {
					imgData1.data[(row * w + col) * 4 + k] = 
					imgData0.data[(row0 * w + col) * 4 + k];
				}
			}
		}
		this.ctxM.putImageData(imgData1, 0, 0);
	}
	
	this.pixelCrossover = function() {
		var w = this.canvasM.width;
		var h = this.canvasM.height;
		var w2 = parseInt(w / 2);
		var h2 = parseInt(h / 2);
		var imgData0 = this.ctxM.getImageData(0,0,w,h);
		var imgData1 = this.ctxM.getImageData(0,0,w,h);	
		
		for (var row = 0; row < h; row++) {
			row0 = (row + h2) % h;
			for (var col = 0; col < w; col++) {
				col0 = (col + w2) % w;
				for (var k = 0; k < 4; k++) {
						//result
						imgData1.data[(row * w + col) * 4 + k] =
						//left nibble of home pixel
						(imgData0.data[(row * w + col) * 4 + k] / 16) + 
						//right nibble of partner pixel * 16
						((imgData0.data[(row0 * w + col0) * 4 + k] % 16) * 16);
				}
			}
		}			
		this.ctxM.putImageData(imgData1, 0, 0);
	}
}


