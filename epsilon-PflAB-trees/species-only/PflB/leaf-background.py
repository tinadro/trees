from Bio import Phylo
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


tree = Phylo.read(sys.argv[1], 'newick') # open the tree file 
names = lookup_by_names(tree) # use the function to get the dictionary
nm = [i for i in names]

results = pd.DataFrame(columns=['node', 'label', 'color'])

for node in nm:
	genus = node.split('_')[0]
	if genus == 'Arcobacter':
		color = '#d5f5e3'
	elif genus == 'Campylobacter':
		color = '#ffffcc'
	elif genus == 'Helicobacter':
		color = '#e8daef'
	elif genus == 'Sulfurospirillum':
		color = '#fde5e6'
	else: 
		color = '#ffffff'
	label = 'label'
	line = pd.Series({'node': node, 'label': label, 'color': color})
	results = results.append(line, ignore_index=True)

n = ''.join(sys.argv[1].split('-')[-1])
query = sys.argv[1].split('-')[0]
results.to_csv('node_rename_'+query+'-'+n+'.csv', header=False, index=False)