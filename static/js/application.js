
window.AudioContext = window.AudioContext || window.webkitAudioContext;

var audioContext = new AudioContext();
var audioRecorder = null;
var isRecording = false;

// Exports the recording as WAV and sends it to the server
function sheetify() {
    audioRecorder.exportWAV(sendToServer);
}

// Sends the WAV file to the server
function sendToServer( blob ) {
	var fd = new FormData();
	fd.append('title', 'hello');
	fd.append('song', blob, 'whistle.wav');
	$.ajax({
		url: '',
		type: 'POST',
		data: fd,
		processData: false,
		contentType: false
	}).done(receiveFromServer);
}

// Receives the song data from the server
function receiveFromServer(data) {
	window.location.replace('/sheet/' + data);
}

// Stops recording if recording, starts if not
function toggleRecording() {
	if (!audioRecorder) {
        return;
	} else if (isRecording) {
        console.log("Stopping recording");
        isRecording = false;
        audioRecorder.stop();
    } else {
        console.log("Starting recording");
        isRecording = true;
        audioRecorder.clear();
        audioRecorder.record();
    }
}

// Fancy WebAudioAPI magic
function gotStream(stream) {
    var inputPoint = audioContext.createGain();
    var audioInput = audioContext.createMediaStreamSource(stream);
    audioInput.connect(inputPoint);
    audioRecorder = new Recorder(inputPoint);
}

// Called when a user presses the record button
function record() {
	toggleRecording();
};

// Called when a user presses the convert button
function convert() {
	sheetify();
};

// Displays an error message for unsupported browsers
function displayUnsupportedBrowser() {
	alert("Your browser is not supported. Please try Chrome or Firefox.");
}


window.onload = function init() {
	// Button event bindings
	$('#record-button').click(record);
	$('#convert-button').click(convert);
	// Checks that getUserMedia is supported, raises an error if not
	if (!navigator.getUserMedia) {
        navigator.getUserMedia = navigator.webkitGetUserMedia || navigator.mozGetUserMedia;
    }
    if (navigator.getUserMedia) {
	    navigator.getUserMedia({audio:true}, gotStream, function(e) {
	        alert('Error getting audio');
	        console.log(e);
	    });
	} else {
		displayUnsupportedBrowser();
	};
};
