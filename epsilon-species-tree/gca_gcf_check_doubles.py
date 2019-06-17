import pandas as pd
from os.path import dirname, abspath
import glob, os

parentdir = dirname(dirname(dirname(abspath(__file__))))
db = parentdir+'/datalocal/e-proteobacteria-genomes-gbff/'

gbff = pd.read_csv('genbank-16s-info.tsv', sep='\t') # genbank info table
gbff = gbff.drop_duplicates(subset=['gcf', 'description'])

gca = [i.split('_')[-1].split('.')[0] for i in gbff['gcf'] if 'GCA' in i]
gcf = [i.split('_')[-1].split('.')[0] for i in gbff['gcf'] if 'GCF' in i]

ls = set(gca) & set(gcf)
#print(ls)
#print(type(ls))

gca_del = ['GCA_'+i for i in ls]

filepath = [f for f in glob.glob(db+'*') for ele in gca_del if f.find(ele) != -1]

for path in filepath:
	os.remove(path)
