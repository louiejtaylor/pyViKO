stopCodons = ['TAG', 'TAA', 'TGA']

translation = {'CTT': 'L', 'ATG': 'M', 'AAG': 'K', 'AAA': 'K', 'ATC': 'I', 'AAC': 'N', 'ATA': 'I', 'AGG': 'R', 'CCT': 'P', 'ACT': 'T', 'AGC': 'S', 'ACA': 'T', 'AGA': 'R', 'CAT': 'H', 'AAT': 'N', 'ATT': 'I', 'CTG': 'L', 'CTA': 'L', 'CTC': 'L', 'CAC': 'H', 'ACG': 'T', 'CAA': 'Q', 'AGT': 'S', 'CAG': 'Q', 'CCG': 'P', 'CCC': 'P', 'TAT': 'Y', 'GGT': 'G', 'TGT': 'C', 'CGA': 'R', 'CCA': 'P', 'TCT': 'S', 'GAT': 'D', 'CGG': 'R', 'TTT': 'F', 'TGC': 'C', 'GGG': 'G', 'GGA': 'G', 'TGG': 'W', 'GGC': 'G', 'TAC': 'Y', 'GAG': 'E', 'TCG': 'S', 'TTA': 'L', 'GAC': 'D', 'TCC': 'S', 'GAA': 'E', 'TCA': 'S', 'GCA': 'A', 'GTA': 'V', 'GCC': 'A', 'GTC': 'V', 'GCG': 'A', 'GTG': 'V', 'TTC': 'F', 'GTT': 'V', 'GCT': 'A', 'ACC': 'T', 'TTG': 'L', 'CGT': 'R', 'CGC': 'R'}

def codonify(sequence):
    '''
    Converts an input DNA sequence (str) to a list of codons.
    '''
    return [sequence[i:i+3] for i in range(0,len(sequence),3)]

def seqify(cod):
    '''
    Converts an input list of codons into a DNA sequence (str).
    '''
    sequence = ""
    for codon in cod:
        sequence += codon
    return sequence
    
def translate(codons):
    '''
    Translates a list of DNA codons into the corresponding amino acids (str).
    '''
    aa = ''
    for c in codons:
        aa = aa + translation[c]
    return aa

def insertMutation(codons, mut):
    '''
    Takes as input a list of
    `codons` to mutate and a tuple `mut` in the form 
    (index, 'mutated codon') ex. (3, 'TAA').
    Returns a list of codons with a mutation generated by 
    removing the codon to be mutated from the list, then adding
    the newly mutated codon in its position. 
    '''
    codons.pop(mut[0])
    newCodons = codons[:mut[0]] + [mut[1]] + codons[mut[0]:]
    return newCodons

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
        codons = codonify(seq[startIndex:])[:-1]
    else:
        if frame == 1:
            print "WARNING THIS IS THE SAME FRAME"
        codons = codonify(seq[frame - 1:])[:-1] # Remove last (incomplete) codon

    for i in range(0,len(codons)):
        if codons[i] in stopCodons:
            codons = codons[:i]
            break
        
    if codons[0] <> 'ATG' and startIndex <> -1:
        print "WARNING: NOT START CODON"
        
    # Throw warnings? Or just print them?
    return codons