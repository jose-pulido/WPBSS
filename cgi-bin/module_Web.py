#! /usr/bin/python 
"""
Module with classes definitions and methods for creating the Web Page
"""
__docformat__ = "restructuredtext en"

QM = '"'

#################### CELL #######################

class Cell():
	"""
	Model for a *td tag* `<td></td>` in HTML language
	"""
	def __init__(self, content, _id="", classtype=""):
		"""
		Form class initializer.

			:parameters:
				- `content`:	Content of the form. Usually with text and tags elements inside. *(string).*
				- `_id`:		Identifier *(string).*
				- `classtype`:	*(string).*
		"""

		self.content = content
		self.id = _id		
		self.classtype = classtype

	def write(self):
		"""
		:return: *string* with the HTML code for the **DIV structure** for being used in other structures.
		"""
		ret = '''<td'''

		if self.id:
			ret = ret +''' id="'''+self.id+'"'
		if self.classtype:
			ret = ret +''' class="'''+self.classtype+'"'
		ret = ret + '>'+self.content+'''</td>'''

		return ret


#################### TABLE #######################
class Table():
	"""
	Model for a *table tag* `<table></table>` in HTML language
	"""
	def __init__(self, rows, columns, content, _id="", classtype=""):
		"""
		Form class initializer.

			:parameters:
				- `rows`:	Number of rows for the table. *(int).*
				- `column`:	Number of coluns for the table. *(int).*
				- `content`:	Description of each one of the cells using the *td tag*. *(list of cells).*
				- `_id`:		Identifier *(string).*
				- `classtype`:	*(string).*
		"""
		self.rows = rows
		self.columns = columns
		self.content = content
		self.id = _id		
		self.classtype = classtype

	def write(self):
		"""
		:return: *string* with the HTML code for the **Table4x3 structure**.
		"""
		ret = '''<table'''

		if self.id:
			ret = ret +''' id="'''+self.id+'"'
		if self.classtype:
			ret = ret +''' class="'''+self.classtype+'"'
		ret = ret + '>'+ '\n'
		
		cell_index = 0
		for r in range(self.rows):
			ret = ret + '<tr>'+ '\n'
			for c in range(self.columns):
				ret = ret + self.content[cell_index] + '\n'
				cell_index +=1
			ret = ret + '</tr>'+ '\n'
		ret = ret +'''</table>'''

		return ret


#################### IMAGE  #######################	
class Image():
	"""
	Model for an *image tag* `<img/>` in HTML language
	"""
	def __init__(self, fileName, directory="http://127.0.0.1/WPBSS/images/", classtype="", extraparams=""):
		"""
		Image class initializer.

			:parameters:
				- `fileName`: 	Line from the file output.txt *(string).*
				- `directory`:	absolute path to image's directory *(string).*
				- `classtype`:	*(string).*
				- `extraparams`:	*(string).*
		"""
		self.dir = directory
		self.fileName = fileName
		self.classtype = classtype
		self.extraparams = extraparams

	def write(self):
		"""
		:return: *string* with the HTML code for the **Image structure** for being used in other structures.
		"""
		ret = '''<img src="'''+self.dir+self.fileName+'"'
		if self.classtype:
			ret = ret +''' class="'''+self.classtype+'"'
		if self.extraparams:
			ret=ret+' '+self.extraparams
		ret = ret+'''/>'''
		return ret  

#################### INPUT #######################

class Input():
	"""
	Model for an *input tag* `<input/>` in HTML language
	"""
	def __init__(self, _type, _id="", name="", value="", classtype="", event=""):
		"""
		Input class initializer.

			:parameters:
				- `_type`: 		Type of input: "file","submit" or "button" *(string).*
				- `_id`:		Identifier *(string).*
				- `name`:		*(string).*
				- `value`:		*(string).*
				- `classtype`:	*(string).*
				- `event`:		Describes what to do when a specif event take place: "onclick" *(string).*
	
		:exceptions:
			- `ArgumentError`: Raised when *_type* is not on its list values.
		"""
		typeValues = ["file","submit","button"]
		if _type not in typeValues:
			raise ArgumentError("Class Input. type not in %s"%(typeValues))

		self.type = _type
		self.id = _id
		self.name = name
		self.value = value
		self.classtype = classtype
		self.event = event

	def write(self):
		"""
		:return: *string* with the HTML code for the **Input structure** for being used in other structures.
		"""
				
		ret = '''<input type="'''+self.type+'"'

		if self.id:
			ret = ret +''' id="'''+self.id+'"'
		if self.name:
			ret = ret +''' name="'''+self.name+'"'
		if self.value:
			ret = ret +''' value="'''+self.value+'"'
		if self.classtype:
			ret = ret +''' class="'''+self.classtype+'"'
		if self.event:
			ret = ret+' '+self.event			
		ret = ret + '''/>'''+'\n'

		return ret  

#################### FORM #######################

class Form():
	"""
	Model for a *form tag* `<form></form>` in HTML language
	"""
	def __init__(self, content, action, enctype="multipart/form-data", method="post", _id="", classtype=""):
		"""
		Form class initializer.

			:parameters:
				- `content`:	Content of the form. Usually with text and input elements inside. *(string).*
				- `action`:		Indicates the URL which processes the form data. *(string).*
				- `enctype`: 	Type of codification: "multipart/form-data" or "application/x-www-form-urlencoded". *(string).*
				- `method`:		HTTP method for sending the form: "post" or "get". *(string).*
				- `_id`:		Identifier *(string).*
				- `classtype`:	*(string).*			
	
		:exceptions:
			- `ArgumentError`: Raised when *enctype* or *method* is not on their list values.
		"""

		enctypeValues = ["multipart/form-data","application/x-www-form-urlencoded"]
		if enctype not in enctypeValues:
			raise ArgumentError("Class Form. method not in %s"%(enctypeValues))

		methodValues = ["post","get"]
		if method not in methodValues:
			raise ArgumentError("Class Form. method not in %s"%(methodValues))

		self.content = content
		self.action = action
		self.enctype = enctype
		self.method = method
		self.id = _id		
		self.classtype = classtype

	def write(self):
		"""
		:return: *string* with the HTML code for the **Form structure** for being used in other structures.
		"""
		ret = '''<form enctype="'''+self.enctype+'''" action="'''+self.action+'''" method="'''+self.method

		if self.id:
			ret = ret +'''" id="'''+self.id+'"'
		if self.classtype:
			ret = ret +''' class="'''+self.classtype+'"'
		ret = ret + '>'+ '\n'+ '\t'+'\t'+self.content+ '\n' + '\t' + '''</form>'''

		return ret  

#################### DIV #######################

class DIV():
	"""
	Model for a *div tag* `<div></div>` in HTML language
	"""
	def __init__(self, content, _id="", classtype=""):
		"""
		Form class initializer.

			:parameters:
				- `content`:	Content of the form. Usually with text and tags elements inside. *(string).*
				- `_id`:		Identifier *(string).*
				- `classtype`:	*(string).*
		"""

		self.content = content
		self.id = _id		
		self.classtype = classtype

	def write(self):
		"""
		:return: *string* with the HTML code for the **DIV structure** for being used in other structures.
		"""
		ret = '''<div'''

		if self.id:
			ret = ret +''' id="'''+self.id+'"'
		if self.classtype:
			ret = ret +''' class="'''+self.classtype+'"'
		ret = ret + '>'+ '\n'+ '\t'+self.content+ '\n' + '''</div>'''

		return ret


#################### HTML  #######################

class HTML():
	"""
	Model for a *htmltag* `<html></html>` in HTML language
	"""
	def __init__(self, title_TAB = "", style_Files = [], script_Files = [], header = "", html_Body = "", footer = ""):
		"""
		Form class initializer.

			:parameters:
				- `title_TAB`:				This text will be displayed in the tab browser. *(string).*
				- `style_Files`:		Stores the names of the .css files *(string).*
				- `script_Files`: 		Stores the names of the .js (javascript) files *(string).*
				- `header`:				The main and bigger text of the website. *(string).*
				- `html_Body`:			*(string).*
				- `footer`:				*(string).*
		"""

		self.title_TAB = ""
		self.style_Files = []
		self.script_Files = []
		self.header = ""
		self.html_Body = ""
		self.footer = ""
	
	def addTitle(self, title_TAB):
		self.title_TAB = title_TAB

	def add_styleFiles(self, fileName):
		self.style_Files.append('''http://127.0.0.1/WPBSS/css/'''+fileName)

	def add_scriptFiles(self, fileName):
		self.script_Files.append('''http://127.0.0.1/WPBSS/javascript/'''+fileName)

	def addHeader(self, header):
		self.header = header

	def addBody(self, content):
		self.html_Body = content

	def addFooter(self, footer):
		self.footer = footer

	def __str__(self):
		"""
			:return: *string* with the HTML code for the **HTML structure**.
		"""

		ret = '''<!DOCTYPE HTML>'''+'\n'+'''<html>''' +'\n'
		ret = ret+'''<head>'''+'\n'+'\t'+'''<title>'''+self.title_TAB+'''</title>'''+'\n'

		for path in self.style_Files:
			ret = ret+ '\t'+'''<link rel="stylesheet" type="text/css" href="''' + path + '''" media="screen">''' + '\n'

		for files in self.script_Files:
			ret = ret+ '\t'+'''<script type="text/javascript" src="''' + files + '''"></script>'''+'\n'

		ret = ret + "</head>" + '\n'+ "<header>" + '\n'+ self.header+ '\n'+ "</header>" + '\n'+ '\n'
		ret = ret + "<body>"+'\n'+self.html_Body+'\n'+"</body>" + '\n'+ '\n'
		ret = ret + "<footer>"+'\n'+self.footer+'\n'+"</footer>"
		return ret

	def WriteHTMLfile(self, fileName):
		"""
			Prints the html code in an output file.
		"""
		path = "/var/www/WPBSS/cgi-bin/"+fileName
		fout = open(path, 'w')
		fout.write("%s"%(self))
		fout.close()




