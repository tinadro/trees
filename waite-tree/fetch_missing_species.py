from Bio import Entrez
import pandas as pd
Entrez.email = 'drobn.tina@gmail.com'


def get_entrez_id(accession):
	handle = Entrez.esearch(db='assembly', term=accession, retmax='100000')
	record = Entrez.read(handle)
	handle.close()
	ids = record['IdList']
	return ids


#fetch summary of the assembly identified with the id, 
def get_assembly_summary(ids):
	handle = Entrez.esummary(db='assembly', id=ids, report='full')
	record = Entrez.read(handle, validate=False)
	handle.close()
	summary = record['DocumentSummarySet']['DocumentSummary'][0]
	status = summary['AssemblyStatus']
	print(status)
	acc = summary['Synonym']
	ftp = summary['FtpPath_RefSeq']
	if 'genome' in status.lower() or 'chromosome' in status.lower():
		return acc, ftp


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# open the nodes-taxid-count sheet with missing species
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

df = pd.read_excel('tree-nodes-taxid-count.xlsx', sheet_name='species_im_missing') # open the species i'm missing table
sp_taxid = ['txid' + str(i) + '[Organism]' for i in df['species_taxid']] # make a list of taxid's of the species i'm missing (format: 'txid0000[Organism]')

a = 0
gcf_df = pd.DataFrame(columns=['Genbank', 'RefSeq', 'Similarity', 'ftp']) # make df into which results will be saved
print(gcf_df)


for taxid in sp_taxid: # for each taxid
	uid = get_entrez_id(taxid) #search each taxid to get the universalID from entrez (is sometimes a list- different strains of same species)
	print(uid)
	for i in uid:
		output = get_assembly_summary(i) #get the assembly summary
		if output is not None: # if the output is not empty, split the 'output' into the two things that the function returns
			acc, ftp = output
			acc['ftp'] = ftp # add ftp link as an entry in the dictionary
			gcf_df = gcf_df.append(acc, ignore_index=True) # add the dictionary as a line to the results df
			a += 1
			print(acc, a)

print(gcf_df)

gcf_df.to_csv('missing_genomes.tsv', sep='\t', index=False) #save the df as a table. used the links to download the 10 missing protein fastas.
