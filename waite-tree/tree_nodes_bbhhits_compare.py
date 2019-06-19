from os.path import dirname, abspath
from Bio import Entrez
import pandas as pd 
import sys
Entrez.email = 'td1515@ic.ac.uk'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OPEN THE NAME + ACC TABLE
#~~~~~~~~~~~~~~~~~~~~~~~~~~~

acc = pd.read_csv('species_accession.csv')

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# PATH TO PARENT DIR OF ALL PROJECT FOLDERS
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

parentdir = dirname(dirname(dirname(abspath(__file__))))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SEARCH FOR THE GCF AND EXTRACT CORRESPONDING PROTEIN ACC.VER
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# extracts the subject_gcf numbers from the PflAB-BBH results tables
def xls_open(query): # query is PflA or PflB
	bbhresult = parentdir + '/1_bidirectional-best-hits/results-Cj' + query + '.xlsx' # path to results xlsx 
	xls = pd.ExcelFile(bbhresult) #
	sheets = xls.sheet_names
	dic = pd.read_excel(xls, header=0, sheet_name=None) # read the file into a dictionary, keys are worksheets and values are dataframes. None means all worksheets are imported 
	del dic[sheets[0]]
	del dic[sheets[2]]
	del sheets[0]
	del sheets[1]
	return sheets, dic
# list is 'BBH-eval-filter', 'psiblast-eval-filter', 'reidentified-psiblast', 'novel-psiblast'


#make it one dataframe with one column-subject_gcf, and sheet name as the index
def make_xls_df(sheetnames, xls_dict):
	data = pd.Series()
	for item in sheetnames: # for every excel worksheet 
		for index, line in xls_dict[item].iterrows(): # for every excel worksheet (sheet names are in sheeta_pfla) 
			gcf = line['subject_gcf']
			ind = item
			s = pd.Series(data=gcf, index=[ind])
			data = data.append(s)
	return data		

# find the entrez id associated with input accession number
def get_entrez_id(accession):
	handle = Entrez.esearch(db='assembly', term=accession)
	record = Entrez.read(handle)
	ids = record['IdList']
	return ids

#fetch summary of the assembly identified with the id, return the uba, gca, and gcf numbers.
def get_assembly_summary(ids):
	handle = Entrez.esummary(db='assembly', id=ids, report='full')
	record = Entrez.read(handle)
	summary = record['DocumentSummarySet']['DocumentSummary'][0]
	uba = summary['Biosource']['Isolate']
	gca = summary['Synonym']['Genbank']
	gcf = summary['Synonym']['RefSeq']
	return uba, gca, gcf

sheets_pfla, d_pfla = xls_open('PflA') # open the results xlsx
data_pfla = make_xls_df(sheets_pfla, d_pfla) # make the xlsx a series of gcf's, with workshet names as indices 

# for gcf in acc, put it through the get_entrez and get_assembly functions- output the gcf. 
# search for that gcf in data_pfla. if it's there, store the index of the hit. if it's not, save the acc code


acc_found = pd.DataFrame()
acc_missing = pd.DataFrame(columns=['species', 'accession'])

def run_entrez_gcf_check(accession, ind):
	ids = get_entrez_id(accession)
	uba, gca, gcf = get_assembly_summary(ids)
	if not gcf:
		row = list(acc.loc[ind])
		return row
	else: 
		df = data_pfla.str.find(gcf)
		return df


for index, value in acc['accession'].iteritems():
	line = run_entrez_gcf_check(value, index)
	print(line)


d_pflb, sheets_pflb = xls_open('PflB')


# iterate over each gcf 

# open the results-PflX.xlsx file

# search for that gcf

# note what worksheet it is from 

# translate that to 1 or -1, or 0 if it's not found? (be careful, the gcf might not even be in my database -- must check!)

# save the results in a new 
