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
    names = []
    for clade in tree.find_clades():
        if clade.name:
            if clade.name in names:
                raise ValueError("Duplicate key: %s" % clade.name)
            names.append(clade.name)
    return names # spits out a list of node names 

tree = Phylo.read(sys.argv[1], 'newick') # open the tree file 
names = lookup_by_names(tree) # use the function to get the dictionary

names = [i for i in names if 'ROOT' not in i]

for ele in names:
	if 'porcin' in ele:
		print(ele)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SAVE SPECIES NAMES AND ASSEMBLY ACCESSIONS IN A TABLE
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
tree_kind = ''.join(sys.argv[1].split('-')[3:])
table = 'nodes-species_accession_'+tree_kind+'.tsv' # filename of the table

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

