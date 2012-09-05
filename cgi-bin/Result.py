from Motif import *
from WebMotif import *


class Result:
	
	def __init__(self, motif, seqs):
		
		self.name = motif.name
		self.ID = motif.ID
		self.format =  motif.format
		self.dic = motif.SC_intuit_Web(seqs)
		self.isEmpty = True		
		self.BSSequence = None
		self.BestScore = None
		self.LOGOpath = motif.LOGOpath
		self.location = []
		self.length = motif.n
		
		self.BestValues(seqs)
		
	def BestValues(self, seqs):
		if self.dic:
			self.BSSequence = sorted(self.dic, key=lambda key: self.dic[key], reverse = True)[0]
			self.BestScore = self.dic[self.BSSequence]
			self.isEmpty = False
			seqsCont = 0
			for s in seqs:
				seqsCont += 1
				index = s.seq.find(self.BSSequence)
				if (index != -1):
					preSeq = ''
					postSeq = ''
					
					if index==0:
						k =0
					else:
						for k in range(index):
							preSeq = preSeq + s.seq[k].lower()
						
					k = k+len(self.BSSequence)+1
					while k<len(s.seq):
						postSeq = postSeq + s.seq[k].lower()
						k+=1
					
					self.location = [s.name[1:], preSeq, postSeq]
					break
			
	def write(self):
	
		if self.isEmpty:
			ret = "Empty dic. Sequences smaller than matrix size."
		else:
			ret = self.format + self.name + '  Better Scored Sequence = ' + self.BSSequence + '   -   SCORE = ' + str(self.BestScore)
		return ret
