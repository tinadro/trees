from Bio import Phylo


def lookup_by_names(tree):
    names = {}
    for clade in tree.find_clades():
        if clade.name:
            if clade.name in names:
                raise ValueError("Duplicate key: %s" % clade.name)
            names[clade.name] = clade
    return names #spits out a dictionary where the keys are the node names, values are Clade(branch_length=value, name=same as key)

tree = Phylo.read('Epsilonbacteraeota.renamed.tree', 'newick')
names = lookup_by_names(tree)

#def name_split(name):

for node in names:
	if node.find('GCF_') != -1 or node.find('GCA_') != -1: #if gcf is not provided
		species = '_'.join(node.split('_', 2)[:2])
		gcf = '_'.join(node.split('_', 2)[2:])
	else:
		species = '_'.join(node.split('_', 2)[:2])
		uba = '_'.join(node.split('_', 2)[2:])
		print(uba)
#this prints out the names very nicely. can save them to a table and then add the 1, 0, -1 for labels accordingly 
#can also split them to extract the GCF/GCA numbers or uba numbers to get the specific species
#then would have to check if i have them in my database (manually?) and then check if i found a BBH (full circle), psiblast hit (outline), or not at all (none)
#and make the text file/ excel file accordingly 


#a = list(names.keys()) #converts names.keys() into a list


