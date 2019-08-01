from Bio import Phylo, SeqIO
from os.path import dirname, abspath
import pandas as pd
import sys

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

tree = Phylo.read('16s-aligned.phy_phyml_tree.txt', 'newick') # open the tree file 
names = lookup_by_names(tree) # use the function to get the dictionary

nm = [i for i in names]
#print(nm)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAKE THE NODE,LABEL TABLE
#~~~~~~~~~~~~~~~~~~~~~~~~~~~

i = 0
results = pd.DataFrame(columns=['node', 'label'])

for record in SeqIO.parse('16s-epsilon-outgroup-unique-species.mfa', 'fasta'):
	species = record.id
	name = record.description.split(' ')[1:-4]
	name = '_'.join(name)
	for node in nm:
		if node in species:
			line = pd.Series({'node': node, 'label': name})
			results = results.append(line, ignore_index=True)
	i += 1
	print(i)

print(results.head(10))
print(len(results))


results.to_csv('node_rename_to_species.csv', header=False, index=False)




