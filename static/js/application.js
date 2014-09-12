
function record() {
	console.log("Recording...");
};

function convert() {
	console.log("Converting...");
};

window.onload = function init() {
	$('#record-button').click(record);
	$('#convert-button').click(convert);
	console.log(document.location.href);
};
