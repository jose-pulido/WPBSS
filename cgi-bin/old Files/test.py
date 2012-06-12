#!/usr/bin/python
#Importar modulos CGI
import cgi, cgitb

print "Content-type: text/html\n\n"	# Imprescindible para explicar que lo que se imprime es HTML


print ("""

<!DOCTYPE HTML>

<html>
  <Title>Hello in HTML</Title>
<body>
  <p>Hello There!</p>
  <p><b>Hi There!</b></p>  
</body>
</html>

""")
