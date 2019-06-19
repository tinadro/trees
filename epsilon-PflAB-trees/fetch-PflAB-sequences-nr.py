import pandas as pd 
from Bio import SeqIO, Entrez
Entrez.email = 'td1515@ic.ac.uk'
Entrez.api_key = '41267f8592172caaa22ab00ec006c4330208'

#open info table

def info_table(query):
	info_df = pd.read_csv(query + '-protein-info.tsv', sep='\t')
	info_nr = info_df.drop_duplicates(subset=['saccver'])
	deleted = info_df.loc[(~info_df.subject_gcf.isin(info_nr.subject_gcf))]
	print(query+':')
	print('all hits: ', len(info_df))
	print('nr hits: ', len(info_nr))
	print('deleted hits: ', len(deleted))
	with pd.ExcelWriter(query+'-protein-info.xlsx') as xl:
		info_df.to_excel(xl, sheet_name='all-hits')
		info_nr.to_excel(xl, sheet_name='non-redundant-hits')
		deleted.to_excel(xl, sheet_name='redundant-hits')
	return info_nr

def get_sequence(hit):
	handle = Entrez.efetch(db="protein", id=hit, rettype="fasta", retmode="text") # fetch the full sequence of that acc.ver
	record = SeqIO.read(handle, "fasta") # read it out
	handle.close()
	return record

def make_mfa(query):
	nr_df = info_table(query)
	hits = [i for i in nr_df['saccver']]
	i = 0
	with open(query+'-protein-nr.mfa', 'a+') as f:
		for hit in hits:
			seq = get_sequence(hit)
			i += 1
			print(i)
			SeqIO.write(seq, f, 'fasta')
	print('finished getting nr ', query, ' sequences')


make_mfa('PflA')
make_mfa('PflB')
