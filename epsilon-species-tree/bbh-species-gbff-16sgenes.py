import pandas as pd
from os.path import dirname, abspath

# cross reference agains the e-proteobacteria-for-bbh table to retain only the ones i included in bbh. but also check the other way, to make sure I have all bbh bacteria represented. 
# check if gcf bbh's are present in genbank-info: note which are not in genbank-info. 


# OPEN THE TWO FILES I'LL BE COMPARING #

parentdir = dirname(dirname(dirname(abspath(__file__))))
bbhfile = parentdir + '/3_bidirectional-best-hits//e-proteobacteria_for_BBH.tsv'

gb = pd.read_csv('genbank-16s-info.tsv', sep='\t')
bbh = pd.read_csv(bbhfile, sep='\t')


# GET THEIR GCF COLUMNS AND COMPARE #

#lists of the gca/gcf numbers form both files
bbh_gcf = [i for i in bbh['subject_gcf']]
gb_gcf = [i for i in gb['gcf'].drop_duplicates()]


for ele in bbh_gcf:
	if ele not in gb_gcf:
		print('not in genbank: ', ele) # if gcf not present in the gb files, let me know which

for ele in gb_gcf:
	if ele not in bbh_gcf:
		print('not in bbh: ', ele) # same for bbh	 

# one accession is printed: GCF_000987835.1 is not in gb, GCA_000987835 is not in bbh. so they're the same, but one is genbank and other is refseq. the same sequence so not a problem.
