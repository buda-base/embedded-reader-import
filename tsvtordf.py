# named tsv but it's csv

import sys
import os
import csv
import re
import rdflib
from rdflib import URIRef, Literal, BNode
from rdflib.namespace import RDF, SKOS, Namespace, NamespaceManager, XSD, RDF, RDFS
import glob

BDR = Namespace("http://purl.bdrc.io/resource/")
BDO = Namespace("http://purl.bdrc.io/ontology/core/")
BDG = Namespace("http://purl.bdrc.io/graph/")
BDA = Namespace("http://purl.bdrc.io/admindata/")
ADM = Namespace("http://purl.bdrc.io/ontology/admin/")
BF = Namespace("http://id.loc.gov/ontologies/bibframe/")

NSM = NamespaceManager(rdflib.Graph())
NSM.bind("bdr", BDR)
NSM.bind("", BDO)
NSM.bind("bdg", BDG)
NSM.bind("bda", BDA)
NSM.bind("adm", ADM)
NSM.bind("skos", SKOS)
NSM.bind("rdf", RDF)
NSM.bind("rdfs", RDFS)
NSM.bind("bf", BF)
NSM.bind("xsd", XSD)

RIDSUBST = {}
with open("id-migration.csv", 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        RIDSUBST[row[0]] = row[1]

def linestordf(g, csvlines):
    """
    Returns an RDF graph or dataset from a yaml object
    """
    curidx = 0
    i = 0
    while i < len(csvlines):
        # the function returns the last analzed idx
        i = addlineaschild(csvlines, i, None, g, None)
        i += 1

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
    if not parent or not partidx: # should only happen when the URI is given in the csv
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
        firstres = cparts[0]
        iinstancelname = firstres
        if iinstancelname.startswith("M"):
            iinstancelname = iinstancelname[1:]
        if firstres in RIDSUBST:
            firstres = RIDSUBST[firstres]
        if firstres.startswith("W") and not firstres.startswith("W1ERI0"):
            firstres = "M"+firstres
        firstres = BDR[firstres]
        if cparts[0].startswith("W1ERI0"):
            thisres = firstres
        elif cparts[2] is not None:
            loc = BNode()
            locinfo = cparts[2]
            g.add((thisres, BDO.contentLocation, loc))
            g.add((loc, RDF.type, BDO.ContentLocation))
            g.add((loc, BDO.contentLocationPage, Literal(locinfo[0], datatype=XSD.integer)))
            g.add((loc, BDO.contentLocationEndPage, Literal(locinfo[1], datatype=XSD.integer)))
            startvol = 1 if len(locinfo) < 3 else locinfo[2]
            endvol = startvol if len(locinfo) < 4 else locinfo[3]
            g.add((loc, BDO.contentLocationVolume, Literal(startvol, datatype=XSD.integer)))
            g.add((loc, BDO.contentLocationEndVolume, Literal(endvol, datatype=XSD.integer)))
            g.add((loc, BDO.contentLocationInstance, BDR[iinstancelname]))
        else:
            g.add((thisres, BDO.virtualLinkTo, firstres))
    g.add((thisres, RDF.type, BDO.Instance))
    g.add((thisres, RDF.type, BDO.VirtualInstance))
    if parent is not None:
        g.add((thisres, BDO.partOf, parent))
        g.add((parent, BDO.hasPart, thisres))
        g.add((thisres, BDO.partIndex, Literal(partidx, datatype=XSD.integer)))
    if cparts[1] is not None:
        g.add((thisres, SKOS.prefLabel, cparts[1]))
    return fillchildrenofline(lines, lineidx, thisres, g)


WRIDPATTERN = re.compile(r"^M?W[0-9][^( ]+$")

WRIDLOCPATTERN = re.compile(r"^M?W[0-9][^( ]+\(([0-9]+,)+[0-9]+\)")

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
    if firstchar >= '\u0F00' and firstchar < '\u0FFF':
        return Literal(s, lang="bo")
    else:
        return Literal(s, lang="en")

def getlinesfromfile(filepath):
    lines = []
    with open(filepath, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
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

def migrate_all():
    g = rdflib.Graph()
    g.namespace_manager = NSM
    for fpath in glob.glob("input/*.csv"):
        lines = getlinesfromfile(fpath)
        linestordf(g, lines)
    g.serialize("EMBR.ttl", format="turtle")
    print("now run\ncurl -X PUT -H Content-Type:text/turtle -T EMBR.ttl -G http://buda1.bdrc.io:13180/fuseki/corerw/data --data-urlencode 'graph=http://purl.bdrc.io/graph/EMBR'\nthen\ncurl -XPOST http://purl.bdrc.io/clearcache\ncurl -XPOST http://iiifpres.bdrc.io/clearcache")

if __name__ == "__main__":
    migrate_all()