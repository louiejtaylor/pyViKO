if __name__ == '__main__':
	
	#####
	##temporary dev hack
	import os
	os.chdir('..')
	#####
	
	from pyviko import core, mutation, restriction, bio

	##	
	#testing
	x = mutation.Mutant('ATGGCCCGGGACGCGCGCTTAGTTAGTTTCTCGAGATAG')
	#                 '''  M  Z  Z  Z  Z  Z  Z  Z  Z  Z  Z  Z  -'''
	#           '''  ATGGATGGCCCGGGACGCGCGCTTAGTTAG'''
	#           '''    M  Z  Z  Z  Z  Z  Z  Z  Z  -'''
	x.setOverGene(startNt = 0, overFrame = 3)			    #'
	#x.setOverGene(overSeq = 'ATGGATGGCCCGGGACGCGCGCTTAGTTAG')	
	print x.findMutants(rSiteLength = 'all')
	print core.findOverlap('ATGGCCCGGGACGCGCGCTTAGTTAGTTTCTCGAGATAG','ATGGATGGCCCGGGACGCGCGCTTAGTTAG')
	##
	
	ovr = core.readFasta('examples/over.fasta')
	toKO = core.readFasta('examples/ko.fasta')
	overlaps = [core.findOverlap(toKO[i][1],ovr[i][1]) for i in range(len(toKO))]
	print overlaps
	