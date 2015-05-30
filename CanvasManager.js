function CanvasManager(canvasId, imagePath) {
	this.canvasId = canvasId;
	this.imagePath = imagePath;
	this.img = document.createElement("img");
	this.img.src = this.imagePath;
	
	this.setURL = function(url) {
		this.imagePath = url
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
	}
	this.horizFlip = function() {
		var can = document.getElementById("roleCanvas");
		var ctx = can.getContext('2d');
		var imgData0;
		var imgData1;
		this.img.onload = function() {
			ctx.drawImage(this.img, 0, 0);
			imgData0 = ctx.getImageData(0,0,can.width,can.height);
			imgData1 = ctx.getImageData(0,0,can.width,can.height);
			for (var i = 0; i < can.width; i++) {
				for(var j = 0; j < can.height; j++) {
					for(var k = 0; k < 4; k++) {
						imgData1.data[(j * can.width) * 4 + i * 4 + k] = imgData0.data[j * can.width * 4 + (can.width - 1 - i) * 4 + k];
					}
				}
			}	
			ctx.putImageData(imgData1, 0, 0);
		}.bind(this);
	}
	this.rotate180 = function() {
		var can = document.getElementById("roleCanvas");
		var ctx = can.getContext('2d');
		var imgData0;
		var imgData1;
		this.img.onload = function() {
			ctx.drawImage(this.img, 0, 0);
			imgData0 = ctx.getImageData(0,0,can.width,can.height);
			imgData1 = ctx.getImageData(0,0,can.width,can.height);
			for (var i = 0; i < can.width; i++) {
				for(var j = 0; j < can.height; j++) {
					for(var k = 0; k < 4; k++) {
						imgData1.data[(j * can.width) * 4 + i * 4 + k] = imgData0.data[(can.height - 1 - j) * can.width * 4 + (can.width - 1 - i) * 4 + k];
					}
				}
			}
			ctx.putImageData(imgData1, 0, 0);
		}.bind(this);
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