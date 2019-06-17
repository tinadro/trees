from Bio import Entrez, SeqIO
Entrez.email = 'td1515@ic.ac.uk'

#GCF_000518225.1

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
	return summary

def get_taxonomy_summary(ids):
	handle = Entrez.esummary(db='taxonomy', id=ids, report='full')
	record = Entrez.read(handle, validate=False)
	handle.close()
	summary = record
	return summary	

def get_assembly(ids):
	handle = Entrez.efetch(db='assembly', id=ids)
	record = SeqIO.read(handle, 'fasta')
	handle.close()
	name = ids + 'test.faa'
	SeqIO.write(record, name, 'fasta')


uid = get_entrez_id('GCA_000310245.1')
d = get_assembly_summary(uid)
name = d['Organism'].replace('(e-proteobacteria)', '')
#strain = d['Biosource']['InfraspeciesList'][0]
for key in d.keys():
	print(d[key])
#print('organism_name ', name)
#print('taxid ', d['Taxid'])
#print('species_taxid ', d['SpeciesTaxid'])

#['organism_name', 'infraspecific_name', 'taxid', 'species_taxid']



#	summary[0] keys:
#	RsUid
#	GbUid
#	AssemblyAccession
#	LastMajorReleaseAccession
#	LatestAccession
#	ChainId
#	AssemblyName
#	UCSCName
#	EnsemblName
#	Taxid
#	Organism
#	SpeciesTaxid
#	SpeciesName
#	AssemblyType
#	AssemblyClass
#	AssemblyStatus
#	WGS
#	GB_BioProjects
#	GB_Projects
#	RS_BioProjects
#	RS_Projects
#	BioSampleAccn
#	BioSampleId
#	Biosource
#	Coverage
#	PartialGenomeRepresentation
#	Primary
#	AssemblyDescription
#	ReleaseLevel
#	ReleaseType
#	AsmReleaseDate_GenBank
#	AsmReleaseDate_RefSeq
#	SeqReleaseDate
#	AsmUpdateDate
#	SubmissionDate
#	LastUpdateDate
#	SubmitterOrganization
#	RefSeq_category
#	AnomalousList
#	ExclFromRefSeq
#	PropertyList
#	FromType
#	Synonym
#	ContigN50
#	ScaffoldN50
#	FtpPath_GenBank
#	FtpPath_RefSeq
#	FtpPath_Assembly_rpt
#	FtpPath_Stats_rpt
#	FtpPath_Regions_rpt
#	SortOrder
#	Meta

