from Motif import *
from WebMotif import *


class Result:
	
	def __init__(self, motif, seqs):
		
		self.name = motif.name
		self.format =  motif.format
		self.dic = motif.SC_intuit_Web(seqs)
		self.isEmpty = True		
		self.BSSequence = None
		self.BestScore = None
		self.LOGOpath = motif.LOGOpath
		
		self.BestValues()
		
	def BestValues(self):
		if self.dic:
			self.BSSequence = sorted(self.dic, key=lambda key: self.dic[key], reverse = True)[0]
			self.BestScore = self.dic[self.BSSequence]
			self.isEmpty = False
			
	def write(self):
	
		if self.isEmpty:
			ret = "Empty dic. Sequences smaller than matrix size."
		else:
			ret = self.format + self.name + '  Better Scored Sequence = ' + self.BSSequence + '   -   SCORE = ' + str(self.BestScore)
		return ret
