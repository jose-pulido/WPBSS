from Motif import *




class WebMotif(Motif):

	def SC_intuit_Web(self,seqs):

		num_seqs = len(seqs)
		dic = {}
		k=1
		for s in seqs:
			
			if self._isValidSeq(s.seq):
			
				num_operations = len(s.seq) - self.n + 1
				inicont = 0
				endcont = self.n

				for j in range(num_operations):
					subseq = s.seq[inicont:endcont]

					if not subseq in dic:								#If some subseq have been already processsed, we don't do it again. Same result.
						dic[subseq] = self.SC_intuit(subseq)  
							
					inicont += 1
					endcont += 1
		
			else:
				#self.SC_intuit_forSmallerSeqs(seq) # TODO! YOu would need to program this method
				dcol_list, drevcol_list = self.generate_dcols(s.seq)
				A_list = self.generate_A(s.seq, dcol_list)
				
				for index in range(len(A_list)):
					
					if not s.seq in dic:
						dic[s.seq] = self.SC_intuit_forSmallerSeqs(s.seq, A_list[index])					# First submatrix processed for that sequence
						#print dic[s.seq]	
					else:
						newscore = self.SC_intuit_forSmallerSeqs(s.seq, A_list[index])					# Rest of the submatrix
						#print newscore
						if (newscore > dic[s.seq]) :
							dic[s.seq] = newscore	
		# HABRA QUE VER COMO SE PRESENTAN LOS RESULTADOS EN CASO DE QUE LAS SECUENCIAS SEAN MENORES, SI HAY UN MINIMO TAMANIO DE SEQ, ETC...
	
		
		return dic
		
	


		


