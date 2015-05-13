window.onload = function() {console.log("CamanComms online")}

function CamanComms(canvasId) {
	console.log("A CamanComm was made")
	this.canvasId = canvasId
	this.CamanFunction = function(command) {
		console.log("camanfunction triggered")
		Caman(canvasId, eval(command))
	};
};