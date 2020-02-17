1. www.khampagar.org, https://github.com/khampagar [catalog](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0001.csv)
2. https://vajravidya.org
3. www.glorioussakya.org, https://github.com/Sakya-center [catalog](https://prose.io/#buda-base/embedded-reader-import/blob/master/input/W1ERI0003.csv)
4. www.gadenjangtse.org, https://github.com/Garden-jangtse [catalog](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0004.csv)
5. www.loselingmonastery.net, https://github.com/Loseling [Link](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0005.csv)
6. https://tibetanlibrary.org/bo/, https://github.com/Tibetan-library [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0006.csv)
7. theyungdrungbon.com, https://github.com/geleknyima, [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0007.csv)
8. cuts.ac.in, https://github.com/Cutac [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0008.csv)
9. shechen.org, https://github.com/shechenorg [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0009.csv)
10. namdroling.or, https://github.com/namdroling [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0010.csv)
11. http://dzongsarinstitute.org.in, https://github.com/dzongsarshedra, [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0008.tsv)
12.
13. palpung.org, https://github.com/palpung [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0013.csv)
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
