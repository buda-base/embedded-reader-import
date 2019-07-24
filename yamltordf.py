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

def ymltordf(ymlobj):
    """
    Returns an RDF graph or dataset from a yaml object
    """
    ds = rdflib.Dataset()
    mainidlocal = ymlobj['id']
    g = ds.graph(BDG[mainidlocal])
    g.namespace_manager = NSM
    mainurl = URIRef(BDR[mainidlocal])
    g.add((mainurl, RDF.type, BDO.Work))
    g.add((mainurl, RDF.type, BDO.VirtualWork))
    addnames(ymlobj, mainurl, g)
    componentstordf(ymlobj, mainurl, g)
    return ds

def componentstordf(obj, parenturi, g):
    """
    Converts a component in the yaml object into rdf.
    """
    if "components" not in obj:
        return
    i = 1
    for component in obj["components"]:
        res = rdflib.BNode() if "id" not in component else BDR[component["id"]]
        g.add((res, BDO.workPartIndex, Literal(i, datatype=XSD.integer)))
        g.add((res, BDO.workPartOf, parenturi))
        g.add((parenturi, BDO.workHasPart, res))
        if "id_bdrc" in component:
            linkto = URIRef(BDR[component["id_bdrc"]])
            g.add((res, BDO.workLinkTo, linkto))
        addnames(component, res, g)
        i+= 1
        componentstordf(component, res, g)
    

def addnames(ymlobj, resource, graph):
    """
    gets all the name_* properties of the object and adds the labels to the resource.
    Used to convert:
    
    name_foo: bar

    to

    "bar"@foo
    """
    for k, v in ymlobj.items():
        if k.startswith("name_"):
            lt = k[5:]
            lit = Literal(v, lang=lt)
            graph.add((resource, SKOS.prefLabel, lit))


def printrdf(dataset):
    """
    Prints the dataset to stdout, in trig serialization.
    """
    print(dataset.serialize(format='trig').decode("utf-8") )

def getymlfromfile(filepath):
    with open(filepath, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)


if __name__ == "__main__":
    srcfile = sys.argv[1]
    yml = getymlfromfile(srcfile)
    dataset = ymltordf(yml)
    printrdf(dataset)