
window.AudioContext = window.AudioContext || window.webkitAudioContext;

var audioContext = new AudioContext();
var audioRecorder = null;
var isRecording = false;
var recordButton = $('#record-button');
var convertButton = $('#convert-button');


// Gets the value from the input given the id of the input
// Will use the placeholder text if the input is empty
//   input_id: id of the input as a String
//   default_val: String to set as the value if no value or
//                placeholder text is found
function getValueFromInput(input_id, default_val) {
	var value = $(input_id).val();
	if (!value || value === '') {
		value = $(input_id).attr("placeholder") || default_val;
	}
	return value;
}


// Enables/disables a button given a jQuery selector
//   button: jQuery selector of a button

function elementIsEnabled(elem) {
	return !elem.attr('disabled');
}

function enableElement(elem) {
	if (!elementIsEnabled(elem)) {
		elem.removeAttr('disabled');
	}
}

function disableElement(elem) {
	if (elementIsEnabled(elem)) {
		elem.attr('disabled', 'disabled');
	}
}


// Exports the recording as WAV and sends it to the server
function sheetify() {
	$("#record-container").hide();
	$("#upload-container").show();
    audioRecorder.exportWAV(sendToServer);
}

// Makes a FormData instance given the audio blob
// Takes other values from the input fields
function makeFormData(blob) {
	var fd = new FormData();
	var title = getValueFromInput('#input-title', 'My Masterpiece');
	var composer = getValueFromInput('#input-composer', 'Beethoven');
	var bpm = getValueFromInput('#input-bpm', '135');
	fd.append('title', title);
	fd.append('composer', composer);
	fd.append('bpm', bpm);
	fd.append('song', blob, 'whistle.wav');
	return fd;
}

// Sends the WAV file to the server
function sendToServer( blob ) {
	var fd = makeFormData(blob);
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
	// window.location.replace('/sheet/' + data);
	$('#upload-container').hide();
	$('#download-container').show();
	$('#download-link').attr('href', '/sheet/' + data);
}

// Stops recording if recording, starts if not
function toggleRecording() {
	if (!audioRecorder) {
        return;
	} else if (isRecording) {
        recordButton.html('<i class="fa fa-microphone fa-lg"></i><h3>Record</h3>');
        enableElement(convertButton);
        isRecording = false;
        audioRecorder.stop();
    } else {
        recordButton.html('<i class="fa fa-microphone fa-lg"></i><h3>Stop Recording</h3>');
        disableElement(convertButton);
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
    enableElement(recordButton);
}

// Called when a user presses the record button
function record() {
	toggleRecording();
};

// Called when a user presses the convert button
function convert() {
	sheetify();
};

// Calle when the next button on the information screen is pressed
function infoNext() {
	$('#information-container').hide();
	$('#record-container').show();
}

// Displays an error message for unsupported browsers
function displayUnsupportedBrowser() {
	$('#error-container').html('<div class="alert" role="alert"><strong>Your browser is not supported.</strong> Please try <a href="https://www.google.com/chrome/browser/">Chrome</a> or <a href="https://www.mozilla.org/en-US/firefox/new/">Firefox</a>.</div><br>');
	disableElement($('#input-title'));
	disableElement($('#input-composer'));
	disableElement($('#input-bpm'));
}

// Initially hides all the other containers from the page
function hideInitialContainers() {
	$('#record-container').hide();
	$('#upload-container').hide();
	$('#download-container').hide();
}


window.onload = function init() {
	// Button event bindings and initial disabling
	recordButton.click(record).attr('disabled', 'disabled');
	convertButton.click(convert).attr('disabled', 'disabled');
	// Set up information next button
	hideInitialContainers();
	$('#info-next-button').click(infoNext);
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
