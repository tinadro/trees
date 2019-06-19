from Bio import Phylo, Entrez
from os.path import dirname, abspath
import csv, os, sys
import pandas as pd
import numpy as np
Entrez.email = 'td1515@ic.ac.uk'

#~~~~~~~~~~~~~~~~~~~~~
# GET A LIST OF NODES
#~~~~~~~~~~~~~~~~~~~~~

# define a function that makes a dictionary, node names are the heys
def lookup_by_names(tree):
    names = {}
    for clade in tree.find_clades():
        if clade.name:
            if clade.name in names:
                raise ValueError("Duplicate key: %s" % clade.name)
            names[clade.name] = clade
    return names # spits out a dictionary where the keys are the node names, values are Clade(branch_length=value, name=same as key)

tree = Phylo.read(sys.argv[1], 'newick') # open the tree file 
names = lookup_by_names(tree) # use the function to get the dictionary

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SAVE SPECIES NAMES AND ASSEMBLY ACCESSIONS IN A TABLE
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

table = 'nodes-species_accession.tsv' # filename of the table

#if the table already exists, delete it. we wanna write a new one not append to the incorrect one
file_exists = os.path.isfile(table)
if file_exists:
	os.remove(table)

with open(table, 'w+') as acc: # make and open the table file
	write = csv.writer(acc, delimiter='\t')
	write.writerow(['species', 'accession']) # put in the headers
	for node in names:
		if node.find('GCF_') != -1 or node.find('GCA_') != -1: #if gcf/gca is provided
			species = ' '.join(node.split('_')[:-2])
			gcf = '_'.join(node.split('_')[-2:])
			ls = [species, gcf] # split the name from the accession and save them as a list 
		else: # if uba is provided
			species = ' '.join(node.split('_', 2)[:-1])
			uba = ''.join(node.split('_', 2)[-1])
			ls = [species, uba] # split the name from the accession and save them as a list 
		write.writerow(ls) # write the list as a line in the csv
print('wrote the species+accession table')

#~~~~~~~~~~~~~~~~~~~~~~~~~
# REOPEN FILE, ADD TAXID  
#~~~~~~~~~~~~~~~~~~~~~~~~~

parentdir = dirname(dirname(dirname(dirname(abspath(__file__)))))
ref = parentdir + '/datalocal/bacteria_assembly_summary_refseq_minimal.tsv'
gen = parentdir + '/datalocal/bacteria_assembly_summary_genbank_minimal.tsv'

df = pd.read_csv(table, sep='\t')
refseq = pd.read_csv(ref, sep='\t')
genbank = pd.read_csv(gen, sep='\t')
df = df.reindex(columns=df.columns.tolist() + ['taxid', 'species_taxid']) #add two columns to the species_accession table

#define function to fetch taxid from entrez if UBA is provided:
def get_entrez_id(accession):
	handle = Entrez.esearch(db='assembly', term=accession)
	record = Entrez.read(handle)
	ids = record['IdList']
	return ids

#fetch summary of the assembly identified with the id, return the uba, gca, and gcf numbers.
def fetch_taxid(ids):
	handle = Entrez.esummary(db='assembly', id=ids, report='full')
	record = Entrez.read(handle, validate=False)
	summary = record['DocumentSummarySet']['DocumentSummary'][0]
	taxid = summary['Taxid']
	species_taxid = summary['SpeciesTaxid']
	return taxid, species_taxid


def find_taxid(nodes_df):
	for index, gcf in nodes_df['accession'].iteritems():
		if gcf.find('GCF_') != -1: # if the accession is gcf
			hit = refseq.loc[refseq['assembly_accession'] == gcf] #look for it in refseq
			if hit.empty: #if its not in refseq, find it in genbank
				hit = genbank.loc[genbank['gbrs_paired_asm'] == gcf]
			col1 = list(hit['taxid']) #extract the taxid and species taxid
			col2 = list(hit['species_taxid']) 
			if len(col1) != 1 or len(col2) != 1: #these two rows check for if you get more than one hit, it tells you what gcf caused this. 
				print(gcf)
			nodes_df.iloc[index, [2]] = col1 #append the two fields to the nodes_ data frame
			nodes_df.iloc[index, [3]] = col2
		elif gcf.find('GCA_') != -1: #same thing for if the assembly accession is gca. but the assembly_accession and gbrs_paired_asm columns are flipped
			hit = refseq.loc[refseq['gbrs_paired_asm'] == gcf]
			if hit.empty:
				hit = genbank.loc[genbank['assembly_accession'] == gcf]
			col1 = list(hit['taxid'])
			col2 = list(hit['species_taxid'])
			if len(col1) != 1 or len(col2) != 1:
				print(gcf)
			nodes_df.iloc[index, [2]] = col1 #append the two fields to the nodes_ data frame
			nodes_df.iloc[index, [3]] = col2
		else:
			entrez_id = get_entrez_id(gcf)
			tax, sp_tax = fetch_taxid(entrez_id)
			nodes_df.iloc[index, [2]] = tax #append the two fields to the nodes_ data frame
			nodes_df.iloc[index, [3]] = sp_tax
	return nodes_df

result = find_taxid(df)
result[['taxid', 'species_taxid']] = result[['taxid', 'species_taxid']].fillna(0.0).astype(int) # change the numbers from floats to integers 

result.to_csv('nodes-species_accession_taxid.tsv', sep='\t', index=False) #save as a table
print('wrote the species+accession+taxid table')
