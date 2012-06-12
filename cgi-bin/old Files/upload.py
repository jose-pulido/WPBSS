#!/usr/bin/python


import cgi, os
import cgitb; cgitb.enable()

user_upload_path = '/tmp/'

print "Content-type:text/html"
print 

def add_webTitle(webTitle):
	print "<title>"+webTitle+"</title>"

def add_css(css_file,css_folder="http://127.0.0.1/html5/css/"):	
	print '''<link rel="stylesheet" type="text/css" href="'''+css_folder+css_file+'''" media="screen">'''

def add_javascript(javascript_file, javascript_folder="http://127.0.0.1/html5/javascript/"):
	print '''<script type="text/javascript" src="'''+javascript_folder+javascript_file+'''"></script>'''

def generate_head():
	print "<head>"
	add_webTitle("WPBSS")
	add_css("sheet1.css")
	add_javascript("jquery-1.7.1.js")
	add_javascript("funct3.js")					#### OJO QUE LO HE CAMBIADO PARA HACER PRUEBAS ####
	print "</head>"

def generate_header(header_content):
	print "<header>"
	print header_content
	print "</header>"

def generate_footer(footer_content):
	print "<footer>"
	print footer_content
	print "</footer>"


def generate_DIV(ident, content, classtype="unhidden"):
	part1= '''<div id="'''+ident+'''" '''+'''class="'''+classtype+'''">'''
	part2= content
	part3= "</div>"
	ret = part1+part2+part3
	return ret


def generate_body():

	section1DIVcontent = """<nav>
					<ul class="menu">
						 <li><a href="#">Home</a></li>
						<li><a href="#">Information</a></li>
						 <li><a href="#">Links</a></li>
					</ul>
				 </nav>""" + generate_DIV("hueco1", "HUECO")


	infocontent = """Welcome to the platform. You can upload your file for using FiSim algorithm (Fuzzy Integral Similarity), a similarity measure for comparing two motifs with one another based on the fuzzy integral with respect to a fuzzy measure. Use the drop zone for placing your file directly dragged from your file explorer or select it using the proper button."""
	section2content1 = generate_DIV("info", infocontent)


	uploadiv_content = """
		<form enctype="multipart/form-data" id="myform" action="/cgi-bin/upload.py" method="post">
					FORM<input type="file" id="fileFASTA" onclick="myFASTA('validating1', 'fileFASTA', 'uploadBUTTON');" name="fileFASTA" class="unhidden"/>
					PWM<input type="file" id="fileMATRIX" onclick="myMATRIX('validating2', 'fileMATRIX', 'uploadBUTTON');" name="fileMATRIX" class="unhidden"/>
					<input type="submit" id="uploadBUTTON" value="Upload" class="hidden"/>
		</form>"""			
	uploadivDIV = generate_DIV("uploadiv", uploadiv_content)


	v1= """Validating1  <img src="http://127.0.0.1/html5/images/waiting.gif"/>"""
	validating_content1 = generate_DIV("validating1", v1, "hidden")
	v2= """Validating2  <img src="http://127.0.0.1/html5/images/waiting.gif"/>"""
	validating_content2 = generate_DIV("validating2", v2, "hidden")
	validatingDIV = generate_DIV("validating", validating_content1+validating_content2)

	section2content2 = generate_DIV("upload_zone", uploadivDIV+validatingDIV)	

	print "<body>"
	print generate_DIV("section1", section1DIVcontent)
	print generate_DIV("section2", section2content1+section2content2)
	#generate_DIV
	print "</body>"
	mybody1 = "<body>"+generate_DIV("section1", section1DIVcontent)+generate_DIV("section2", section2content1+section2content2)+"</body>"
	return mybody1


def generate_HTML():
	print """<!DOCTYPE HTML>

		 <html>"""
	generate_head()
	generate_header("Web Platform For Binding Sites Sequences")
	generate_body()
	generate_footer("Max Planck Institute for Infection Biology - Charit&eacute;platz 1 - D-10117 Berlin - GERMANY")
	print "</html>"


######################### MAIN ##################################
def main():
	form = cgi.FieldStorage()
	if ((form.has_key('fileFASTA'))and(form.has_key('fileMATRIX'))):
		# Get filename here.
		FASTAitem = form['fileFASTA']
		MATRIXitem = form['fileMATRIX']

		# Test if the file was uploaded
		if (FASTAitem.filename and MATRIXitem.filename):
			# strip leading path from file name to avoid 
			# directory traversal attacks
			fn = os.path.basename(FASTAitem.filename.replace("\\", "/" ))
			open(user_upload_path + fn, 'wb').write(FASTAitem.file.read())
			fn2 = os.path.basename(MATRIXitem.filename.replace("\\", "/" ))
			open(user_upload_path + fn2, 'wb').write(MATRIXitem.file.read())
			message = 'The file "' + fn + '" was uploaded successfully'
			
		else:
			message = 'No file was uploaded'
			
		print """
		<html>
		<body>
			<p>%s</p>
		</body>
		</html>""" %(message)
	else:
		generate_HTML()
###################################################################
if __name__ == "__main__":
    main()

