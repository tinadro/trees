import glob, os
import pandas as pd 
from os.path import dirname, abspath


parentdir = dirname(dirname(dirname(abspath(__file__))))
table = parentdir + '/3_bidirectional-best-hits/e-proteobacteria_for_BBH.tsv'
dbpath = parentdir + '/datalocal/e-proteobacteria-genomes-gbff/*.gbff'

df = pd.read_csv(table, sep='\t')
gcf_ls = [i[4:] for i in df['subject_gcf']] # list of gcf numbers I used 

paths = []
for f in glob.glob(dbpath):
	paths.append(f)
print(paths[:5])


dbs = [] # list of gbff files 
for f in glob.glob(dbpath):
	db = f.split('/')[-1]
	ele = '_'.join(db.split('_', 2)[:2])
	dbs.append(ele[4:])


print(len(gcf_ls))
print(len(dbs))


# check if all gcf's are in the gbff db
#for gcf in gcf_ls:
#	if any(gcf in p for p in dbs) == False:
#		print(gcf, ' is not in gbff')
		# the one this spits out i have in GCA for gbff, and GCF for the bbh 

extras = []
i = 0
for db in dbs:
	if db not in gcf_ls:
		extras.append(db)

for extra in extras:
	for path in paths:
		if extra in path:
			os.remove(path)
			i += 1
			print(i)

# check if there are extra gbff db



#'e-proteobacteria-genomes-gbff/ncbi-genomes-2019-06-13/*.gbff'
