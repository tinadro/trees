from Bio import SeqIO

def shorten_accver(query):
	multi_fa = query+'-protein-nr.mfa'
	with open(query+'-protein-nr-ids.mfa', 'a+') as new:
		for record in SeqIO.parse(multi_fa, 'fasta'):
			record.id = record.id.replace('WP_', '')
			record.description = record.description.replace('WP_', '')
			print(record.description)
			SeqIO.write(record, new, 'fasta')
	print(query, 'done')

shorten_accver('PflA')
shorten_accver('PflB')
