window.onload = function() {console.log("CamanComms online")}

function CamanComms(canvasId, imagePath) {
	console.log("A CamanComm was made");
	this.canvasId = canvasId
	this.imagePath = imagePath
	this.CamanFunction = function(command) {
		console.log("camanfunction triggered");
		
		Caman(canvasId, imagePath, function() {
			this.brightness(-10).render();
		});
		//Caman(canvasId, function() {
		//	eval(command)});
	};
};