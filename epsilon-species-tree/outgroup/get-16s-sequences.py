from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import pandas as pd
from os.path import dirname, abspath
import glob

parentdir = dirname(dirname(dirname(abspath(__file__))))

gbff = pd.read_csv('16s-info.tsv', sep='\t') # genbank info table

# clean up the DF to only have one 16s gene per genome
gbff_clean = gbff.drop_duplicates(subset=['gcf', 'description'])
print(gbff_clean.head())

#get the 16s sequence and append to a fasta file

with open('16s-sequences.mfa', 'a+') as result:
	for ind, row in gbff_clean.iterrows():
		f = glob.glob(row['gcf']+'*.gbff') # get path of each gcff file, line-by-line
		loc = row['gene_location']# get locus tag 
		for record in SeqIO.parse(f[0], 'genbank'):
			if 'plasmid' in record.description or 'conjugative element' in record.description: # ignore the records for plasmids/ conjugative elements (only leaves the genome/ chromosome sequences)
				pass
			else:
				for feature in record.features:
					if feature.type == 'rRNA' and loc == str(feature.location):
						sequence = feature.extract(record.seq)
						info = row['organism_name'] + ' ' + 'species_taxid: ' + str(row['species_taxid']) + ' | ' + row['gcf']
						rec = SeqRecord(sequence, id=row['locus_tag'], name=row['gene_name'], description=info)
						SeqIO.write(rec, result, 'fasta')
						print('wrote sequence for', row['organism_name'])

