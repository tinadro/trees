from Bio import Entrez
Entrez.email = 'td1515@ic.ac.uk'

handle = Entrez.esearch(db='assembly', term='UBA6792')
record = Entrez.read(handle)


#get raw assembly summary
handle = Entrez.esummary(db='assembly', id='1275351', report='full')
record = Entrez.read(handle)
#print(type(record))

#print(record['DocumentSummarySet'])

summary = record['DocumentSummarySet']['DocumentSummary']



#for key in summary[0]['Biosource'].keys():
#	print(key)

uba = summary[0]['Biosource']['Isolate']


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

