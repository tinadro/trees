from Bio import SeqIO
from os.path import dirname, abspath
import sys 
import pandas as pd

parentdir = dirname(dirname(dirname(abspath(__file__))))
filepath = parentdir + '/datalocal/e-proteobacteria-genomes-gbff/'


gcf = []
description = []
gene_name = []
accver = []
location = []
locus_tag = []

for record in SeqIO.parse(filepath+'GCA_000310245.1_ASM31024v1_genomic.gbff', 'genbank'):
	print(record.description)




#assembly = '_'.join(sys.argv[1].split('_', 2)[:2])
print(len(record.features))

for val in record.features:
	if 'rRNA' in val.type:
		if '16S' in val.qualifiers['product'][0]:
			print(val)
#			gcf.append(assembly)
#			description.append(record.description)
#			gene_name.append(val.qualifiers['product'][0])
#			accver.append(record.id)
#			location.append(str(val.location))
#			locus_tag.append(val.qualifiers['locus_tag'][0])

#d = {'gcf': gcf, 'description': description, 'gene_name': gene_name, 'accver': accver, 'gene_location': location, 'locus_tag': locus_tag}


#print(sys.argv[1])
#for key in d.keys():
#	print(key, d[key])

#df = pd.DataFrame(d, index=False)

#with open(parentdir+'/4_trees/epsilon-species-tree/genbank-16s-info.tsv', 'a+') as f:
#	df.to_csv(f, sep='\t', index=False)
