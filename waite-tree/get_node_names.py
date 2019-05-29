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

# key in names.keys():
#	print(key)
#this prints out the names very nicely. can save them to a table and then add the 1, 0, -1 for labels accordingly 
#can also split them to extract the GCF/GCA numbers or uba numbers to get the specific species
#then would have to check if i have them in my database (manually?) and then check if i found a BBH (full circle), psiblast hit (outline), or not at all (none)
#and make the text file/ excel file accordingly 


#a = list(names.keys()) #converts names.keys() into a list


