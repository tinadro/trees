from os.path import dirname, abspath
import pandas as pd 
import sys

#~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OPEN THE NAME + ACC TABLE
#~~~~~~~~~~~~~~~~~~~~~~~~~~~

df = pd.read_csv('species_accession.csv')
acc = df['accession']

#~~~~~~~~~~~~~~~~~~~~~~~~~~
# GET PATH TO RESULTS XLSX
#~~~~~~~~~~~~~~~~~~~~~~~~~~

parentdir = dirname(dirname(dirname(abspath(__file__))))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SEARCH FOR THE GCF AND EXTRACT CORRESPONDING PROTEIN ACC.VER
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#extracts the subject_gcf numbers from the PflAB-BBH results tables
def xls_open(query): # query is PflA or PflB
	bbhresult = parentdir + '/1_bidirectional-best-hits/results-Cj' + query + '.xlsx' # path to results xlsx 
	xls = pd.ExcelFile(bbhresult) #
	sheets = xls.sheet_names
	dic = pd.read_excel(xls, header=0, sheet_name=None) # read the file into a dictionary, keys are worksheets and values are dataframes. None means all worksheets are imported 
	del dic[sheets[0]]
	del dic[sheets[2]]
	del sheets[0]
	del sheets[1]
	return dic, sheets
# list is 'BBHs', 'BBH-eval-filter', 'psiblast', 'psiblast-eval-filter', 'reidentified-psiblast', 'novel-psiblast'

# find the entrez id associated with input accession number
def get_entrez_id(accession):
	ids = []
	handle = Entrez.esearch(db='assembly', term=accession)
	record = Entrez.read(handle)
	ids.append(record['IdList'])
	return ids

#fetch raw summary of the assembly identified with the id
def raw_assembly_summary(as_id):
	handle = Entrez.esummary(db='assembly', id=as_id, report='full')
	record = Entrez.read(handle)
	return record

d_pfla, sheets_pfla = xls_open('PflA')

for item in sheets_pfla:
	for index, line in d_pfla[item].iterrows():
		gcf = line['subject_gcf']
		ent_ids = get_entrez_id(gcf)
		summary = raw_assembly_summary(ent_ids)




d_pflb, sheets_pflb = xls_open('PflB')


# iterate over each gcf 

# open the results-PflX.xlsx file

# search for that gcf

# note what worksheet it is from 

# translate that to 1 or -1, or 0 if it's not found? (be careful, the gcf might not even be in my database -- must check!)

# save the results in a new 
