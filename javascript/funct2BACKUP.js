/*JAVASCRIPT CODE*/

var validate_size = 1048576;		// Global variable. Limits the size of the verification chunk [1MB] for big files
var validateFASTA = 0;
var validateMATRIX = 0;

function abortRead() {
	reader.abort();
}

/**********************************************************/
/**************************FASTA****************************/
/**********************************************************/

function myFASTA(validatingDIV, fileid, uploadBUTTON) {
	document.getElementById(fileid).onchange = function() {
		document.getElementById(validatingDIV).className = 'unhidden';
		SlicerFASTA(this.files[0], validate_size, validatingDIV, fileid, uploadBUTTON);		
	};
}
	
function SlicerFASTA(file, validate_size, validatingDIV, fileid, uploadBUTTON) {
	
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
			var mydata=evt.target.result;
			validateFasta(mydata, file, validatingDIV, fileid, uploadBUTTON);	      
		}//if
	}; //reader.onloadend

	reader.onerror = function() {
		alert('Unable to read ' + file.fileName);
	};
}

                   /*VALIDATINGFASTA FUNCTIONS*/

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

function validateFasta(data, file, validatingDIV, fileid, uploadBUTTON) {
	var validated = 1;
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

		if (testline[0] == ">") {									// check if it's a description line
			validated = ValidateDescriptionLine(lines, curLine);
			curLine++;
		}else {								// if it is not a description line, it should be a data line
			validated = ValidateDataLine(testline);
			curLine++;
		}
	}

	var validateMessage = "";		// Error management
	switch (validated){				
		case 1:
			validateMessage = " - successfully validated";			
			break;
		case -1:
			validateMessage = " - Error during the validation: file must begin with a description line (> symbol). ";			
			break;
		case -2:
			validateMessage = " - Error during the validation: There can't be consecutive description lines. ";			
			break;
		case -3:
			validateMessage = " - Error during the validation: Invalid data line. Only A,C,T,G,N and - chars are allowed. ";			
			break;
		case -4:
			validateMessage = " - Error during the validation: Description line has inappropriate format. ";			
			break;
		case -5:
			validateMessage = " - Error during the validation: Less than 1MB files can't end with description line. ";			
			break;
		default:
			validateMessage = " - Error during the validation: Something strange happened. ";			
			break;
	}
	validateFASTA = validated;
	makingFastaDIV(file, validatingDIV, fileid, uploadBUTTON, validateMessage, validateFASTA);
	if ( (validateFASTA==1) &&  (validateMATRIX==1) ) {
		document.getElementById(uploadBUTTON).className = 'unhidden';
	}
}


/************************************************************/
/**************************MATRIX****************************/
/************************************************************/

function myMATRIX(validatingDIV, fileid, uploadBUTTON) {
	document.getElementById(fileid).onchange = function() {
		document.getElementById(validatingDIV).className = 'unhidden';
		 SlicerMATRIX(this.files[0], validate_size, validatingDIV, fileid, uploadBUTTON);		
	};
}
	

function SlicerMATRIX(file, validate_size, validatingDIV, fileid, uploadBUTTON) {
	
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
			var mydata=evt.target.result;
			validateMatrix(mydata, file, validatingDIV, fileid, uploadBUTTON);	      
		}//if
	}; //reader.onloadend

	reader.onerror = function() {
		alert('Unable to read ' + file.fileName);
	};
}

                   /*VALIDATINGMATRIX FUNCTIONS*/

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

function LocateHeaders(lines) {
	var header_index = 0;
	var myHeaders = [];
	for (var i=0; i<(lines.length -1);i++){
		if lines[i][0] ==">" {
			myHeaders[header_index] = i;
			header_index++;
		}
	}
	return myHeaders;
}

function FindFormat(lines) {
	var format ="";
	if (lines[0][0]==">") {				//Check the first line of a block.
		if (lines[1][0]=="A"){
			format = "JASPAR";
		}else{
			format ="RAW";
		}								//Block error: it doesn't begin with a header line

	}else{											//Check the body of the block. Distinguish between RAW format and JASPAR format
		format = "TRANSFAC";
	}
	return format
}
	
function IsAnumber(string){
	//FUNCION QUE DADA UNA CADENA DE TAMAñO N DIGA SI ESTA CADENA ES UN NÚMERO O NO
}

function CheckRAWline(myline, ROWsize){
	numbersARRAY = myline.split(" ");
	if .length (numbersARRAY!= ROWsize) {						//All rows have to have the same number of columns
		var correctline = -1;									
	}else{
		var validNUMBER =true;									// All elements in the array must be correct numbers
		for (i in numbersARRAY){
			if (!IsAnumber(numbersARRAY[i]) ){
				validNUMBER = false;
				break;
			}
		}
		if !validNUMBER {
			correctline = -2;		
		}else{
			correctline = 1;
		}
	}
	return correctline
}

function CheckBlock(lines, block_index, format) {
	var stillOK = 0;	
	if (format="RAW") {											//RAW format treatment
		if (lines[block_index][0]!=">") {
			stillOK = -2;										//ERROR: HEADER not found (">")
		}else {
			correctline = 0;
			var line_index =1;
			var ROWsize = lines(line_index).split(" ").length;

			while (correctline>=0)&&(line_index < (block_index+5)) {
				correctline = CheckRAWline(lines[line_index], ROWsize)
				line_index++;		
			}
			////AÑADIR CUANDO Y COMO TERMINA, como diseñar la vble stillOK en este caso, en funcion de la variable correctline
		}	
	}else{														//JASPAR format treatment

	}
	return stillOK;
}	

function AnalyzeBlocks(lines, lastHeader, format){
	var block_index = 0;
	var stillOK = 0;
	while (block_index <= lastHeader)&&(stillOK >= 0) {
		stillOK  = CheckBlock(lines, block_index, format)
		block_index = block_index + 5;							//Jump to the next block
	}

}

function validateMatrix(data, file, validatingDIV, fileid, uploadBUTTON) {
	var validated = 1;
	var lines = data.split("\n");		// splits the original string in several strings (array) using return as separator. 
	var stillOK = 0;
	myHeaders = LocateHeaders(lines);
	if (file.size<validate_size){
		var lastHeader = myHeaders[myHeaders.length -1];
	}else{
		var lastHeader = myHeaders[myHeaders.length -2];
	}	

	format = FindFormat(lines);
	if format="ERROR" {
		stillOK = -1;											//ERROR: format not supported
	}else if format ="TRANSFAC"{
		stillOK = CheckTRANSFAC(lines, lastHEADER);
	}else {
		stillOK = AnalyzeBlocks(lines, lastHeader, format);
	}

	var validateMessage = "";		// Error management
	switch (stillOK){				
		case 1:
			validateMessage = " - successfully validated";			
			break;
		case -1:
			validateMessage = " - Error during the validation: file format not supported ";			
			break;
		case -2:
			validateMessage = " - Error during the validation: ERROR RAW FORMAT: HEADER not found (>) ";			
			break;
		case -3:
			validateMessage = " - Error during the validation: Invalid data line. Only A,C,T,G,N and - chars are allowed. ";			
			break;
		case -4:
			validateMessage = " - Error during the validation: Description line has inappropriate format. ";			
			break;
		case -5:
			validateMessage = " - Error during the validation: Less than 1MB files can't end with description line. ";			
			break;
		default:
			validateMessage = " - Error during the validation: Something strange happened. ";			
			break;
	}
	validateMATRIX = validated;
	makingFastaDIV(file, validatingDIV, fileid, uploadBUTTON, validateMessage, validateMATRIX);
	if ( (validateFASTA==1) && (validateMATRIX==1) ) {
		document.getElementById(uploadBUTTON).className = 'unhidden';
	}
}

/**************************GLOBAL VARIABLES STUFF****************************/


function makingFastaDIV (file, validatingDIV, fileid, uploadBUTTON, validateMessage, validateVAR) {

	if (validateVAR==1) {
		document.getElementById(fileid).className = 'hidden';
		document.getElementById(validatingDIV).innerHTML = '<img id="tick" src="http://127.0.0.1/html5/images/green_tick.jpg" />' + 
		'&nbsp;' + file.name + validateMessage;
		//document.getElementById(uploadBUTTON).className = 'unhidden';
		
		
	}else{
		document.getElementById(validatingDIV).innerHTML = '<img id="tick" src="http://127.0.0.1/html5/images/red_tick.jpg" />' +
		'&nbsp;' + file.name + validateMessage +" Choose another one file &nbsp;"; 
	}
}

/*  FINAL CHECK - SHOW THE UPLOAD BUTTON ONLY IF EVERYTHING IS OK IN BOTH CASES
		
	if ( (validateFASTA==1) && ( (validateMATRIX==1) ) {
		document.getElementById(uploadBUTTON).className = 'unhidden';
	}*/
