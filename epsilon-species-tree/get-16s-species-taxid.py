import pandas as pd
from Bio import Entrez
Entrez.email = 'td1515@ic.ac.uk'
Entrez.api_key = '41267f8592172caaa22ab00ec006c4330208'

key_refseq = pd.read_csv('~/datalocal/bacteria_assembly_summary_refseq_minimal.tsv', sep='\t')
key_genbank = pd.read_csv('~/datalocal/bacteria_assembly_summary_genbank_minimal.tsv', sep='\t')




base = pd.read_csv('genbank-16s-info.tsv', sep='\t')
gcf = base['gcf'].to_dict()

df = pd.DataFrame()

for key in gcf.keys():
	print(key)
#	print(gcf[key])
	if 'GCF' in gcf[key]:
		hit = key_refseq.loc[key_refseq['assembly_accession'] == gcf[key]]
		if hit.empty:
			hit = key_genbank.loc[key_genbank['gbrs_paired_asm'] == gcf[key]]
			if hit.empty:
				print(gcf[key])
	elif 'GCA' in gcf[key]:
		hit = key_genbank.loc[key_genbank['assembly_accession'] == gcf[key]]
		if hit.empty:
			hit = key_refseq.loc[key_refseq['gbrs_paired_asm'] == gcf[key]]
			if hit.empty:
				print(gcf[key])
	hit = hit.loc[:, ['organism_name', 'infraspecific_name', 'taxid', 'species_taxid']]
	print(hit)
	df = df.append(hit, ignore_index=True)

result = pd.concat([base, df], axis=1, sort=False)

print(result.head())

result.to_csv('genbank-16s-info.tsv', sep='\t', index=None)
