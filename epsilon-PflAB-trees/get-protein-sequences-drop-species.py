from Bio import SeqIO, Entrez
from Bio.SeqRecord import SeqRecord
import pandas as pd
from os.path import dirname, abspath
import glob
Entrez.email = 'td1515@ic.ac.uk'
Entrez.api_key = '41267f8592172caaa22ab00ec006c4330208'

def single_species(pfl):
	proteins = pd.read_excel(pfl+'-protein-info.xlsx', sheet=['all-hits']) # genbank info table
	proteins = proteins.sample(frac=1) # shuffle the rows randomly
	proteins_nr = proteins.drop_duplicates(subset=['species_taxid'])
	print(proteins_nr)

	i = 0 
	with open(pfl+'-sequences-species.mfa', 'a+') as result:
		for ind, accver in proteins_nr['saccver'].iteritems():
			i += 1
			handle = Entrez.efetch(db="protein", id=accver, rettype="fasta", retmode="text") # fetch the full sequence of that acc.ver
			record = SeqIO.read(handle, "fasta") # read it out
			handle.close()
			SeqIO.write(record, result, 'fasta')
			print(i)
		
single_species('PflA')
single_species('PflB')

# clean up the DF to only have one 16s gene per genome
#gbff_clean = gbff.drop_duplicates(subset=['species_taxid'])
#print(gbff_clean.head())
#print(len(gbff_clean))

#get the 16s sequence and append to a fasta file

#with open('16s-sequences-species.mfa', 'a+') as result:
#	for ind, row in gbff_clean.iterrows():
#		f = glob.glob(gbff_db+row['gcf']+'*.gbff') # get path of each gcff file, line-by-line
#		loc = row['gene_location']# get locus tag 
#		for record in SeqIO.parse(f[0], 'genbank'):
#			if 'plasmid' in record.description or 'conjugative element' in record.description: # ignore the records for plasmids/ conjugative elements (only leaves the genome/ chromosome sequences)
#				pass
#			else:
#				for feature in record.features:
#					if feature.type == 'rRNA' and loc == str(feature.location):
#						sequence = feature.extract(record.seq)
#						info = row['organism_name'] + ' ' + 'species_taxid: ' + str(row['species_taxid']) + ' | ' + row['gcf']
#						rec = SeqRecord(sequence, id=row['locus_tag'], name=row['gene_name'], description=info)
#						SeqIO.write(rec, result, 'fasta')
#						print('wrote sequence for', row['organism_name'])

