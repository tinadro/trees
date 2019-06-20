from os.path import dirname, abspath
from Bio import Entrez
import pandas as pd 
import sys, os
Entrez.email = 'td1515@ic.ac.uk'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OPEN THE NAME + GCF TABLE
#~~~~~~~~~~~~~~~~~~~~~~~~~~~

tree = sys.argv[1]
kind = ''.join(sys.argv[1].split('-')[3:])
acc = pd.read_csv('nodes-species_accession_'+kind+'.tsv', sep='\t')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PATH TO PARENT DIR OF ALL PROJECT FOLDERS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

parentdir = dirname(dirname(dirname(dirname(abspath(__file__)))))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SEARCH FOR THE GCF AND EXTRACT CORRESPONDING PROTEIN ACC.VER
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# extracts the subject_gcf numbers from the PflAB-BBH results tables
def xls_open(query): # query is PflA or PflB
	bbhresult = parentdir + '/3_bidirectional-best-hits/results-Cj' + query + '-names.xlsx' # path to results xlsx 
	xls = pd.ExcelFile(bbhresult) #
	sheets = xls.sheet_names
	dic = pd.read_excel(xls, header=0, sheet_name=None) # read the file into a dictionary, keys are worksheets and values are dataframes. None means all worksheets are imported 
	del dic[sheets[5]]
	del dic[sheets[4]]
	del dic[sheets[0]]
	del dic[sheets[2]]
	negs = pd.read_excel(parentdir+'/3_bidirectional-best-hits/results-Cj' + query + '-negative.xlsx', header=0)
	dic['negatives'] = negs
	dic['BBH'] = dic.pop('BBH-eval-filter')
	dic['psiblast'] = dic.pop('psiblast-eval-filter')
	return dic
# list is 'BBH-eval-filter', 'psiblast-eval-filter', 'negs'


#make it one dataframe with one column-subject_gcf, and sheet name as the index
def make_xls_df(xls_dict):
	data = pd.Series()
	for key in xls_dict.keys(): # for every excel worksheet 
		for index, line in xls_dict[key].iterrows(): # for every excel worksheet (sheet names are in sheeta_pfla) 
			gcf = line['subject_gcf']
#			gcf = gcf.split('_')[-1]
#			gcf = gcf.split('.')[0]
			ind = key
			s = pd.Series(data=gcf, index=[ind])
			data = data.append(s)
	return data		


def master_function(query):
	d_pfla = xls_open(query) # open the results xlsx
	data_pfla = make_xls_df(d_pfla) # make the xlsx a series of gcf's, with workshet names as indices 

	results = pd.DataFrame(columns=['BBH', 'psiblast', 'negatives', 'absent'])
	for index, row in acc.iterrows(): # iterating row-by-row through all node names
		gcf = row['accession']
		gcf = gcf.split('.')[0] # get the gcf of node, remove the .ver number
		df = data_pfla[data_pfla.str.contains(gcf)] # get the data_pfla that has the same GCF_xxxx
		if df.empty:
			results.loc[index, 'absent'] = 500 # if the gcf is not in the hits, write in the 'absent' column
		else:
			for ind, val in df.iteritems():
				results.loc[index, ind] = 1	# otherwise, write a '1' in the column that corresponds to the index of the gcf in data_pfla (the index tells u if its a bbh/psiblast/negative)
	results = results.fillna(0) # fill the NaN's as zeroes
	return results

pfla = master_function('PflA')
final_a = pd.concat([acc, pfla], axis=1, sort=False) # concatenate the species_accession tsv and the counts we jsut created above ^
pflb = master_function('PflB')
final_b = pd.concat([acc, pflb], axis=1, sort=False)

with pd.ExcelWriter('nodes-bbh-count-'+kind+'.xlsx') as w:
	final_a.to_excel(w, sheet_name='PflA_nodes_bbhs')
	final_b.to_excel(w, sheet_name='PflB_nodes_bbhs')

			

