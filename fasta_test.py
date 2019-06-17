from Bio import SeqIO, Entrez
import sys
import pandas as pd
Entrez.email = 'td1515@ic.ac.uk'
Entrez.api_key = '41267f8592172caaa22ab00ec006c4330208'

def get_entrez_id(accession):
	handle = Entrez.esearch(db='nuccore', term=accession, retmax='100000')
	record = Entrez.read(handle)
	handle.close()
	uid = record['IdList']
	return uid

def get_summary(ids):
	handle = Entrez.esummary(db='nuccore', id=ids, report='full')
	record = Entrez.read(handle, validate=False)
	handle.close()
	return record [0]


def fasta_to_idtable(filename):
	fa_id = []
	gi = []
	txid = []
	title = []
	i = 0

	# get the nuccore locus numbers from the big fasta file.
	for record in SeqIO.parse(filename, 'fasta'):
		fid = record.id.split('.')[0]
		fa_id.append(fid)
	print('got all IDs, fetching them with entrez')
	
	interval = list(range(0, 32000, 500))
	
	for ind, val in enumerate(interval):
		a = val 
		try:
			b = interval[ind+1]
		except IndexError:
			b = ''
		fa_section = fa_id[a:b]
		#for each id, get the GI, taxid, and 'species' title
		for ele in fa_section:
			uid = get_entrez_id(ele)
			rec = get_summary(uid)
			i += 1
			print(i)
			gi.append(rec['Gi'])
			txid.append(rec['TaxId'])
			title.append(rec['Title'])

		d = {'title': title, 'fasta_id': fa_section, 'taxid': txid, 'gi': gi} # make dictionary of fetched data
			
		df = pd.DataFrame(dict([ (k, pd.Series(v)) for k,v in d.items() ])) # make df from the dictionary
		print('made df, to ', b)
		with open('silva-campylobacteria-id-table.tsv', 'a') as f:
			df.to_csv(f, sep='\t', index=False)
		print('saved ', b, ' to csv')

#df1 = fasta_to_idtable('silva-desulfurellia-16s.fna')
#df1.to_csv('silva-desulfurellia-id-table.tsv', sep='\t', index=False)
fasta_to_idtable('silva-campylobacteria-16s.fna')
#df2.to_csv('silva-campylobacteria-id-table.tsv', sep='\t', index=False)

