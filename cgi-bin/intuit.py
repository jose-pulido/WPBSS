descriptionText = ''' 
Program to bla bla bla
'''


import sys, os, glob
from Motif import *
from WebMotif import *
from Result import *
import utils
import argparse



homedir = os.path.expanduser('~')
TRANSFACpath = homedir+'/Python/External_Data_SC/TRANSFAC/matrix_seqs/test/'
#TRANSFACpath = homedir+'/Python/External_Data_SC/TRANSFAC/kk/'
JASPAR_sequencesPath = homedir+'/Python/External_Data_SC/JASPAR/sequences/'

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





def main():

	parser = argparse.ArgumentParser(description = descriptionText, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument("seqFile", help="User's sequence File. It will be the previously uploaded file. It's mandatory.")
	parser.add_argument('-t', dest='transfac', action='store_true', help='Compare against TRANSFAC sequences.')
	parser.add_argument('-j', dest='jaspar', action='store_true', help='Compare against JASPAR sequences.')
	parser.add_argument("-m", "--fileOut", dest="ownMatrix", type=argparse.FileType("r"), help="User's own matrix File (TRANSFAC). It will be the previously uploaded file if exists.")
	args = parser.parse_args()

	seqs = utils.readSeq(args.seqFile)
	#minlenseqs = len(seqs[0])
	results = []
	cont =0
	#for s in seqs:
	#	if (len(s)<minlenseqs): minlenseqs = len(s)

	if args.transfac:
		print "TRANSFAC processing..."
		transfac_valid, transfac_NOT_valid = ReadTransfacFile(TRANSFACpath)
		
		for m in transfac_valid:
			results.append( Result(m, seqs) )
		
	if args.jaspar:
		print "JASPAR processing..."
		jaspar_valid, jaspar_NOT_valid = ReadJasparFile(JASPAR_sequencesPath)
		
		for j in jaspar_valid:
			results.append( Result(j, seqs) )
		
		
	for r in sorted(results, key=lambda result: result.BestScore, reverse = True):																		
			cont +=1
			print cont, r.write()

if __name__ == "__main__":
    main()

