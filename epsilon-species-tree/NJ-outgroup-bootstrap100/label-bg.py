#node name | 'label_background' | #color

from Bio import Phylo
import pandas as pd

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
    names = [i for i in names if 'porcinus' not in i ]
    names.append('Arcobacter_porcinus_GCF_004299785.1')
    names = names[1:]
    return names # spits out a dictionary where the keys are the node names, values are Clade(branch_length=value, name=same as key)

def node_label_table(nodes):
	i = 0
	results = pd.DataFrame(columns=['node', 'type', 'hex_color'])
	
	for nm in names:
		if 'Helicobacter_pylori' in nm:
			line = pd.Series({'node': nm, 'type': 'label_background', 'hex_color': '#dbc4e6'})
		elif 'Helicobacter' in nm:
			line = pd.Series({'node': nm, 'type': 'label_background', 'hex_color': '#e8daef'})
		elif 'Arcobacter' in nm:
			line = pd.Series({'node': nm, 'type': 'label_background', 'hex_color': '#d5f5e3'})
		elif 'Sulfurospirillum' in nm:
			line = pd.Series({'node': nm, 'type': 'label_background', 'hex_color': '#fde5e6'})
		elif 'Campylobacter_jejuni' in nm:
			line = pd.Series({'node': nm, 'type': 'label_background', 'hex_color': '#f8d799'})
		elif 'Campylobacter' in nm:
			line = pd.Series({'node': nm, 'type': 'label_background', 'hex_color': '#ffffcc'})
		else:
			line = pd.Series()
		results = results.append(line, ignore_index=True)
		i += 1
		print(i)
	return results

tree = Phylo.read('16s-epsilon-outgroup-consense100-r.tree', 'newick') # open the tree file 
names = lookup_by_names(tree) # use the function to get the dictionary
df = node_label_table(names)
df.to_csv('label-bg.csv', header=False, index=False)

#tree = Phylo.read('PflA-nr-consense-phyml-labels.tree', 'newick') # open the tree file 
#names = lookup_by_names(tree) # use the function to get the dictionary
#df = node_label_table(names)
#df.to_csv('label-bg-PflA.csv', header=False, index=False)
