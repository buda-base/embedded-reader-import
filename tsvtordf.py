import sys
import os
import csv
import re
import rdflib
from rdflib import URIRef, Literal, BNode
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

def linestordf(tsvlines, graphname):
    """
    Returns an RDF graph or dataset from a yaml object
    """
    curidx = 0
    ds = rdflib.Dataset()
    g = ds.graph(BDG[graphname])
    g.namespace_manager = NSM
    i = 0
    while i < len(tsvlines):
        # the function returns the last analzed idx
        i = addlineaschild(lines, i, None, g, None)
        i += 1
    return ds

def fillchildrenofline(lines, lineidx, lineres, g):
    """
    Fills the children of a line, returns the last line index to have
    been considered a child.
    """
    linedepth = lines[lineidx]["depth"]
    thislineidx = lineidx + 1
    partidx = 1
    while thislineidx < len(lines):
        # the function returns the last analzed idx
        thisline = lines[thislineidx]
        if thisline["depth"] <= linedepth:
            return thislineidx -1
        thislineidx = addlineaschild(lines, thislineidx, lineres, g, partidx)
        thislineidx += 1
        partidx += 1
    return thislineidx-1


def geturl(parent, partidx):
    if not parent or not partidx: # should only happen when the URI is given in the tsv
        return None
    return URIRef(str(parent)+"_"+('%02d' % partidx))

def addlineaschild(lines, lineidx, parent, g, partidx):
    """
    Adds a line as a child of another one, and get all its children too
    """
    line = lines[lineidx]
    cparts = splitcontent(line["content"])
    thisres = geturl(parent, partidx)
    if cparts[0] is not None:
        firstres = URIRef(BDR[cparts[0]])
        if cparts[0].startswith("W1ERI0"):
            thisres = firstres
        elif cparts[2] is not None:
            loc = BNode()
            locinfo = cparts[2]
            g.add((thisres, BDO.workLocation, loc))
            g.add((loc, BDO.workLocationPage, Literal(locinfo[0], datatype=XSD.integer)))
            g.add((loc, BDO.workLocationEndPage, Literal(locinfo[1], datatype=XSD.integer)))
            startvol = 1 if len(locinfo) < 3 else locinfo[2]
            endvol = startvol if len(locinfo) < 4 else locinfo[3]
            g.add((loc, BDO.workLocationVolume, Literal(startvol, datatype=XSD.integer)))
            g.add((loc, BDO.workLocationEndVolume, Literal(endvol, datatype=XSD.integer)))
            g.add((loc, BDO.workLocationWork, firstres))
        else:
            g.add((thisres, BDO.workLinkTo, firstres))
    g.add((thisres, RDF.type, BDO.Work))
    g.add((thisres, RDF.type, BDO.VirtualWork))
    if parent is not None:
        g.add((thisres, BDO.workPartOf, parent))
        g.add((parent, BDO.workHasPart, thisres))
        g.add((thisres, BDO.workPartIndex, Literal(partidx, datatype=XSD.integer)))
    if cparts[1] is not None:
        g.add((thisres, SKOS.prefLabel, cparts[1]))
    return fillchildrenofline(lines, lineidx, thisres, g)


WRIDPATTERN = re.compile("^W[0-9][^( ]+$")

WRIDLOCPATTERN = re.compile("^W[0-9][^( ]+\(([0-9]+,)+[0-9]+\)")

def splitcontent(c):
    """
    Splits a cell content into RID and name, giving the name as a literal with a lang tag
    """
    c = c.strip()
    firstspaceidx = c.find(" ")
    if firstspaceidx == -1:
        if WRIDPATTERN.match(c):
            return (c, None, None)
        if WRIDLOCPATTERN.match(c):
            openparidx = c.find("(")
            rid = c[:openparidx]
            loc = c[openparidx+1:-1].split(",")
            return (rid, None, loc)
        return (None, getliteralfromstring(c), None)
    firstpart = c[:firstspaceidx]
    if WRIDPATTERN.match(firstpart):
        return (firstpart, getliteralfromstring(c[firstspaceidx+1:]), None)
    if WRIDLOCPATTERN.match(firstpart):
        openparidx = firstpart.find("(")
        rid = firstpart[:openparidx]
        loc = firstpart[openparidx+1:-1].split(",")
        return (rid, getliteralfromstring(c[firstspaceidx+1:]), loc)
    else:
        return (None, getliteralfromstring(c), None)

def getliteralfromstring(s):
    if not s:
        return None
    firstchar = s[0]
    if firstchar > '\u0F00' and firstchar < '\u0FFF':
        return Literal(s, lang="bo")
    else:
        return Literal(s, lang="en")

def printrdf(dataset):
    """
    Prints the dataset to stdout, in trig serialization.
    """
    print(dataset.serialize(format='trig').decode("utf-8") )

def getlinesfromfile(filepath):
    lines = []
    with open(filepath, 'r') as tsvfile:
        reader = csv.reader(tsvfile, delimiter="\t")
        first = True # skipping the first line for now
        for row in reader:
            if first:
                first = False
                continue
            depth = 0
            for cell in row:
                if cell:
                    lines.append({"depth": depth, "content": cell})
                depth += 1
    return lines

def graphnamefromfilepath(filepath):
    basename = os.path.splitext(os.path.basename(filepath))[0].strip()
    firstspaceidx = basename.find(" ")
    if firstspaceidx > 0:
        basename = basename[:firstspaceidx]
    if not basename.startswith("W1ERI0"):
        basename += "W1ERI0"
    return basename

if __name__ == "__main__":
    srcfile = sys.argv[1]
    lines = getlinesfromfile(srcfile)
    dataset = linestordf(lines, graphnamefromfilepath(srcfile))
    printrdf(dataset)