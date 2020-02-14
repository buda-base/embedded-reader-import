# Collection import script for BDRC's eReader

Import script for the BDRC embeded reader.

This script takes a TSV file (in the `input/` folder), generated from a spreadsheet representing the collection, and outputs a .trig file (in the `output/` folder), ready to be imported in BDRC's database to generate the iframe code.

## 

1.
2.
3. Sakya-center [Link](https://prose.io/#buda-base/embedded-reader-import/blob/master/input/W1ERI0003.csv)
4. Garden-jangtse [Link](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0004.csv)
5. Gurthang Tsering [Link](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0005.csv)
6. Tibetan Library [Link](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0006.csv)
7. theyungdrungbon.com, https://github.com/geleknyima, [catalog](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0007.csv)
8. varanasi college [Link](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0008.csv)
9.
10.
11.
12.
13.
14.
15.
16.
17.
18.
19.
20.



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
for i in input/*.tsv; do b=`basename $i`; bnoext=${b%.*}; bfirst=${bnoext% *}; python3 tsvtordf.py $i > output/$bfirst.trig; done
```

## Uploading to Fuseki

When on buda2, once the files have been converted, run:

```
for i in output/*.trig; do b=`basename $i`; bnoext=${b%.*}; putg bdrcrw $b $i; done
```

Note that `putg` is located in ~/bin/ on buda2 and so ~/bin must be on the path when the above is run.

## Input file format

To create a tsv catalog, copy-paste the catalog from a spreadsheet in a copy of an existing tsv.

Each line of the spreadsheet should only contain one value. Section and subsections only need to contain the names, while works should contain a BDRC Work ID. Titles from BDRC will be displayed by default. You can replace them with a custom title by adding a space and the custom title after the Work ID. 

[spreadsheet screenshot]

For texts running from a specific page to another page, add these four things to the tsv files (\<start volume\> and \<end volume\> are optional):
  
```
W123(120,347,3,5) title
W123(<start page>,<end page>,<start volume>,<end volume>) title
```
## Setting up an embedded reader

Iframe code:
```
<iframe src="http://library.bdrc.io/scripts/embed-iframe.html?work=bdr:W1ERI#######&origin=website.com"></iframe>
```

- [setup instructions](https://github.com/buda-base/public-digital-library/blob/master/BDRC_Embedded_Reader.md)
- [catalog spreadsheets](https://drive.google.com/drive/folders/1sW4fFSYPswMg9pfP7zpVdy-VlGu1MLIY?usp=sharing)
- [demo sites](https://github.com/bdrc-reader)
