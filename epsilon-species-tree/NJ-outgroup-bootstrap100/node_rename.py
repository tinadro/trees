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
print(nm[-1])

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OPEN REF TABLE OF LOCUS TAGS AND GCF's
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#reference table of accession nrs and strain names
parentdir = dirname(dirname(abspath(__file__)))
table = parentdir+'/genbank-16s-info.tsv'

ref = pd.read_csv(table, sep='\t')
ref = ref.drop(columns=['description', 'gene_name', 'accver', 'gene_location'])
ref = ref.iloc[:, [1, 0, 2, 3, 4, 5]]
ref.drop(index=[8], inplace=True) #remove the hydrogenimonas sp. line, has no annotated 16s rRNA, and blast couldn't find one either

#~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MAKE THE NODE,LABEL TABLE
#~~~~~~~~~~~~~~~~~~~~~~~~~~~

i = 0
results = pd.DataFrame(columns=['node', 'label'])

for node in nm:
	row = ref.loc[ref['locus_tag'].str.contains(node)]
	row  = row.drop_duplicates(subset=['gcf'])
	try:
		row = row.iloc[0]
		org_name = row['organism_name']
		if 'porcin' in org_name:
			org_name = 'Arcobacter_porcinus'
		label = org_name + ' ' + row['gcf']
		label = label.replace(' ', '_')
		line = pd.Series({'node': node, 'label': label})
		results = results.append(line, ignore_index=True)
	except IndexError:
		pass
	i += 1
	print(i)

print(results.head(10))
print(len(results))


n = ''.join(sys.argv[1].split('-')[3:])
results.to_csv('node_rename_'+n+'.csv', header=False, index=False)




