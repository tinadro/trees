from Bio import SeqIO, Entrez
import sys
import pandas as pd
Entrez.email = 'td1515@ic.ac.uk'
Entrez.api_key = '41267f8592172caaa22ab00ec006c4330208'

def get_entrez_id(accession):
	handle = Entrez.esearch(db='assembly', term=accession, retmax='100000')
	record = Entrez.read(handle)
	handle.close()
	uid = record['IdList']
	return uid

def get_summary(ids):
	handle = Entrez.esummary(db='genome', id=ids, report='full')
	record = Entrez.read(handle, validate=False)
	handle.close()
	return record


#a = get_entrez_id('txid29547[Organism] AND (latest[filter] AND ("chromosome level"[filter] OR "complete genome"[filter]) AND all[filter] NOT anomalous[filter])')
#print(len(a))

b = get_summary('36628')
print(b)
print(type(b))
