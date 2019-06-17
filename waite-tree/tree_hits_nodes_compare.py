from os.path import dirname, abspath
import pandas as pd 
import sys

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PATH TO PARENT DIR OF ALL PROJECT FOLDERS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

parentdir = dirname(dirname(dirname(abspath(__file__))))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OPEN THE NODES TABLE and NEGS TABLE
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

nodes = pd.read_csv('nodes-species_accession_taxid.tsv', sep='\t')
nodes = nodes.reindex(columns=nodes.columns.tolist() + ['BBH', 'psiblast', 'negatives', 'absent']) #add 3 columns to the species_accession table

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OPEN HITS AND NEGS TABLES. EXTRACT SPECIES_TAXID'S. COUNT WHERE THEY APPEARED
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#make a new dataframe containing only the BBH hits, psiblast hits, and negatives
def make_taxid_table(bbh, psi, negs):
	species_taxid = pd.DataFrame()
	species_taxid['BBH'] = bbh['species_taxid']
	species_taxid['psiblast'] = psi['species_taxid']
	species_taxid['negs'] = negs['species_taxid']
	return species_taxid
	
#take each txid that is in the waite tree, count how many times it occurs in BBH hits, psiblast hits, and negatives. 
def taxid_counter(nodes, taxid_df):
	for index, row in nodes.iterrows():
		tid = row['species_taxid']
		bbhcount = len(taxid_df.loc[taxid_df['BBH'] == tid])
		psicount = len(taxid_df.loc[taxid_df['psiblast'] == tid])
		negcount = len(taxid_df.loc[taxid_df['negs'] == tid])
		nodes.iloc[index, 4] = bbhcount
		nodes.iloc[index, 5] = psicount
		nodes.iloc[index, 6] = negcount
		if bbhcount + psicount + negcount == 0:
			nodes.iloc[index, 7] = '500'
	return nodes

def my_extras(negs, bbh, psi, nodes):
	extra = pd.DataFrame()
	txids = [i for i in nodes['species_taxid']]
	for txid in txids:  
		negs = negs.loc[negs['species_taxid'] != txid]
		bbh = bbh.loc[bbh['species_taxid'] != txid]
		psi = psi.loc[psi['species_taxid'] != txid]
	return negs, bbh, psi



def master_function(query):
	results_xls = parentdir + '/3_bidirectional-best-hits/gcf_and_species_names_' + query + '.xlsx'
	d_hits = pd.read_excel(results_xls, sheet_name=None) # open the results xlsx
	negs_path = parentdir + '/3_bidirectional-best-hits/results-Cj' + query + '-negative.xlsx'

	negs_df = pd.read_excel(negs_path) # open the negs xlsx
	bbh_df = d_hits['BBH-eval-filter']
	psi_df = d_hits['psiblast-eval-filter']

	taxid_df = make_taxid_table(bbh_df, psi_df, negs_df) # make a table of taxid's of the BBH hits, psiblast hits, and negatives
	taxid_df = taxid_df.fillna(0.0).astype(int) # change the numbers from floats to integers 

	nodes_with_counts = taxid_counter(nodes, taxid_df) # count how many times each taxid was found and where 
	missing_species = nodes_with_counts.loc[nodes_with_counts['absent'] == '500'] # make second df of only species that i was missing

	print(nodes.head())
	print(nodes_with_counts.head())
	extra_negs, extra_bbh, extra_psi = my_extras(negs_df, bbh_df, psi_df, nodes)
	
	return nodes_with_counts, missing_species, extra_negs, extra_bbh, extra_psi

counts_pfla, missing_pfla, pfla_negs, pfla_bbh, pfla_psi = master_function('PflA')
counts_pflb, missing_pflb, pflb_negs, pflb_bbh, pflb_psi = master_function('PflB')


if missing_pfla.equals(missing_pflb):
	with pd.ExcelWriter('tree-species-taxid-count.xlsx') as xl:
		counts_pfla.to_excel(xl, sheet_name='PflA_all_nodes_with_counts', index=False)
		counts_pflb.to_excel(xl, sheet_name='PflB_all_nodes_with_counts', index=False)
		missing_pfla.to_excel(xl, sheet_name='species_im_missing', index=False)
else:
	with pd.ExcelWriter('tree-nodes-taxid-count.xlsx') as xl:
		counts_pfla.to_excel(xl, sheet_name='PflA_all_nodes_with_counts', index=False)
		counts_pflb.to_excel(xl, sheet_name='PflB_all_nodes_with_counts', index=False)
		missing_pfla.to_excel(xl, sheet_name='PflA_species_im_missing', index=False)
		missing_pflb.to_excel(xl, sheet_name='PflB_species_im_missing', index=False)

with pd.ExcelWriter('db_species_not_in_tree.xlsx') as xl:
	pfla_bbh.to_excel(xl, sheet_name='PflA-bbh', index=False)
	pfla_psi.to_excel(xl, sheet_name='PflA-psi', index=False)
	pfla_negs.to_excel(xl, sheet_name='PflA-negs', index=False)
	pflb_bbh.to_excel(xl, sheet_name='PflB-bbh', index=False)
	pflb_psi.to_excel(xl, sheet_name='PflB-psi', index=False)
	pflb_negs.to_excel(xl, sheet_name='PflB-negs', index=False)

