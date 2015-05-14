window.onload = function() {console.log("HELLO from CamanComms!")}

function CamanComms(canvasId, imagePath) {
	this.canvasId = canvasId
	this.imagePath = imagePath
	this.CamanFunction = function(command) {
		Caman(canvasId, imagePath, function() {
			eval(command);
		});
	};
};