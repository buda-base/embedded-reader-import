import sys
import os
import yaml
import rdflib
from rdflib import URIRef, Literal
from rdflib.namespace import RDF, SKOS, Namespace, NamespaceManager, XSD

BDR = Namespace("http://purl.bdrc.io/resource/")
BDO = Namespace("http://purl.bdrc.io/ontology/core/")
BDG = Namespace("http://purl.bdrc.io/graph/")
BDA = Namespace("http://purl.bdrc.io/admindata/")
ADM = Namespace("http://purl.bdrc.io/ontology/admin/")

NSM = NamespaceManager(rdflib.Graph())
NSM.bind("bdr", BDR)
NSM.bind("", BDO)
NSM.bind("bdg", BDG)
NSM.bind("bda", BDA)
NSM.bind("adm", ADM)
NSM.bind("skos", SKOS)

def linestordf(tsvlines):
    """
    Returns an RDF graph or dataset from a yaml object
    """
    pass

def printrdf(dataset):
    """
    Prints the dataset to stdout, in trig serialization.
    """
    print(dataset.serialize(format='trig').decode("utf-8") )

def getlinesfromfile(filepath):
    with open(filepath, 'r') as stream:
        pass


if __name__ == "__main__":
    srcfile = sys.argv[1]
    yml = getlinesfromfile(srcfile)
    dataset = linestordf(yml)
    printrdf(dataset)