#!/usr/bin/python

descriptionText = '''
Program to 

'''

import module_Web
import cgi, os
import cgitb; cgitb.enable()

import sys, glob
from Motif import *
from WebMotif import *
from Result import *
import utils
#import argparse

homedir = os.path.expanduser('~')
user_upload_path = '/tmp/'
LOGOpath = '/External_Data_SC/LOGO/'
#TRANSFACpath = homedir+'/Python/External_Data_SC/TRANSFAC/matrix_seqs/test/'
#JASPAR_sequencesPath = homedir+'/Python/External_Data_SC/JASPAR/sequences/'
TRANSFACpath = homedir+'/External_Data_SC/TRANSFAC/matrix_seqs/'
JASPAR_sequencesPath = homedir+'/External_Data_SC/JASPAR/sequences/'

print "Content-type:text/html"
print



######################### INTUIT FUNCTIONS ##################################

def ReadTransfacFile(pathfile):									#Read a TRANSFAC formatted file and fill the motif object properly
	
	seqFiles = glob.glob(pathfile+'*.transfac.txt')
	transfac_valid = []
	transfac_NOT_valid = []
	
	for f in seqFiles:		
		m = WebMotif(f, 'Transfac')
		
		if m.validMotif:
			transfac_valid.append(m)
		else:
			transfac_NOT_valid.append(m)
			
	return transfac_valid, transfac_NOT_valid


def ReadJasparFile(pathfile):									#Read a JASPAR formatted file and fill the motif object properly
		
	seqFiles = glob.glob(pathfile+'*.sites')
	jaspar_valid = []
	jaspar_NOT_valid = []
	
	for f in seqFiles:		
		m = WebMotif(f, 'Jaspar')
		if m.validMotif:
			jaspar_valid.append(m)
		else:
			jaspar_NOT_valid.append(m)
			
	return jaspar_valid, jaspar_NOT_valid
	
def createTableOfResults(results):

	tableOfResults = []
	hr1_1 = module_Web.Cell('Motif ID', classtype="headerResult")
	hr1_2 = module_Web.Cell('Motif Origin', classtype="headerResult")
	hr1_3 = module_Web.Cell('Best Scored Sequence', classtype="headerResult")
	hr1_4 = module_Web.Cell('SCORE', classtype="headerResult")
	hr1_5 = module_Web.Cell('Motif LOGO', classtype="headerResult")
	headerRow = [hr1_1.write(), hr1_2.write(), hr1_3.write(), hr1_4.write(), hr1_5.write()]
	tableOfResults.append(headerRow)
	
	cont = 1
	for result in results:
		if result.format == 'Transfac':
			logo = LOGOpath + 'LOGO_T/'
		else:
			logo = LOGOpath + 'LOGO_J/'
			
		logo_img = 	module_Web.Image(result.name + '.logo.png', directory = logo, classtype="logo_img")
		
		r1_1 = module_Web.Cell(str(cont)+'.'+'\t'+result.name, classtype="stuffResult")
		r1_2 = module_Web.Cell(result.format, classtype="stuffResult")
		r1_3 = module_Web.Cell(result.BSSequence, classtype="stuffResult")
		r1_4 = module_Web.Cell( str(result.BestScore), classtype="stuffResult")
		r1_5 = module_Web.Cell( logo_img.write(), classtype="stuffResult")
		row = [r1_1.write(), r1_2.write(), r1_3.write(), r1_4.write(), r1_5.write()]
		tableOfResults.append(row)
		cont += 1
	return 	tableOfResults


######################### HTML CONSTRUCTION ##################################

def generate_HTML():
	title_img = module_Web.Image("title_clear", classtype="title_img")	

	check1 = module_Web.Input("checkbox", _id="transfac", name="transfac", value="on", event='''onclick="BlockBox('transfac');", checked''')
	check2 = module_Web.Input("checkbox", _id="jaspar", name="jaspar", value="on", event='''onclick="BlockBox('jaspar');", checked''')
	check3 = module_Web.Input("checkbox", _id="userownfile", name="userownfile", value="on", event='''onclick="checkingBox('userownfile');"''')
	checkbox = check1.write()+'TRANSFAC<br>'+'\n'+check2.write()+'JASPAR<br>'+'\n'+check3.write()+'OWN MATRIX FILE'

	img = module_Web.Image("waiting.gif", "http://127.0.0.1/WPBSS/images/")
	inp1 = module_Web.Input("file", _id='fileMATRIX', classtype="hidden", event='''onclick="myMATRIX('validating2', 'fileMATRIX', 'uploadBUTTON');"''', name="fileMATRIX")
	v2 = module_Web.DIV("Validating2"+img.write(), _id="validating2", classtype="hidden")
	inp2 = module_Web.Input("file", _id='fileFASTA', classtype="unhidden", event='''onclick="myFASTA('validating1', 'fileFASTA', 'uploadBUTTON');"''', name="fileFASTA")
	v1 = module_Web.DIV("Validating"+img.write(), _id="validating1", classtype="hidden")
	inp3 = module_Web.Input("submit", _id="uploadBUTTON", classtype="hidden", value="Upload")

	frm = module_Web.Form(checkbox+inp1.write()+v2.write()+"<br><b>SEQUENCE</b>"+inp2.write()+v1.write()+inp3.write(), "/cgi-bin/pfm.py", _id="myform")	
	uploadiv = module_Web.DIV(frm.write(), _id="uploadiv", classtype="unhidden")

	td1_1 = module_Web.Cell('What is it?', classtype="header")
	td1_2 = module_Web.Cell('How does it work?', classtype="header")
	td1_3 = module_Web.Cell('Try it', classtype="header")
	row1 = [td1_1.write(), td1_2.write(), td1_3.write()]
	
	info_td21 = '''<b>WPBSS</b> es un Framework que, basandose en los algoritmos difusos, ofrece la posibilidad de analizar completamente experimentos biologicos reales dentro de una interfaz sencilla y amigable.'''
	info_td22 = '''Sube tu archivo con la secuencia que deseas analizar. La web lo procesara en busca de alguna errata en el formato y elige contra que matrices de las disponibles quieres hacerlo. Puedes incluso utilizar tus propias matrices.'''
	info_td23 = '''Selecciona las opciones y sube tus archivos:<br>'''+'\n'+uploadiv.write()

	td2_1 = module_Web.Cell(info_td21, classtype="stuff")
	td2_2 = module_Web.Cell(info_td22, classtype="stuff")
	td2_3 = module_Web.Cell(info_td23, classtype="stuff")
	row2 = [td2_1.write(), td2_2.write(), td2_3.write()]
	

	td3_1 = module_Web.Cell('More Info', classtype="header")
	td3_2 = module_Web.Cell('Team', classtype="header")
	td3_3 = module_Web.Cell('Credits', classtype="header")
	row3 = [td3_1.write(), td3_2.write(), td3_3.write()]
	
	td4_1 = module_Web.Cell('Bla bla info', classtype="stuff")
	td4_2 = module_Web.Cell('bla bla team', classtype="stuff")
	td4_3 = module_Web.Cell('bla bla credits', classtype="stuff")
	row4 = [td4_1.write(), td4_2.write(), td4_3.write()]
	
	table_content = [row1, row2, row3, row4]
	tesTable = module_Web.Table(table_content,  classtype="main")
	tabletest = module_Web.DIV(tesTable.write(), _id="tablerize")
	#table_content = [td1_1.write(), td1_2.write(), td1_3.write(), td2_1.write(), td2_2.write(), td2_3.write(), td3_1.write(), td3_2.write(), td3_3.write(), td4_1.write(), td4_2.write(), td4_3.write()]
	#table1x3 = module_Web.Table(4,3, table_content,  classtype="main")
	#tabletest = module_Web.DIV(table1x3.write(), _id="tablerize")

	
	footer  = '''Max Planck Institute for Infection Biology - Charit&eacute;platz 1 - D-10117 Berlin - GERMANY'''
	header = title_img.write()+'''Web Platform For Binding Sites Sequences'''
	web = module_Web.HTML()
	web.addTitle("WPBSS")
	web.addHeader(header)
	web.addFooter(footer)
	web.addBody(tabletest.write())
	web.add_styleFiles("sheet1.css")
	web.add_scriptFiles("jquery-1.7.1.js")
	web.add_scriptFiles("funct6.js")
	#web.WriteHTMLfile("myWeb.html")
	return web

###################################################################
######################### MAIN ##################################

def main():
	form = cgi.FieldStorage()
	myWeb = generate_HTML()
	
	omf = []

	if ((form.has_key('fileFASTA'))and(form.has_key('fileMATRIX'))):
		# Get filename here.
		FASTAitem = form['fileFASTA']
		MATRIXitem = form['fileMATRIX']

		# Test if the file was uploaded
		if (FASTAitem.filename):
			# strip leading path from file name to avoid 
			# directory traversal attacks
			fh_FASTA = os.path.basename(FASTAitem.filename.replace("\\", "/" ))
			open(user_upload_path + fh_FASTA, 'wb').write(FASTAitem.file.read())
			seqs = utils.readSeq(user_upload_path + fh_FASTA)
			results = []
			
			if (MATRIXitem.filename):
				fh_MATRIX = os.path.basename(MATRIXitem.filename.replace("\\", "/" ))
				open(user_upload_path + fh_MATRIX, 'wb').write(MATRIXitem.file.read())
				message = 'The files "' + fh_FASTA + ' and '+ user_upload_path+fh_MATRIX + '" were uploaded successfully'
			else:
				message = 'The file "' + fh_FASTA + '" was uploaded successfully'


#####################################################################################################

			if form.getvalue('transfac'):
				
   				transfac_valid, transfac_NOT_valid = ReadTransfacFile(TRANSFACpath)		
				for m in transfac_valid:
					results.append( Result(m, seqs) )
					
					
				message = '<br>' + message + '<br>' + 'NUMERO DE MATRICES TRANSFAC ' + str(len(transfac_NOT_valid)) + homedir
									
			if form.getvalue('jaspar'):
			
   				jaspar_valid, jaspar_NOT_valid = ReadJasparFile(JASPAR_sequencesPath)
		
				for j in jaspar_valid:
					results.append( Result(j, seqs) )
   				
   				   				 				
				message = '<br>' + message + '<br>' + str(len(jaspar_motifs))
		
			if form.getvalue('userownfile'):
			
						
   				omf = WebMotif(user_upload_path+fh_MATRIX, 'Transfac')
   				if omf.validMotif:
					results.append( Result(omf, seqs) )
			#	message = '<br>' + message + '<br>' + str(len(omf))
				
			#else:
   			#	omf = "OWNER MATRIX FILE NO"

			#message = '<br>' + message + '<br>' +  str(len(transfac_motifs)) + '<br>' + str(len(jaspar_motifs)) + '<br>' + omf + '<br>'
			#message = '<br>' + message + '<br>' + str(len(omf)) + '<br>' + str(len(transfac_motifs))+ '<br>' + str(len(jaspar_motifs))
		else:
			message = 'No file was uploaded'
			
		
		listOfResults = createTableOfResults(sorted(results, key=lambda result: result.BestScore, reverse = True))
		TableOfResults = module_Web.Table(listOfResults,  classtype="mainResult")
		DIVofResults = module_Web.DIV(TableOfResults.write(), _id="tablerizeResult")
		#DIVofResults = module_Web.DIV(message, _id="tablerize")
		webResults = myWeb
		webResults.addBody(DIVofResults.write())
		print webResults
	else:
		print myWeb

###################################################################
if __name__ == "__main__":
    main()
