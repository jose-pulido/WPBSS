import types
from Sequence import *

def EOF(f):
	pos = f.tell()					#f.tell() returns the current position of the file read/write pointer within the file (Integer Bytes).
	if(f.readline()):
		f.seek(pos)					#moves #pos bytes ahead
		return False

	else:
		return True	

def decideFSMorNot(mat):
	for i in range(len(mat)):
		#print sum(mat[i,:])
		if sum(mat[i,:]) > 1.5: return True
	return False
	
#def readSeq(fileIn):									
#	f = open(fileIn)
	#return f.readline().upper().replace('\n','')
	#myseqs = []
	#for line in f:													#seqs-size LIMITATION to one-line
	#	if (line[0] !=	'>'):
	#		myseqs.append(line.upper().replace('\n',''))
#	lines = f.readlines()
#	myseqs = []
#	seq = ""
#	for l in range(len(lines)):
#		if ((lines[l][0] == '>')):
#			if seq:
#				myseqs.append(seq)
#				seq=""	
#		else:
#			seq = seq + lines[l].upper().replace('\n','')
#	myseqs.append(seq)	
#	return myseqs

def readSeq(fileIn):									
	f = open(fileIn)
	Seqs = []
	seq = ""
	line = f.readline()
		
	while line:
		if (line[0] == '>'):
			
			if seq:
				Seqs.append(Sequence(name, seq))
				seq=""
					
			name = line.replace('\n','')
		else:
			seq = seq + line.upper().replace('\n','')
			
		line = f.readline()
	if (name and seq):
		Seqs.append(Sequence(name, seq))
	return Seqs


def computeMaxMin(A,row):
	_max = -1
	_min = 2
	maxV =  max(A[1][row])
	
	for i in range(16): 
		mu = A[0][row][i]
		v = maxV - A[1][row][i]
		curSim = mu * v
		if curSim > _max: _max = curSim
		if curSim < _min: _min = curSim
	
	return _max,_min


def AreSequences(text):
	lines = text.split('\n')
	seqs = False
	for l in lines:
		if (l[0:2] and l[0:2] == 'BS'):
			seqs = True
			break
	return seqs

def AreSpecies(fileIn):
	if type(fileIn) == types.StringType: fileIn = open(fileIn)
	col = fileIn.readline()
	seqs = False
	while col and not EOF(fileIn):
		if col[0:2] == 'BF':
			seqs = True
			break
		col = fileIn.readline()
	#fileIn.close()
	fileIn.seek(0)
	return seqs, fileIn

		
		
		
def Fvalue(F, drow, dcol, b1, b2, c1, c2):					
	"""Fulfill F matrix being able to read 'N' chars in the sequences. Used by function computeNumSamples(self,mat)
				- If the base-pair is XN or NX, the score will be 0.25 for each of the four possibilities
				- If the base-pair is NN, the score will be 0.0625 for each of the sixteen possibilities
				- If the base-pair is XY, the score will be 1 for this only possibility, like it was done before."""
				
	if 'N' in b1+b2:
		if ((b1=='N')and(b2!='N')):
			for i in ['A','C','G','T']:
				F[drow[str(i)+b2],dcol[(c1,c2)]] += 0.25

		if ((b1!='N')and(b2=='N')):
			for i in ['A','C','G','T']:
				F[drow[b1+str(i)],dcol[(c1,c2)]] += 0.25	

		if ((b1=='N')and(b2=='N')):
			for i in ['A','C','G','T']:
				for j in ['A','C','G','T']:
					F[drow[str(i)+str(j)],dcol[(c1,c2)]] += 0.0625
	else:
		F[drow[b1+b2],dcol[(c1,c2)]] += 1

	return F
