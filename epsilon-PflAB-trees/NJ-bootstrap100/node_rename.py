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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OPEN REF TABLE OF LOCUS TAGS AND GCF's
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#reference table of accession nrs and strain names

def get_reference_table(query):
	table = '../../'+query+'-protein-info.xlsx'
	ref = pd.read_excel(table, sheet_name='non-redundant-hits')
	return ref

#~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAKE THE NODE,LABEL TABLE
#~~~~~~~~~~~~~~~~~~~~~~~~~~~

def node_label_table(nodes):
	i = 0
	results = pd.DataFrame(columns=['node', 'label'])

	for node in nodes:
		print(node)
		row = ref.loc[ref['saccver'].str.contains(node)] # get the row, for which the node is a substring in the saccver column 
		org_name = row['organism_name'].to_string() # get the organism name 
		org_name = org_name.lstrip('0123456789.- ')
		print(org_name)
		gcf = row['subject_gcf'].to_string()
		gcf = gcf.lstrip('0123456789.- ')
		label = org_name + ' ' + gcf # make the label by concatenating the organism name and gcf
		label = label.replace(' ', '_')
		line = pd.Series({'node': node, 'label': label}) 
		results = results.append(line, ignore_index=True)
		i += 1
		print(i)

	return results
tree = Phylo.read(sys.argv[1], 'newick') # open the tree file 
names = lookup_by_names(tree) # use the function to get the dictionary
nm = [i for i in names]
#print(nm)
#print(len(nm))

query = sys.argv[1].split('-')[0]
#print(query)

ref = get_reference_table(query)
print(ref.head())

results = node_label_table(nm)
print(results.head(10))
print(len(results))


n = ''.join(sys.argv[1].split('-')[-1])
results.to_csv('node_rename_'+query+'-'+n+'.csv', header=False, index=False)




