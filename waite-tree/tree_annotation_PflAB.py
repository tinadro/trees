from os.path import dirname, abspath
import pandas as pd 
import sys

#~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OPEN THE NAME + ACC TABLE
#~~~~~~~~~~~~~~~~~~~~~~~~~~~

df = pd.read_csv('species_accession.csv')
acc = df['accession']
for a in acc:
	print(a)

#~~~~~~~~~~~~~~~~~~~~~~~~~~
# GET PATH TO RESULTS XLSX
#~~~~~~~~~~~~~~~~~~~~~~~~~~

parentdir = dirname(dirname(dirname(abspath(__file__))))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# SEARCH FOR THE GCF AND EXTRACT CORRESPONDING PROTEIN ACC.VER
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#extracts the subject_gcf numbers from the PflAB-BBH results tables
def xls_cleanup(query): # query is PflA or PflB
	bbhresult = parentdir + '/1_bidirectional-best-hits/results-Cj' + query + '.xlsx' # path to results xlsx 
	xls = pd.ExcelFile(bbhresult) #
	sheets = xls.sheet_names
	dic = pd.read_excel(xls, sheet_name=None) # read the file into a dictionary, keys are worksheets and values are dataframes. None means all worksheets are imported 
	for sheet, df in dic.items():
		df = df.loc[:, ['saccver', 'subject_gcf']] #keep only the saccvver and gcf columns
		dic[sheet] = df # save that df as that sheet
	return dic
	return sheets
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
	record = Entrez.read((handle)
	return record

d_pfla, sheets = xls_cleanup('PflA')
print(sheets)


# iterate over each gcf 

# open the results-PflX.xlsx file

# search for that gcf

# note what worksheet it is from 

# translate that to 1 or -1, or 0 if it's not found? (be careful, the gcf might not even be in my database -- must check!)

# save the results in a new 
