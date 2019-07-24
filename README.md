# Collection import script for BDRC's eReader

Import script for the BDRC embeded reader.

This script takes a TSV file (in the `input/` folder), generated from a spreadsheet representing the collection, and outputs a .trig file (in the `output/` folder), ready to be imported in BDRC's database to generate the iframe code.

## Dependency installation

```sh
$ pip3 install -r requirements.txt
```

## Running the scripts

```sh
$ python3 txttoyaml.py input/myfile.txt > tmp-yaml/myfile.yml
```

will produce `tmp-yaml/myfile.yml`.


```sh
$ python3 yamltordf.py tmp-yaml/myfile.yml > output/myfile.trig
```

will produce the corresponding file in `output/myfile.trig`.