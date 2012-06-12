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
		}
	}

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
		}else {														// if it is not a description line, it should be a data line
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


/*****************************************************************/
/**************************MATRIX*********************************/
/*****************************************************************/

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

function FindFormat(lines) {
	var format ="";
	if (lines[0].slice(0,2)=="AC") {							//Check the first line of a block.
			format = "TRANSFAC";								//Block error: it doesn't begin with a header line

	}else if (lines[0][0]==">"){
		if (lines[1][0]=="A"){
			format = "JASPAR";
		}else{
			format ="RAW";
		}														//Check the body of the block. Distinguish between RAW format and JASPAR format		
	}else {
		format = "ERROR";	
	}
	return format
}

function DelimitateBlocks(lines, format) {
	var initBlock =[];
	var endBlock = [];
	if (format=="TRANSFAC"){
		var i =0;
		for (var line_index=0; line_index <= (lines.length -2); line_index++) {
			if (lines[line_index].slice(0,2)=="P0") {
				initBlock[i] = line_index;
				var k = line_index+1;
				while ((k<(lines.length -2)) && (lines[k].slice(0,2)!="XX")) {
					k++;
				}
				if ((k==(lines.length -2)) && (lines[k].slice(0,2)!="XX")) {		// It's the end of file, but the block terminator "//"
					trash = initBlock.pop();										// is not found -> last block incomplete (file.size>1MB)
				}else{
					endBlock[i]=k-1;												// The file ends correctly with the block terminator "//"			
				}
				i++;
				var line_index = k-1;
			}
		}

	}else {
		var i=0;																		//RAW or JASPAR format
		for (block_index = 0; block_index <= (lines.length -1); block_index +=5) {		//The size of the blocks in these formats is fixed
			initBlock[i] = block_index;													//One line for description, four lines for the matrix
			endBlock[i] = block_index +4;
			i++;
		}
		if ( endBlock[endBlock.length -1] > (lines.length -1) ) {						//Last block may be incomplete if file.size > 1MB
			trash = initBlock.pop();													//In that case, we don't take it into account 
			trash = endBlock.pop();
		}
	}
	var Blocks = [initBlock, endBlock];
	return Blocks;
}

function SpacesPurge(array) {
	position = array.indexOf('');
	while (position!=-1) {
		array.splice(position,1);
		position = array.indexOf('');
	}
	return array;
}

function RemoveSpaces(lines, init, end) {									// Create an array of lists. Each list has the column numbers of his row.
	var myArray = [];
	var j =0;
	for (var i=(init+1); i<=end; i++) {		
		myArray[j] = SpacesPurge( (lines[i].split(" ")) );
		j = j+1;
	}
	return myArray;
}

function CheckColumns(myBlock) {
	var ind = 1;
	var stillOK = 1;
	while ((ind <= myBlock.length-1)&&(stillOK==1)) {
		if ( myBlock[ind].length != myBlock[ind-1].length){
			stillOK = -3;
		}
		ind = ind+1;
	}
	return stillOK;
}

function ValidateBlocks(lines, init, end, format) {
	var stillOK = 0;
	var myBlock = [];
	myBlock = RemoveSpaces(lines, init, end);
	stillOK = CheckColumns(myBlock);
	return stillOK;
}

function validateMatrix(data, file, validatingDIV, fileid, uploadBUTTON) {
	//var validated = 1;
	var lines = data.split("\n");							// splits the original string in several strings (array) using return as separator. 
	var stillOK = 0;
	format = FindFormat(lines);

	if (format== "ERROR") {
		stillOK = -1;										//ERROR: format not supported
	}else  {
		var Blocks = DelimitateBlocks(lines, format);
		if (Blocks[0] == [])	{							//No header founded for the format (CHECK POSSIBLE ERROR: Blocks[0].length==0 instead????)
			stillOK = -2;
		}else {
			var i=0;
			while ( (stillOK >= 0)&&(i <= Blocks[0].length -1) ) {
				var stillOK = ValidateBlocks(lines, Blocks[0][i], Blocks[1][i], format);
				i++;
			}		
		}
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
			validateMessage = " - Error during the validation: HEADER not found for that format ";			
			break;
		case -3:
			validateMessage = " - Error during the validation: All the rows in the matrix must have the same number of columns. ";			
			break;
		case -4:
			validateMessage = " - Error during the validation: TRANSFAC format error. Check every row has its nucleotid score.";			
			break;
		case -5:
			validateMessage = " - Error during the validation: Less than 1MB files can't end with description line. ";			
			break;
		default:
			validateMessage = " - Error during the validation: Something strange happened. ";			
			break;
	}
	validateMATRIX = stillOK;
	makingFastaDIV(file, validatingDIV, fileid, uploadBUTTON, validateMessage, validateMATRIX);
	if ( (validateFASTA==1) && (validateMATRIX==1) ) {
		document.getElementById(uploadBUTTON).className = 'unhidden';
	}
}

/**************************GLOBAL VARIABLES STUFF****************************/


function makingFastaDIV (file, validatingDIV, fileid, uploadBUTTON, validateMessage, validateVAR) {

	if (validateVAR==1) {
		document.getElementById(fileid).className = 'hidden';
		document.getElementById(validatingDIV).innerHTML = '<img id="tick" src="http://127.0.0.1/WPBSS/images/green_tick.jpg" />' + 
		'&nbsp;' + file.name + validateMessage;
		//document.getElementById(uploadBUTTON).className = 'unhidden';
		
		
	}else{
		document.getElementById(validatingDIV).innerHTML = '<img id="tick" src="http://127.0.0.1/WPBSS/images/red_tick.jpg" />' +
		'&nbsp;' + file.name + validateMessage +" Choose another one file &nbsp;"; 
	}
}
