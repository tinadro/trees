from Bio import SeqIO
from os.path import dirname, abspath
import sys 
import pandas as pd
import numpy as np

gcf = []
description = []
gene_name = []
accver = []
location = []
locus_tag = []

gb_file = open(sys.argv[1], 'r') # open the genbank file
assembly = '_'.join(sys.argv[1].split('_', 2)[:2]) # get the gcf from the filename (some files have it in their info, but not all. so this way is more sure.)

for record in SeqIO.parse(gb_file, 'genbank'):
	if 'plasmid' in record.description or 'conjugative element' in record.description: # ignore the records for plasmids/ conjugative elements (only leaves the genome/ chromosome sequences)
		pass
	else:
		print(record.description)
		for val in record.features:
			if val.type == 'rRNA': # find the features that are rRNAs
				if '16S' in val.qualifiers['product'][0]: # find features that are 16S rRNA.  
					# get the different stats for each 16S rRNA entry
					gcf.append(assembly)
					description.append(record.description)
					gene_name.append(val.qualifiers['product'][0])
					accver.append(record.id)
					location.append(str(val.location))
					locus_tag.append(val.qualifiers['locus_tag'][0])

		if gcf == []: # if there's no 16S rRNA, save the gcf adn record it in the table. so i can look at it manually later. 
			d = {'gcf': assembly, 'description': record.description, 'gene_name': '', 'accver': record.id, 'gene_location': '', 'locus_tag': ''}
			df = pd.DataFrame(d, index=[0])
		else:
			d = {'gcf': gcf, 'description': description, 'gene_name': gene_name, 'accver': accver, 'gene_location': location, 'locus_tag': locus_tag}
			df = pd.DataFrame(d)
		print(df)
		with open('/project/home/td1515/4_trees/epsilon-species-tree/outgroup/16s-info.tsv', 'a+') as f:
			df.to_csv(f, sep='\t', index=False, header=False)

