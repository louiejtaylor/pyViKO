stopCodons = ['TAG', 'TAA', 'TGA']
translation = {'CTT': 'L', 'ATG': 'M', 'AAG': 'K', 'AAA': 'K', 'ATC': 'I', 'AAC': 'N', 'ATA': 'I', 'AGG': 'R', 'CCT': 'P', 'ACT': 'T', 'AGC': 'S', 'ACA': 'T', 'AGA': 'R', 'CAT': 'H', 'AAT': 'N', 'ATT': 'I', 'CTG': 'L', 'CTA': 'L', 'CTC': 'L', 'CAC': 'H', 'ACG': 'T', 'CAA': 'Q', 'AGT': 'S', 'CAG': 'Q', 'CCG': 'P', 'CCC': 'P', 'TAT': 'Y', 'GGT': 'G', 'TGT': 'C', 'CGA': 'R', 'CCA': 'P', 'TCT': 'S', 'GAT': 'D', 'CGG': 'R', 'TTT': 'F', 'TGC': 'C', 'GGG': 'G', 'GGA': 'G', 'TGG': 'W', 'GGC': 'G', 'TAC': 'Y', 'GAG': 'E', 'TCG': 'S', 'TTA': 'L', 'GAC': 'D', 'TCC': 'S', 'GAA': 'E', 'TCA': 'S', 'GCA': 'A', 'GTA': 'V', 'GCC': 'A', 'GTC': 'V', 'GCG': 'A', 'GTG': 'V', 'TTC': 'F', 'GTT': 'V', 'GCT': 'A', 'ACC': 'T', 'TTG': 'L', 'CGT': 'R', 'CGC': 'R'}

import warnings

class SequenceError(Exception):
	pass

def codonify(sequence):
	'''
	Converts an input DNA sequence (str) to a list of codons.
	'''
	if type(sequence) == type([]):
		return sequence
	return [sequence[i:i+3] for i in range(0,len(sequence),3)]

def seqify(cod):
	'''
	Converts an input list of codons into a DNA sequence (str).
	'''
	if type(cod) == type("str"):
		return cod
	sequence = ""
	for codon in cod:
		sequence += codon
	return sequence
	
def translate(codons):
	'''
	Translates a list of DNA codons into the corresponding amino 
	acids, stopping translation if a stop codon is encountered.
	'''
	#optimization from js fnTranslate(): only one loop
	codons = codonify(codons)
	for i in range(0,len(codons)):
		if codons[i] in stopCodons:
			codons = codons[:i]
			break
	if len(codons[-1]) <> 3:
		codons = codons[:-1] # Remove last codon if incomplete
	aa = ''
	for c in codons:
		aa = aa + translation[c]
	return aa

def insertMutation(codons, mut):
	'''
	Takes as input a list of
	`codons` to mutate and a tuple `mut` in the form 
	(index, 'mutated codon') ex. `(3, 'TAA')`.
	Returns a list of codons with a mutation generated by 
	removing the codon to be mutated from the list, then adding
	the newly mutated codon in its position. 
	'''
	iCodons = [c for c in codons]
	iCodons[mut[0]] = mut[1]	
	return iCodons
	
def pointMutant(seq, mut):
	'''
	Takes as input a sequence `seq` to mutate
	and a tuple `mut` in the form (index, 'mutated nt') ex. `(3, 'A')`.
	Returns a nucleotide sequence with a point mutation.
	'''
	return seq[:mut[0]] + mut[1] + seq[mut[0]+1:]
	
def findOverprintedGene(seq, startIndex, frame=1):
	'''
	Given a sequence `seq` and the `startIndex` of 
	an overprinted gene, returns a list of codons that
	correspond to the overprinted gene. The `frame` 
	argument is only necessary if the overprinted
	gene's start codon is before the input sequence, in 
	which case `startIndex` must be -1. <br> <br>
	**NOTE:** the index of the first nucleotide in `seq` is 0,
	so if the overprinted gene starts from the 59th nucleotide
	of `seq`, the `startIndex` will be 58.
	'''
	
	if startIndex <> -1:
		frame = 1   # In case `frame` argument provided erroneously
		codons = codonify(seq[startIndex:])[:-1] # Remove last (incomplete) codon
	else:
		if frame == 1:
			raise SequenceError("The overprinted sequence is in the same frame as the main coding sequence. Please provide a frame argument.")
		codons = codonify(seq[frame - 1:])[:-1] # Remove last (incomplete) codon
	for i in range(0,len(codons)):
		if codons[i] in stopCodons:
			codons = codons[:i]
			break
		
	if codons[0] <> 'ATG' and startIndex <> -1:
		##NOTE: Not all viral genes are initiated with ATG.
		warnings.warn("The first codon of your sequence is not a start codon.")
		
	return codons

def reverseComplement(seq):
	'''
	Given a sequence `seq`, returns the reverse complement.
	'''
	seq = seqify(seq)
	pairs = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
	rev = ""
	#Here should add reverse complements for regex sites? i.e. Y -> R 
	try:	
		for nt in seq[::-1]:
			rev += pairs[nt]
	except KeyError:
		print "Unknown nucleotide '" + nt  + "' encountered."
	
	return rev
	
def findOverlap(seq1, seq2):
	'''
	Given two sequences, returns a tuple `(i1, i2)` where `i1`
	is the index in `seq1` where the overlap with `seq2` begins and
	`i2` is the corresponding index in `seq2`.
	'''
	i1 = 0
	i2 = 0
	if seq1 in seq2:
		i2 = seq2.index(seq1)
	elif seq2 in seq1:
		i1 = seq1.index(seq2)
	else:
		max12 = 0
		max21 = 0
		l1 = len(seq1)
		l2 = len(seq2)
		overall = min(l1,l2) + 1
		for i in xrange(1, overall):
			if seq1[:i] == seq2[l2-i:]:
				max21 = i
			if seq2[:i] == seq1[l1-i:]:
				max12 = i				
		if max12 > max21:
			i1 = l1 - max12
		elif max12 < max21:
			i2 = l2 - max21
		else: 
			raise SequenceError("No overlap detected between input sequences")
			
	return (i1, i2)
	
def readFasta(loc):
	'''
	Reads in a FASTA file, returns tuples in the form
	`('> identifying information, 'sequence')`.
	'''
	f = open(loc, 'r')
	seqs = []
	iden = ''
	seq = ''
	for line in f.readlines():
		if iden == '':
			try:
				if line.lstrip()[0] <> '>':
					raise SequenceError("Invalid file format: id line doesn't begin with '>'")
				iden = line.strip()
			except IndexError: #blank line
				next
				print 'boop'
		else:
			try:
				if line.lstrip()[0] == '>':
					seqs.append((iden, seq))
					iden = line.strip()
					seq = ''
				else:
					seq += line.strip().upper()
			except IndexError: #blank line
				next
	seqs.append((iden, seq))
	f.close()
	return seqs
