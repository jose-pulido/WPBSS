import utils
import types
import sys, os
from numpy import *
				

class Motif:
	
	def __init__(self, fileIn, format):
		
		self.name = None
		self.format = format
		self.ID = None
		self.FSM = None							#Boolean - Te dice si es una matriz de frecuencias o de conteos			
		self.n = None							#Longitud de las secuencias

		self.numSamples = None
		self.originalMatrix = None
		self.validMatrix = None					#matriz construida unicamente con secuencias validas
		self.matFSM = None						#matriz de conteos (ver ejemplo en pag. 93 Tesis)
		self.matPSSM = None						#matriz de conteos dividida entre el numero de samples (ver ejemplo en pag. 93 Tesis)
		self.intuitM = None						# Matrix for the membership degree "\mu"   16 rows
		self.intuitV = None						# Matrix for the non-membership degree "\nu"

		self.seq = []
		self.validSeqs = []
		self.discardSeqs = []
		self.QF = None
		self.validMotif = None
		self.species = []
		self.LOGOpath = None
		
		
		
		if(fileIn != None):
			self.readFromFile(fileIn, format)
			
			if self.validMotif:													# Si el motivo no es valido, no tiene sentido seguir leyendo el resto
		
				#self.LOGOpath = self._createLOGO()		
				self.validMatrix = self._validSeqsMatrix()											# Creo una matriz unicamente con los valores de las secuencias validas
							 													# Con esta matriz se ejecuta el resto del algoritmo
				self.numSamples = len(self.validSeqs)
				self.n = self.validMatrix.shape[0]
				self.matPSSM = (self.validMatrix / self.numSamples)
				self.intuitM = zeros((16,(self.n * (self.n -1))/2))	
				self.intuitV = zeros((16,(self.n * (self.n -1))/2))
				
				
				#print self.validMatrix
				#print self.matPSSM
				
				self.computeIntuitionisticMotif()
			
		else:
			print "Wrong usage for Motif.__init__()"

	

	
	def calculatePSSMFromFSM(self):
		self.matPSSM = array(self.matFSM,float)				#returns an array (type = 'numpy.ndarray') with the specified type (float)
		self.matPSSM /= self.numSamples						




	def calculateFSMFromPSSM(self,numSamples=None):
		if numSamples == None:
			numSamples = self.numSamples

		self.numSamples = numSamples
		self.matFSM = array(self.matPSSM*self.numSamples).astype(int)
		for i in range(self.n):											#Soluciona problema de redondeo
			s = sum(self.matFSM[i,:])
			ind = self.matFSM[i,:].tolist().index(max(self.matFSM[i,:]))
			self.matFSM[i,ind] += self.numSamples - s
		


	def computeNumSamples(self,mat):										## UPDATE!!!! self.numSamples = len(self.validSeqs)
		numSamples = 0
		for i in range(len(mat)):
			if numSamples < sum(mat[i,:]):
				numSamples = sum(mat[i,:])
		return numSamples



	def pseudoCountFSM(self):									#Not used!!!
		if not all(self.matFSM):
			
			self.matFSM += 1
			self.numSamples += 4
			self.calculatePSSMFromFSM()



	def pseudoCountPSSM(self):									#If some value in self.matPSSM == 0, add 0.000001 to each value.
		if not all(self.matPSSM):
			
			self.matPSSM += 0.000001
			self.calculateFSMFromPSSM()
				
						 

	def ICmatrix(self):
	
		self.pseudoCountPSSM()
		matAux = self.matPSSM * (log(self.matPSSM)/log(2))		
		return matAux
				
	
	
	def _seqsAligner(self, seqini, ref, lenseq, gap, thread):
		"""For Transfac files, reads the alignment info and constructs a sequence fulfilling with 'N' the gaps in order to be processed."""
		
	
		aligSeq = ''
		for elm in seqini.split():								#Si la secuencia tenia huecos al principio o en medio, se los quito
			aligSeq = aligSeq+elm
	
		if (len(aligSeq)!=lenseq):								#Si la secuencia tiene el tamanio de la matriz, no hay que procesarla.

			if thread == 'p':									#Orientacion positiva

				if gap:
			
					insertPos = [(g-ref) for g in gap]
				
					for pos in insertPos:
										
						if pos<0:
							aligSeq = aligSeq + 'N'
						else:
							aligSeq = aligSeq[0:pos]+'N'+aligSeq[pos:]	
				if ref<0:										#Tambien se usa esta notacion para hacer inserciones al inicio
					for i in range(abs(ref)):
						aligSeq = 'N'+aligSeq

			else:												#Orientacion negativa
				if gap:
			
					insertPos = [(lenseq-g) for g in gap[::-1]]

					for pos in insertPos:
					
						if pos<0:
							aligSeq = 'N' + aligSeq
						else:
							aligSeq = aligSeq[0:pos]+'N'+aligSeq[pos:]

				if ref<0:										#Tambien podria utilizarse esta notacion para hacer inserciones al final
					for i in range(abs(ref)):
						aligSeq = aligSeq + 'N'
				
		self.seq.append(aligSeq)
	
	
	
	
	
	def _passSQC(self, format, matrixlen=0, minValidSeqs=3):
		"""Motif Sequences Quality Control. Analyze every sequence stored in self.seq and check two conditions: length = length (Motif Matix) and
		   all the characters are valid ('A', 'C', 'G', 'T', 'N'). Valid and Invalid sequences are stored separately in self.validSeqs or 
		   self.discardSeqs. Then calculates the Quality Factor (self.QF) and decide if the motif is valid or not (self.validMotif).
		   
		   For jaspar format, matrixlen = maxlenSeq, therefore, sequences with smaller size will be discarded."""
		   
		
		validChars = set(['A', 'C', 'G', 'T', 'N'])

		#if format == 'jaspar':
		#	#Obtain matrixlen from JASPAR files
		#	pass
		
		
		
		for seq in self.seq:
		
			ok = True
			if (len(seq)==matrixlen):
				for c in seq:
					if c not in validChars:
						ok = False
						break
				if 'NNNN' in seq:
					ok = False		
			else:
				ok = False
						
			if ok:
				self.validSeqs.append(seq)
			else:
				self.discardSeqs.append(seq)
	
		self.QF = float(len(self.validSeqs))/(len(self.seq))			# calcula el factor de Calidad: relacion entre secuencias validas y totales

		if ( (self.QF >= 0.25) and (len(self.validSeqs) >= minValidSeqs) ): 
			self.validMotif = True
		else:
			self.validMotif = False
			#print self.name, self.validMotif
	
		
	
	def _validSeqsMatrix(self):								
		"""Constructs a Matrix only with the valid and aligned sequences."""
		mat = []	
		lenSeq = len(self.validSeqs[0])						#En este punto todas las secuencias son validas y de igual longitud = len(Motifmatrix)

		for pos in range(lenSeq):						
			nA = 0;
			nC = 0;
			nG = 0;
			nT = 0;
			
			for seq in self.validSeqs:
				
				if (pos <= len(seq)-1):						
					if (seq[pos] == 'A'): nA += 1
					if (seq[pos] == 'C'): nC += 1
					if (seq[pos] == 'G'): nG += 1
					if (seq[pos] == 'T'): nT += 1
					if (seq[pos] == 'N'): 						
						nA += 0.25
						nC += 0.25
						nG += 0.25
						nT += 0.25
		
			cont = [nA, nC, nG, nT]
			mat.append([float(s) for s in cont])
			
		return array(mat,float)
	
		
	def _createLOGO(self):
	
		homedir = os.path.expanduser('~')
		
		if (self.format=="Transfac"):
			LOGOpath = homedir+'/External_Data_SC/LOGO/LOGO_T/Temp.logo.txt'
			LOGOpng = homedir+'/External_Data_SC/LOGO/LOGO_T/'+self.name+'.logo.png'
			
		if (self.format=="Jaspar"):
			LOGOpath = homedir+'/External_Data_SC/LOGO/LOGO_J/Temp.logo.txt'
			LOGOpng = homedir+'/External_Data_SC/LOGO/LOGO_J/'+self.name+'.logo.png'
			
		if (self.format=="User"):
			LOGOpath = homedir+'/External_Data_SC/LOGO/LOGO_U/Temp.logo.txt'
			LOGOpng = homedir+'/External_Data_SC/LOGO/LOGO_U/'+ self.name+ '.logo.png'	
		
		ftemp = open(LOGOpath, 'w')
		for seq in self.validSeqs:
			
			content = seq + '\n'
			ftemp.write(content)
		ftemp.close()
		
		
		os.system('weblogo -f ' + LOGOpath + ' -o ' + LOGOpng + ' -F png')
		
		return LOGOpng
		
		
		
		
		
		
		

	def readFromFile(self,fileIn, format):
		"""Specifies how to read nd fulfill the Motif depending on the format"""
		
		allowed_transfac_Formats = ["Transfac", "transfac"]
		allowed_jaspar_Formats = ["Jaspar", "jaspar"]
		allowed_user_Formats = ["User", "user"]
		#if format not in allowedFormats:
		#	raise sdalfjasd
		if format in allowed_transfac_Formats:
			
			self._readTransfacFile(fileIn)
	
		elif format in allowed_jaspar_Formats:
		
			self._readJasparFile(fileIn)
			
		elif format in allowed_user_Formats:
		
			self._readTransfacFile(fileIn)
			self.LOGOpath = self._createLOGO()

	def _readJasparFile(self,fileIn):									#Read a Jaspar formatted file and fill the motif object properly
		"""Read a Jaspar formatted file and fill the motif object properly"""
			
			#search the matrix into the all-matrix file	
			

		if type(fileIn) == types.StringType: fileIn = open(fileIn)
		name = fileIn.name.split('/')[len(fileIn.name.split('/'))-1].split('.sites')[0]
		header = fileIn.readline().replace('\n','').split()
		if len(header)>1:
			AC  = header[1]
		else:
			AC = ""	
		
		self.name = name
		self.ID = AC
		
		line = fileIn.readline()
		while line:
			if (line[0]!='>'):
				
				charsLine = line.replace('\n','')
				clseq = ""
				for c in charsLine:
					if (c.isupper()):
						clseq = clseq+c
				self.seq.append(clseq)
				
			line = fileIn.readline()

				
		maxlenSeq = 0
		maxSeq = ""
		for s in self.seq:
			if (len(s) > maxlenSeq) :
				maxlenSeq = len(s)
				maxSeq = s
		cont = 0
		
		

		self._passSQC('jaspar', matrixlen = maxlenSeq)
		
		
			
			
	def _readTransfacFile(self,fileIn):									
		"""Read a Transfac formatted file and fill the motif object properly."""
		
		check_species, fileIn = utils.AreSpecies(fileIn)				# sometimes there are no species related. We check it
																		# fileIn is opened because AreSpecies function. Point again to the beginning
														
		#if type(fileIn) == types.StringType: fileIn = open(fileIn)
		mat = []
		header = fileIn.readline().replace('\n','').split()				#read matrix name (name)
		name = header[1]
		col = fileIn.readline()
		while (col[0:2] != 'ID'):
			col = fileIn.readline()
		
		AC = col.replace('\n','').split()[1]							#read matrix ID (AC)
		
		self.name = name
		self.ID = AC
		
		if check_species:
			col = fileIn.readline()										#read the species
			while (col[0:2] != 'BF'):
				col = fileIn.readline()
			while(col and col[0:2] != 'XX'):
				if (not col.split(';')[2].split(': ')[1] in self.species): self.species.append(col.split(';')[2].split(': ')[1])
				col = fileIn.readline()
		
		col = fileIn.readline()											#read the matrix
		while (col[0:2] != '01'):
			col = fileIn.readline()
		
		while(col and col[0:2] != 'XX'):
			col = col.replace('\n','').split()[1:5]
			mat.append([float(s) for s in col])
			col = fileIn.readline()
		mat = array(mat,float)
		self.originalMatrix = mat		
		
		col = fileIn.readline()											#read the sequences
		while (col[0:2] != 'BS'):
			col = fileIn.readline()		
		
	
		while(col and col[0:2] != 'XX'):
			#self.seq.append(col.split(';')[0].split()[1].upper())
			seqini = col.split(';')[0].split('BS  ')[1].upper()				#Utilizo el separador 'BS  ' y no '' para poder atrapar secuencias con huecos en el medio
			ref = int(col.split(';')[2])									#Si utilizara el separador '' las dividiria en dos y las perderia
			lenseq = int(col.split(';')[3])
			gap = col.split(';')[4].split()
			thread = col.split(';')[5].split()[0].split('.')[0]
			
			if ((len(gap)==1) and (',' in gap[0]) ):						#Casos donde anotacion TRANSFAC no separa los gaps con coma y espacio
				gap = gap[0].split(',')										#sino solo comas
				gap = [(int(g)) for g in gap]
				
			else:
				gap = [int(g.split(',')[0]) for g in gap]
			
			self._seqsAligner(seqini, ref, lenseq, gap, thread)				# Alinea la secuencia y la guarda en la clase motivo ya alineada			
			
			col = fileIn.readline()
		
		
		self._passSQC('transfac', matrixlen=lenseq)							# Coge las secuencias guardadas y mira si son validas o no almacenandolas
																			# respectivamente entre validas y no validas
		
									
		
		
		




	
	def computeIntuitionisticMotif(self):
		t = float(len(self.validSeqs))
		F = zeros((16,(self.n * (self.n -1))/2))
		a = 0.000001 * 0.000001
	

		dposmatFSM = {}
		dposmatFSM['A'] = 0
		dposmatFSM['C'] = 1
		dposmatFSM['G'] = 2
		dposmatFSM['T'] = 3

		drow = {}						#Diccionario con las posibles combinaciones de dos bases (AA, AC, AG,... TA, TC, TG, TT) numeradas del 0 al 15
		drevrow = {}					#Idem cambiando las clave por los valores y viceversa
	
		conti = 0
		for i in ['A','C','G','T']:					
			for j in ['A','C','G','T']:
				drow[str(i)+str(j)] = conti
				drevrow[conti] = str(i)+str(j)
				conti += 1

		dcol = {}						#Diccionario con las posibles combinaciones entre dos columnas distintas[(0,1),(0,2),...,(n-2, n-1)] numeradas
		drevcol = {}					#Idem cambiando las clave por los valores y viceversa
		conti = 0
		for i in range(self.n):
			for j in range(i+1,self.n):
				dcol[(i,j)] = conti
				drevcol[conti] = (i,j)
				conti += 1
		
		#for s in self.seq:				# Esto lo cambio porque ahora solo utilizo las secuencias validas
		for s in self.validSeqs:
			
			for indexi,posi in enumerate(s[0:-1]):
				for indexj,posj in enumerate(s[indexi+1:]):
					#print s, s[0:-1], s[indexi+1:], (indexi, posi), (indexj,posj)
					#F[drow[str(posi)+str(posj)],dcol[(indexi,indexj+indexi+1)]] += 1
					F = utils.Fvalue(F, drow, dcol, str(posi), str(posj), indexi, (indexj+indexi+1))
					#print 'F[drow['+str(posi)+str(posj)+'], dcol[(' + str(indexi) + ',' + str(indexj+indexi+1) + ')]]'
					#+ str(indexj+indexi+1) + ')]]'
		
		self.intuitM = (F /t) + a
		
		for indexi in range(self.n):
			for indexj in range(indexi+1,self.n):
				for posi in ['A','C','G','T']:
					for posj in ['A','C','G','T']:
						izq = self.matPSSM[indexi][dposmatFSM[str(posi)]]
						dcha = self.matPSSM[indexj][dposmatFSM[str(posj)]]
						tot1 = (izq + dcha) / 2.
						oldM = self.intuitM[drow[str(posi)+str(posj)],dcol[(indexi,indexj)]]
						self.intuitM[drow[str(posi)+str(posj)],dcol[(indexi,indexj)]] += (1-oldM)*tot1
						
						#k1 = dposmatFSM[str(posi)]
						#k2 = dposmatFSM[str(posj)]						
						#print indexi, indexj, posi, posj
						#print self.matPSSM
						#print "izq = self.matPSSM[" + str(indexi) + "][dposmatFSM[str(" + str(posi) + ")]]" + "   =   " + "self.matPSSM[" + str(indexi) + "][" + str(k1) +"] = ", izq	
						#print "dcha = self.matPSSM[" + str(indexj) + "][dposmatFSM[str(" + str(posj) + ")]]" + "   =   " + "self.matPSSM[" + str(indexj) + "][" + str(k2) +"] = ", dcha
						#print "tot1 = ", tot1
						#print "oldM = ", oldM
						#print "valor a cambiar: self.intuitM[drow[" + str(posi)+str(posj)+ "],dcol[(" + str(indexi) + "," + str(indexj) + ")]] = self.intuitM[" + str(drow[str(posi)+str(posj)]) + "," + str(dcol[(indexi,indexj)]) + "] = ", (1-oldM)*tot1
						#print self.intuitM
							
						#raw_input("Press any Key")
		
						
		ic = self.ICmatrix()
		
		for indexi in range(self.n):
			for indexj in range(indexi+1,self.n):
				for posi in ['A','C','G','T']:
					for posj in ['A','C','G','T']:
						izq = (2 + ic[indexi,dposmatFSM[str(posi)]]) / 2
						dcha = (2 + ic[indexj, dposmatFSM[str(posj)]]) / 2
						tot1 = (izq + dcha) / 2
						tot2 = tot1 * (1- self.intuitM[drow[str(posi)+str(posj)],dcol[(indexi,indexj)]])
						self.intuitV[drow[str(posi)+str(posj)],dcol[(indexi,indexj)]] = tot2
						
						
						
						
	
	def _isValidSeq(self,seq,minSizePerc=1.0):
		relativeSize = float(len(seq)) / self.n
		ret = True if relativeSize >= minSizePerc else False
		
		return ret	
		
		
	def generate_dcols(self, smallSeq):
		#print self.intuitM
		ndcols = self.n - len(smallSeq) +1
		dcol_list = []
		drevcol_list = []
		#print self.name, self.n, len(smallSeq), '\n'
		for n in range(ndcols):
			
			dcol = {}
			drevcol = {}
			conti = 0
			for i in range((self.n)):
				for j in range(i+1,self.n):
					if ( (i>=(n)) and (j<=(self.n - ndcols +n)) ):
						dcol[(i,j)] = conti
						drevcol[conti] = (i,j)									
						#print len(dcol_list), ", dcol[("+ str(i) + "," + str(j) + ")] = " + str(conti), self.name, self.n					
					conti += 1
			#print dcol
			#print len(dcol)
			#for i,j in sorted(dcol.iteritems(), key=lambda (k,v): (v,k)):
			#	print i, j, dcol[i]	
			dcol_list.append(dcol)
			drevcol_list.append(drevcol)
			
		#print dcol_list
		#print '\n'
		return dcol_list, drevcol_list
		
		
	def generate_A(self, smallSeq, dcol_list):
		nMatrix = self.n - len(smallSeq) +1
		matrix_list = []
		#print self.intuitM
		#print '\n'
		for dcol in dcol_list:
			mM = zeros(shape=(len(self.intuitM),len(dcol)))
			mV = zeros(shape=(len(self.intuitV),len(dcol)))
			column_index = 0
			for i,j in sorted(dcol.iteritems(), key=lambda (k,v): (v,k)):
				
				mM[:,column_index:column_index+1] = self.intuitM[:,j:j+1]
				mV[:,column_index:column_index+1] = self.intuitV[:,j:j+1]
				column_index +=1
			#print mM
			#print mV
			#print '\n'
			
			mA = [mM.transpose(), mV.transpose()]
			#print mA
			#print '\n'
			matrix_list.append(mA)
		
		return matrix_list
	
	
	
	
	
			
	def SC_intuit_forSmallerSeqs(self, smallSeq, A):
		#pass
		# TODO!
		# El procedimiento seria:
		# values = []
		# para cada submotivo necesario:
			# currSubMotivo = self._createSubmotif(ini,fin)
			# values.append(currSubMotivo.Sc_intuit(seq))
		
		# return values
		
		drow = {}
		drevrow = {}
		
		conti = 0
		for i in ['A','C','G','T']:
			for j in ['A','C','G','T']:
				drow[str(i)+str(j)] = conti
				drevrow[conti] = str(i)+str(j)
				conti += 1
		
		dcol = {}
		drevcol = {}
		conti = 0
		for i in range(len(smallSeq)):
			for j in range(i+1,len(smallSeq)):
				dcol[(i,j)] = conti
				drevcol[conti] = (i,j)
				conti += 1
		
		#print shape(A[0]), A[0]
		#print shape(A[1]), A[1]
		#print self.validSeqs
		simsNorm = []
		
		for indexi,posi in enumerate(smallSeq[0:-1]):
			for indexj,posj in enumerate(smallSeq[indexi+1:]):
				maxSim,minSim = utils.computeMaxMin(A,dcol[(indexi,indexj+ indexi +1)])
				mu = A[0][dcol[(indexi,indexj+ indexi +1)]][drow[posi+posj]]
				maxV =  max(A[1][dcol[(indexi,indexj+ indexi +1)]])
				v = maxV - A[1][dcol[(indexi,indexj+ indexi +1)]][drow[posi+posj]]			#If there are many 'N', same values can be in A[1][dcol[(indexi,indexj+ indexi +1)]] and if this value is tmaximum -> v = 0 -> curSim = 0 maxSim=0 and minSim=0 (see utils.computeMaxMin) -> curSimNorm = nan
				curSim = mu * v
				curSimNorm = (curSim - minSim) / (maxSim -minSim)
				
				#print A[1][dcol[(indexi,indexj+ indexi +1)]]
				#print [drow[posi+posj]]
				#print A[1][dcol[(indexi,indexj+ indexi +1)]][drow[posi+posj]]
				#print mu, maxV, curSim, maxSim, minSim, (maxSim -minSim), curSimNorm
				#raw_input("Press Enter to continue...")
				
				simsNorm.append(curSimNorm)
		return average(simsNorm)
	
	
	
	def SC_intuit(self, seq):								#def SC_intuit(self,seq,minSizePerc=1.0):
		"""
		This method REQUIRES that len(seq) == self.n
		Right now we consider only sequences with length higher or equal to the length of the motif"""

		
		if not self.validMotif:
			# hacer que se informe de que el motivo no mola y no se va a tener en cuenta. La funcion debe devolver un valor que informe del hecho. Por ejemplo se me ocurre None
			pass
		if (len(seq) != self.n):
		
			raise AttributeError("SC_intuit REQUIRES that len(seq) == self.n")
		
		#if not self._isValidSeq(seq,minSizePerc):
		#	self.SC_intuit_forSmallerSeqs(seq) # TODO! YOu would need to program this method
		
		else:
			
			drow = {}
			drevrow = {}
		
			conti = 0
			for i in ['A','C','G','T']:
				for j in ['A','C','G','T']:
					drow[str(i)+str(j)] = conti
					drevrow[conti] = str(i)+str(j)
					conti += 1
	
			dcol = {}
			drevcol = {}
			conti = 0
			for i in range(self.n):
				for j in range(i+1,self.n):
					dcol[(i,j)] = conti
					drevcol[conti] = (i,j)
					conti += 1
	
		
			A = [self.intuitM.transpose(),self.intuitV.transpose()]
		
		
			simsNorm = []
			for indexi,posi in enumerate(seq[0:-1]):
				for indexj,posj in enumerate(seq[indexi+1:]):
					maxSim,minSim = utils.computeMaxMin(A,dcol[(indexi,indexj+ indexi +1)])
					mu = A[0][dcol[(indexi,indexj+ indexi +1)]][drow[posi+posj]]
					maxV =  max(A[1][dcol[(indexi,indexj+ indexi +1)]])
					v = maxV - A[1][dcol[(indexi,indexj+ indexi +1)]][drow[posi+posj]]
					curSim = mu * v
					curSimNorm = (curSim - minSim) / (maxSim -minSim)
					simsNorm.append(curSimNorm)
			return average(simsNorm)
