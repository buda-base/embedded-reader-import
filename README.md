# Collection import script for BDRC's eReader

Import script for the BDRC embeded reader.

This script takes a TSV file (in the `input/` folder), generated from a spreadsheet representing the collection, and outputs a .trig file (in the `output/` folder), ready to be imported in BDRC's database to generate the iframe code.

## Dependency installation

```sh
$ pip3 install -r requirements.txt
```

It may also be necessary to:

```sh
pip3 install setuptools
```

before the requirements.txt.

## Running the script

To output the RDF of one tsv file:

```sh
$ python3 tsvtordf.py input/myfile.tsv
```

To convert all the files into the `output/` folder:

```
for i in input/*.tsv; do b=`basename $i`; bnoext=${b%.*}; python3 tsvtordf.py $i > output/$bnoext.trig; done
```

## Uploading to Fuseki

When on buda2, once the files have been converted, run:

```
for i in output/*.trig; do b=`basename $i`; bnoext=${b%.*}; bin/putg bdrcrw $b $i; done
```

## Input file format

## Setting up an embedded reader

- [Setup Tutorial](https://github.com/buda-base/public-digital-library/blob/master/BDRC_Embedded_Reader.md)
- [Embeded Reader demo sites](https://github.com/bdrc-reader)
