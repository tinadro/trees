from Bio import Entrez
Entrez.email = 'td1515@ic.ac.uk'

handle = Entrez.esearch(db='assembly', term='UBA6792')
record = Entrez.read(handle)


#get raw assembly summary
handle = Entrez.esummary(db='assembly', id='1275351', report='full')
record = Entrez.read(handle)
print(record)
