#!/usr/bin/python

descriptionText = '''
Program to 

'''

import module_Web
import cgi, os
import cgitb; cgitb.enable()

user_upload_path = '/tmp/'

print "Content-type:text/html"
print 
######################### FUNCTIONS ##################################

def generate_HTML():
	infoWeb = "Welcome to the platform. You can upload your file for using FiSim algorithm (Fuzzy Integral Similarity), a similarity measure for comparing two motifs with one another based on the fuzzy integral with respect to a fuzzy measure. Use the drop zone for placing your file directly dragged from your file explorer or select it using the proper button."
	info = module_Web.DIV(infoWeb, _id="info")
	
	img = module_Web.Image("waiting.gif", "http://127.0.0.1/html5/images/")

	imgLogo = module_Web.Image("mpiib_logo.gif", "http://127.0.0.1/html5/images/", classtype="a")
	divLogo = v1 = module_Web.DIV(imgLogo.write(), _id="imgLogo")

	inp1 = module_Web.Input("file", _id='fileFASTA', classtype="unhidden", event='''onclick="myFASTA('validating1', 'fileFASTA', 'uploadBUTTON');"''', name="fileFASTA")	
	inp2 = module_Web.Input("file", _id='fileMATRIX', classtype="unhidden", event='''onclick="myMATRIX('validating2', 'fileMATRIX', 'uploadBUTTON');"''', name="fileMATRIX")
	inp3 = module_Web.Input("submit", _id="uploadBUTTON", classtype="hidden", value="Upload")

	frm = module_Web.Form("FASTA"+inp1.write()+"PWM"+inp2.write()+inp3.write(), "/cgi-bin/testWeb.py", _id="myform")	
	uploadiv = module_Web.DIV(frm.write(), _id="uploadiv", classtype="unhidden")

	v1 = module_Web.DIV("Validating"+img.write(), _id="validating1", classtype="hidden")
	v2 = module_Web.DIV("Validating2"+img.write(), _id="validating2", classtype="hidden")
	validating = module_Web.DIV(v1.write()+'\n'+v2.write(), _id="validating", classtype="unhidden")
	
	upload_zone = module_Web.DIV(uploadiv.write()+'\n'+validating.write(), _id="upload_zone")

	section2 = module_Web.DIV(info.write()+'\n'+'\n'+upload_zone.write(), _id="section2")

	footer  = '''Max Planck Institute for Infection Biology - Charit&eacute;platz 1 - D-10117 Berlin - GERMANY'''
	header = '''Web Platform For Binding Sites Sequences'''
	web = module_Web.HTML()
	web.addTitle("WPBSS")
	web.addHeader(header)
	web.addFooter(footer)
	web.addBody(divLogo.write()+'\n'+section2.write())
	web.add_styleFiles("sheet1.css")
	web.add_scriptFiles("jquery-1.7.1.js")
	web.add_scriptFiles("funct5.js")
	#web.WriteHTMLfile("myWeb.html")
	return web
###################################################################
######################### MAIN ##################################
def main():
	form = cgi.FieldStorage()
	myWeb = generate_HTML()
		
	if ((form.has_key('fileFASTA'))and(form.has_key('fileMATRIX'))):
		# Get filename here.
		FASTAitem = form['fileFASTA']
		MATRIXitem = form['fileMATRIX']

		# Test if the file was uploaded
		if (FASTAitem.filename and MATRIXitem.filename):
			# strip leading path from file name to avoid 
			# directory traversal attacks
			fh_FASTA = os.path.basename(FASTAitem.filename.replace("\\", "/" ))
			open(user_upload_path + fh_FASTA, 'wb').write(FASTAitem.file.read())
			fh_MATRIX = os.path.basename(MATRIXitem.filename.replace("\\", "/" ))
			open(user_upload_path + fh_MATRIX, 'wb').write(MATRIXitem.file.read())
			message = 'The files "' + fh_FASTA + ' and '+ fh_MATRIX + '" were uploaded successfully'
			
		else:
			message = 'No file was uploaded'
			
		fh_result = open(user_upload_path + fh_MATRIX, 'r')
		read_data = ""		
		for line in fh_result:
			read_data = read_data+line+'<br>'
		fh_result.closed
		
		webResults = myWeb
		results = module_Web.DIV(message+". Aqui voy a poner los resultados:"+'<br>'+read_data, _id="results")
		webResults.addBody(results.write())
		print webResults
	else:
		print myWeb
###################################################################
if __name__ == "__main__":
    main()
