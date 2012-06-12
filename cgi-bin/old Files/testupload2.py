#!/usr/bin/python


import cgi, os
import cgitb; cgitb.enable()

user_upload_path = '/tmp/';

########### PAGINA WEB INICIAL
print "Content-type:text/html"
print 
def generate_web():

	htmlcode="""
	<!DOCTYPE HTML>

	<html>
	<body>
	   <form enctype="multipart/form-data" action="/cgi-bin/testupload2.py" method="post">
		   <p>File: <input type="file" name="filename" /></p>
		   <p><input type="submit" value="Upload" /></p>
	   </form>
	</body>
	</html> """
	print htmlcode

def main():
	form = cgi.FieldStorage()
	if (form.has_key('filename')) :
		# Get filename here.
		fileitem = form['filename']

		# Test if the file was uploaded
		if fileitem.filename:
		   # strip leading path from file name to avoid 
		   # directory traversal attacks
		   fn = os.path.basename(fileitem.filename.replace("\\", "/" ))
		   open(user_upload_path + fn, 'wb').write(fileitem.file.read())

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
		generate_web();

main();
