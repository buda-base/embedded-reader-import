# Collection import script for BDRC's eReader

Import script for the BDRC embeded reader.

This script takes a TSV file (in the `input/` folder), generated from a spreadsheet representing the collection, and outputs a .trig file (in the `output/` folder), ready to be imported in BDRC's database to generate the iframe code.

## Dependency installation

```sh
$ pip3 install -r requirements.txt
```

## Running the script

```sh
$ python3 tsvtordf.py input/myfile.tsv > output/myfile.trig
```

will produce `output/myfile.trig`.