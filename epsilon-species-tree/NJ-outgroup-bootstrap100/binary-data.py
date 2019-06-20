from Bio import Phylo
import pandas as pd 
import numpy as np
import sys

# Node name | PflA | PflB | no full genome 

#~~~~~~~~~~~
# OPEN DATA
#~~~~~~~~~~~

kind = ''.join(sys.argv[1].split('-')[3:])

pfla = pd.read_excel('nodes-bbh-count-'+kind+'.xlsx', sheet_name='PflA_nodes_bbhs')
pfla = pfla.loc[:, ['accession', 'BBH', 'psiblast', 'negatives', 'absent']]
pflb = pd.read_excel('nodes-bbh-count-'+kind+'.xlsx', sheet_name='PflB_nodes_bbhs')
pflb = pflb.loc[:, ['accession', 'BBH', 'psiblast', 'negatives', 'absent']]
print('opened pfla+pflb .xlsx sheets')


# writes a new column, saying which column has the greatest value in each row
def max_col(df):
	df_nr = df.iloc[:, 1:]
	df['max'] = df_nr.idxmax(axis=1)
	return df

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# GET A DF OF NODES AND COUNTS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#def lookup_by_names(tree, df):
#	names = {}
#	for clade in tree.find_clades():
#		if clade.name:
#			if clade.name in names:
#				raise ValueError("Duplicate key: %s" % clade.name)
#			names[clade.name] = clade
#	for node in names.keys():
#		for ind, val in df.iterrows():
#			print(val[0])
#			if val[0] in node:
#				df.iloc[ind, 0] = node
#	return df   ~~~~~~~~~~~~ dict version

# makes a data frame where first column are node names, other columns are bbh, psi, and negatives count
def lookup_by_names(tree, df):
    names = []
    for clade in tree.find_clades():
        if clade.name:
            if clade.name in names:
                raise ValueError("Duplicate key: %s" % clade.name)
            names.append(clade.name)
    names = [i for i in names if 'ROOT' not in i]

    for node in names:
        for ind, val in df['accession'].iteritems():
            if val in node:
                df.iloc[ind, 0] = node
    return df 

tree = Phylo.read(sys.argv[1], 'newick') # open the tree file 
pfla = lookup_by_names(tree, pfla) # use the function to get the dictionary
pflb = lookup_by_names(tree, pflb)

# make a column of which results column has most species in it
pfla = max_col(pfla)
pflb = max_col(pflb)

def binary_prot(df):
	df2 = df.iloc[:, :2]  
	df2 = df2.reindex(columns=['accession', 'binary', 'binary2'])
	df2.iloc[:, 1:] = np.nan
	print(df2.head())
	for ind, val in df['max'].iteritems():
		if val == 'BBH':
			df2.iloc[ind, 1] = 1
		elif val == 'psiblast':
			df2.iloc[ind, 1] = 0
		else:
			df2.iloc[ind, 1] = -1
	for ind, val in df['max'].iteritems():
		if val == 'negatives':
			df2.iloc[ind, 2] = 1
		else:
			df2.iloc[ind, 2] = -1
	return df2
	
pfla_bin = binary_prot(pfla) # binary column for PflA
pflb_bin = binary_prot(pflb) # binary coumn for PflB

absent = pfla.iloc[:, :1]
absent = absent.reindex(columns=['accession', 'binary']) # binary column for species with no full genome available
absent['binary'] = np.nan
for ind, val in pfla['max'].iteritems():
	if val == 'absent':
		absent.iloc[ind, 1] = 1
	else:
		absent.iloc[ind, 1] = -1


# data frame that will be the final results table 
df = pd.DataFrame(columns=['nodes', 'PflA', 'PflB', 'no_PflA_found', 'no_PflB_found', 'no_full_genome'])
df['nodes'] = pfla['accession']
df['PflA'] = pfla_bin['binary']
df['PflB'] = pflb_bin['binary']
df['no_PflA_found'] = pfla_bin['binary2']
df['no_PflB_found'] = pflb_bin['binary2']
df['no_full_genome'] = absent['binary']

df.PflA = df.PflA.astype(int) # change the numbers from floats to integers 
df.PflB = df.PflB.astype(int) 
df.no_PflA_found = df.no_PflA_found.astype(int)
df.no_PflB_found = df.no_PflB_found.astype(int) 
df.no_full_genome = df.no_full_genome.astype(int)

print(df.head())

df.to_csv('binary-annotation-'+kind+'.csv', header=False, index=False)




