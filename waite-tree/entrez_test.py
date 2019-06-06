from Bio import Entrez
Entrez.email = 'td1515@ic.ac.uk'

#GCF_000518225.1

def get_entrez_id(accession):
	handle = Entrez.esearch(db='assembly', term=accession)
	record = Entrez.read(handle)
	ids = record['IdList']
	return ids

#fetch summary of the assembly identified with the id, return the uba, gca, and gcf numbers.
def get_assembly_summary(ids):
	handle = Entrez.esummary(db='assembly', id=ids, report='full')
	record = Entrez.read(handle, validate=False)
	summary = record['DocumentSummarySet']['DocumentSummary'][0]
	species = summary['Organism']
#	uba = summary['Biosource']['Isolate']
#	gca = summary['Synonym']['Genbank']
#	gcf = summary['Synonym']['RefSeq']
	print(species)

ids = get_entrez_id('GCF_000518225.1')
get_assembly_summary(ids)

#handle = Entrez.esearch(db='assembly', term='GCF_000518225.1')
#record = Entrez.read(handle)
#ids = record['IdList'][0]


#get raw assembly summary
#handle = Entrez.esummary(db='assembly', id=ids, report='full')
#record = Entrez.read(handle)
#summary = record['DocumentSummarySet']['DocumentSummary'][0]
#uba = summary['Biosource']['Isolate']
#gca = summary['Synonym']['Genbank']
#gcf = summary['Synonym']['RefSeq']
#print(gca)




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

