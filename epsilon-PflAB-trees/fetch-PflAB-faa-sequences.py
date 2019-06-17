import pandas as pd 
from os.path import dirname, abspath
from Bio import SeqIO, Entrez
Entrez.email = 'td1515@ic.ac.uk'
Entrez.api_key = '41267f8592172caaa22ab00ec006c4330208'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OPEN RESULTS FILE AND GET HITS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

parentdir = dirname(dirname(dirname(abspath(__file__))))
resultsdir = parentdir + '/3_bidirectional-best-hits/'

def open_result(query):
	filepath = resultsdir + 'results-Cj' + query + '-names.xlsx'
	bbh = pd.read_excel(filepath, sheet_name='BBH-eval-filter')
	bbh = bbh.loc[:, ['saccver', 'subject_gcf', 'organism_name', 'infraspecific_name', 'taxid', 'species_taxid']]
	psi = pd.read_excel(filepath, sheet_name='psiblast-eval-filter')
	psi = psi.loc[:, ['saccver', 'subject_gcf', 'organism_name', 'infraspecific_name', 'taxid', 'species_taxid']]
	df = bbh.append(psi, ignore_index=True)
	df.to_csv(query+'-protein-info.tsv', sep='\t', index=False)
	print('made ', query, ' csv')
	return df

def get_sequence(hit):
	handle = Entrez.efetch(db="protein", id=hit, rettype="fasta", retmode="text") # fetch the full sequence of that acc.ver
	record = SeqIO.read(handle, "fasta") # read it out
	handle.close()
	return record

def make_mfa(query):
	info = open_result(query)
	hits = [i for i in info['saccver']]
	print(len(hits))
	i = 0
	with open(query+'-protein.mfa', 'a+') as f:
		for hit in hits:
			seq = get_sequence(hit)
			i += 1
			print(i)
			SeqIO.write(seq, f, 'fasta')
	print('finished ', query)

make_mfa('PflA')
make_mfa('PflB')
