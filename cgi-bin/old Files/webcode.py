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

	check1 = module_Web.Input("checkbox", name="transfac", value="on", event='checked')
	check2 = module_Web.Input("checkbox", name="jaspar", value="on", event='checked')
	check3 = module_Web.Input("checkbox", name="userownfile", value="on")
	checkbox = check1.write()+'TRANSFAC<br>'+'\n'+check2.write()+'JASPAR<br>'+'\n'+check3.write()+'OWN MATRIX FILE'

	img = module_Web.Image("waiting.gif", "http://127.0.0.1/WPBSS/images/")
	inp1 = module_Web.Input("file", _id='fileMATRIX', classtype="unhidden", event='''onclick="myMATRIX('validating2', 'fileMATRIX', 'uploadBUTTON');"''', name="fileMATRIX")
	v2 = module_Web.DIV("Validating2"+img.write(), _id="validating2", classtype="hidden")
	inp2 = module_Web.Input("file", _id='fileFASTA', classtype="unhidden", event='''onclick="myFASTA('validating1', 'fileFASTA', 'uploadBUTTON');"''', name="fileFASTA")
	v1 = module_Web.DIV("Validating"+img.write(), _id="validating1", classtype="hidden")
	inp3 = module_Web.Input("submit", _id="uploadBUTTON", classtype="hidden", value="Upload")

	frm = module_Web.Form(checkbox+inp1.write()+v2.write()+"<br><b>SEQUENCE</b>"+inp2.write()+v1.write()+inp3.write(), "/cgi-bin/testWeb.py", _id="myform")	
	uploadiv = module_Web.DIV(frm.write(), _id="uploadiv", classtype="unhidden")

	td1_1 = module_Web.Cell('What is it?', classtype="header")
	td1_2 = module_Web.Cell('How it works?', classtype="header")
	td1_3 = module_Web.Cell('Try it', classtype="header")

	info_td21 = '''<b>WPBSS</b> es un Framework que, basandose en los algoritmos difusos, ofrece la posibilidad de analizar completamente experimentos biologicos reales dentro de una interfaz sencilla y amigable.'''
	info_td22 = '''Sube tu archivo con la secuencia que deseas analizar. La web lo procesara en busca de alguna errata en el formato y elige contra que matrices de las disponibles quieres hacerlo. Puedes incluso utilizar tus propias matrices.'''
	info_td23 = '''Selecciona las opciones y sube tus archivos:<br>'''+'\n'+uploadiv.write()

	td2_1 = module_Web.Cell(info_td21, classtype="stuff")
	td2_2 = module_Web.Cell(info_td22, classtype="stuff")
	td2_3 = module_Web.Cell(info_td23, classtype="stuff")

	td3_1 = module_Web.Cell('More Info', classtype="header")
	td3_2 = module_Web.Cell('Team', classtype="header")
	td3_3 = module_Web.Cell('Credits', classtype="header")
	
	td4_1 = module_Web.Cell('Bla bla info', classtype="stuff")
	td4_2 = module_Web.Cell('bla bla team', classtype="stuff")
	td4_3 = module_Web.Cell('bla bla credits', classtype="stuff")
	
	table_content = [td1_1.write(), td1_2.write(), td1_3.write(), td2_1.write(), td2_2.write(), td2_3.write(), td3_1.write(), td3_2.write(), td3_3.write(), td4_1.write(), td4_2.write(), td4_3.write()]
	table1x3 = module_Web.Table(4,3, table_content,  classtype="main")
	tabletest = module_Web.DIV(table1x3.write(), _id="tablerize")



	footer  = '''Max Planck Institute for Infection Biology - Charit&eacute;platz 1 - D-10117 Berlin - GERMANY'''
	header = '''Web Platform For Binding Sites Sequences'''
	web = module_Web.HTML()
	web.addTitle("WPBSS")
	web.addHeader(header)
	web.addFooter(footer)
	web.addBody(tabletest.write())
	web.add_styleFiles("sheet1.css")
	web.add_scriptFiles("jquery-1.7.1.js")
	web.add_scriptFiles("funct5.js")
	#web.WriteHTMLfile("myWeb.html")
	return web
###################################################################
######################### MAIN ##################################
def main():
	
	myWeb = generate_HTML()
	myWeb.WriteHTMLfile('webcode.html')
###################################################################
if __name__ == "__main__":
    main()
