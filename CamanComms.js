function CamanComms(canvasId) {
	this.canvasId = canvasId
};

CamanComms.prototype.darkenImg = function() {
	Caman(this.canvasId, function () {
		this.brightness(-20).render();
	});
};