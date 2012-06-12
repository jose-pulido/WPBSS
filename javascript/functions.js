/*JAVASCRIPT CODE*/

var validate_size = 1048576;		// Global variable. Limits the size of the verification chunk [1MB] for big files

function ValidateDescriptionLine(lines, curLine){
	//future description-line processing -> validated = 1 OR validated = -4

	//after a description line, it can't be found another description line
	var nextline = lines[curLine+1];
	if (nextline[0]==">"){
		return -2;
	}else{
		return 1;	
	}		
}

function ValidateDataLine(testline){
	var regEx = /[^A|^C|^G|^T|^N|^-]/i;	// The chars allowed are 'A', 'C', 'G', 'T', 'N' and '-'. 
	testline = testline.toUpperCase();
	if (testline.match(regEx)==null){	// If everything is ok, match function doesn't match any other char and return null
		return 1;			// Because you can't use length method of null, I evaluate this condition
	}else{
		return -3;			// If there's any different char, match function return it and testline.match(regEx).length = 1
	}
}

function abortRead() {
	reader.abort();
}

function myclick() {
	//validate_size = 1048576;
	document.getElementById('file').onchange = function() {
		document.getElementById("validating").className = 'unhidden';
		ValidateSlicer(this.files[0], validate_size);
		document.getElementById("file").className = 'hidden';
	};
}


function validateFasta(data, file) {
	var validated = 1;
	//validate_size = 1048576;
	var lines = data.split("\n");		// splits the original string in several strings (array) using return as separator. 
	curLine = 0
	if (lines[curLine][0]!=">"){		// First line must be a description line
		validated = -1;

	}else if ( (file.size<validate_size) && (lines[lines.length-2][0]==">") ) {

		validated = -5;	
	}else{
			
	}
	while ( (validated==1) && (curLine < lines.length-2) ){			// Should be lenght-1, but always take one last blank line
		var testline = lines[curLine];

		if (testline[0] == ">") {					// check if it's a description line
			validated = ValidateDescriptionLine(lines, curLine);
			curLine++;
		}else {								// if it is not a description line, it should be a data line
			validated = ValidateDataLine(testline);
			curLine++;
		}
	}

	document.getElementById("validating").className = 'hidden'; // hide the validating gif wheel
	document.getElementById("uploadiv").className = 'unhidden'; // make visible the <div> element for the next step
	var validateMessage = "";
	switch (validated){				// Error management
		case 1:
			validateMessage = " successfully validated";			
			break;
		case -1:
			validateMessage = " Error during the validation: file must begin with a description line (> symbol). ";			
			break;
		case -2:
			validateMessage = " Error during the validation: There can't be consecutive description lines. ";			
			break;
		case -3:
			validateMessage = " Error during the validation: Invalid data line. Only A,C,T,G,N and - chars are allowed. ";			
			break;
		case -4:
			validateMessage = " Error during the validation: Description line has inappropriate format. ";			
			break;
		case -5:
			validateMessage = " Error during the validation: Less than 1MB files can't end with description line. ";			
			break;
		default:
			validateMessage = " Error during the validation: Something strange happened. ";			
			break;
	}
	if (validated==1) {
		
		document.getElementById('uploadiv').innerHTML = '<img id="tick" src="http://127.0.0.1/html5/images/green_tick.jpg" />' + 
		'&nbsp;' + file.name + validateMessage + 
		'<input type="submit" id="uploadFASTA" value="Upload" class="unhidden"/>';
		
	}else{
		document.getElementById('uploadiv').innerHTML = '<img id="tick" src="http://127.0.0.1/html5/images/red_tick.jpg" />' +
		'&nbsp;' + file.name + validateMessage +" Choose another one file &nbsp;" + 
		'<input type="file" id="file" onclick="myclick();" name="file" class="unhidden"/>';
	}
}

	
function ValidateSlicer(file, validate_size) {
	
	var reader = new FileReader();
	var data=[];

	if (file.size < validate_size) {
		var mysize = file.size;
	} else {
		var mysize = validate_size;
	}

	 // split first N bytes of the file
	if (file.webkitSlice) {
		var blob = file.webkitSlice(0, mysize);
	} else if (file.mozSlice) {
		var blob = file.mozSlice(0, mysize);
	}
	reader.readAsText(blob);
	reader.onloadend = function(evt) {
		if (evt.target.readyState == FileReader.DONE) { // DONE == 2
			mydata=evt.target.result;
			//alert(mydata);
			validateFasta(mydata, file);	      
		}//if
	}; //reader.onloadend

	reader.onerror = function() {
		alert('Unable to read ' + file.fileName);
	};
}
