window.onload = function() {console.log("HELLO from CamanComms!")}

function CamanComms(canvasId, imagePath) {
	this.canvasId = canvasId
	this.imagePath = imagePath
	this.i = 0
	this.setURL = function(image) {
		this.imagePath = image
	};
	this.resetCamanImage = function() {
		nohashtagsallowed = canvasId.slice(1);
		document.getElementById(nohashtagsallowed).removeAttribute("data-caman-id");
	};
	this.CamanFunction = function(command) {
		Caman(this.canvasId, this.imagePath, function() {
			console.log(command)
			eval(command);
		});
	};
};