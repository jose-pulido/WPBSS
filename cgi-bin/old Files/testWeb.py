descriptionText = '''
Program to 

'''

#! /usr/bin/python 


import module_Web



######################### MAIN ##################################

def main():
	img = module_Web.Image("red_tick.jpg", "http://127.0.0.1/html5/images/")
	print img
	print '\n'

	inp = module_Web.Input("file", value="myvalue", event="algosasdf", name="sdfsd")	
	print inp
	print '\n'

	frm = module_Web.Form(inp.write(), "/cgi-bin/upload.py", _id="myID", classtype="myCLass")	
	print frm
	print '\n'

	div = module_Web.DIV(frm.write(), _id="myDIVid", classtype="myDIVclass")	
	print div
	print '\n'

	footer  = '''Max Planck Institute for Infection Biology - Charit&eacute;platz 1 - D-10117 Berlin - GERMANY'''
	header = '''Web Platform For Binding Sites Sequences'''
	web = module_Web.HTML()
	web.addTitle("WPBSS")
	web.addHeader(header)
	web.addFooter(footer)
	web.addBody(div.write())
	web.add_styleFiles("sheet1.css")
	web.add_scriptFiles("jquery-1.7.1.js")
	web.add_scriptFiles("funct3.js")
	web.WriteHTMLfile("myWeb.html")
	print web.style_Files
	print web.script_Files
###################################################################
if __name__ == "__main__":
    main()
