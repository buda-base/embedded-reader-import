import sys
import os

def ymltordf(ymlobj):
	"""
	Returns an RDF graph or dataset from a yaml object
	"""
	pass

def componenttordf(ymlcollection, parent, dataset):
	"""
	Converts a component in the yaml object into rdf.
	"""
	pass

def nametolitteral(ymlobj):
	"""
	Returns an RDF litteral with the string and lang tag. Used to convert:
	
	name_foo: bar

	to

	"bar"@foo
	"""
	pass

def printrdf(dataset):
	"""
	Prints the dataset to stdout, in trig serialization.
	"""
	pass

def getymlfromfile(filepath):
	pass


if __name__ == "__main__":
    srcfile = sys.argv[1]
    yml = getymlfromfile(srcfile)
    dataset = ymltordf(yml)
    printrdf(dataset)