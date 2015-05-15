window.onload = function() {console.log("HELLO from CamanComms!")}

function CamanComms(canvasId, imagePath) {
	this.canvasId = canvasId
	this.imagePath = imagePath
	this.setURL = function(image) {
		this.imagePath = image
	};
	this.resetCamanImage = function() {
		nohashtagsallowed = canvasId.slice(1);
		document.getElementById(nohashtagsallowed).removeAttribute("data-caman-id");
	};
	this.CamanFunction = function(command) {
		alert("this.imagePath = " +this.imagePath)
		//alert("Image path outside function = " + imagePath)
		Caman(this.canvasId, this.imagePath, function() {
			//alert("Image path inside Caman = " + imagePath)
			console.log(command)
			eval(command);
			//this.initImage()
		});
	};
};