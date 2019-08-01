import pandas as pd 

all_sp = pd.read_csv('PflAB-results.csv', header=None)
current_sp = pd.read_csv('core-proteins-accessions.tsv', sep='\t')

#print(all_sp.head())
#print(current_sp.head())

all_sp = [i for i in all_sp[0]]
currrent_sp = [i for i in current_sp['species']]

for ele1 in all_sp:
	if ele1 not in current_sp:
		print(ele1)
