import pandas as pd
from Bio import SeqIO

nm = []
for record in SeqIO.parse('16s-outgroup-sequences.mfa', 'fasta'):
	nm.append(record.id[:10])


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OPEN REF TABLE OF LOCUS TAGS AND GCF's
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#reference table of accession nrs and strain names
table = '16s-info.tsv'

ref = pd.read_csv(table, sep='\t')
ref = ref.drop(columns=['description', 'gene_name', 'accver', 'gene_location'])
ref = ref.iloc[:, [1, 0, 2, 3, 4, 5]]
ref.drop(index=[8], inplace=True) #remove the hydrogenimonas sp. line, has no annotated 16s rRNA, and blast couldn't find one either

#~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAKE THE NODE,LABEL TABLE
#~~~~~~~~~~~~~~~~~~~~~~~~~~~

i = 0
results = pd.DataFrame(columns=['node', 'label'])

for node in nm:
	row = ref.loc[ref['locus_tag'].str.contains(node)]
	row.drop_duplicates(subset=['gcf'], inplace=True)
	try:
		row = row.iloc[0]
		label = row['organism_name'] + ' ' + row['gcf']
		label = label.replace(' ', '_')
		line = pd.Series({'node': node, 'label': label})
		results = results.append(line, ignore_index=True)
	except IndexError:
		pass
	i += 1
	print(i)

print(results.head(10))
print(len(results))

results.to_csv('node_rename_outgroups.csv', header=False, index=False)

