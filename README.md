1. khampagar.org, https://github.com/khampagar [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0001.csv)
2. vajravidya.org, https://github.com/thrangu [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0002.csv)
3. glorioussakya.org, https://github.com/Sakya-center [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/blob/master/input/W1ERI0003.csv)
4. gadenjangtse.org, https://github.com/Garden-jangtse [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0004.csv)
5. loselingmonastery.net, https://github.com/Loseling [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0005.csv)
6. tibetanlibrary.org/bo/, https://github.com/Tibetan-library [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0006.csv)
7. theyungdrungbon.com, https://github.com/geleknyima, [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0007.csv)
8. cuts.ac.in, https://github.com/Cutac [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0008.csv)
9. shechen.org, https://github.com/shechenorg [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0009.csv)
10. namdroling.or, https://github.com/namdroling [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0010.csv)
11. dzongsarinstitute.org.in, https://github.com/dzongsarshedra, [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0008.tsv)
12. gadenshartse.org, https://github.com/gadenshartse [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0012.csv)
13. palpung.org, https://github.com/palpung [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0013.csv)
14. gyudra.com, https://github.com/gyudra [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0014.csv)
15. sarah.instituteofbuddhistdialectics.org, https://github.com/sarahcollege [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0015.csv)
16. sakyacollege.org, https://github.com/sakyacollege [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0016.csv)
17. internationalbuddhistacademy.org, https://github.com/internationalbuddhistacademy [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0017.csv)
18. gomanglibrary.com, https://github.com/gomanglibrary [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0018.csv)
19. serajeyrigzodchenmo.org, https://github.com/serajeyrigzodchenmo [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0019.csv)
20. [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0020.csv)
21. tashilhunpo.org, https://github.com/tashilhunpo [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0021.csv)
22.  kirti92.org, [དཀར་ཆག](https://prose.io/#buda-base/embedded-reader-import/edit/master/input/W1ERI0022.csv)
23. [དཀར་ཆག](https://github.com/buda-base/embedded-reader-import/blob/master/input/W1ERI0023.csv)
24. [དཀར་ཆག](https://github.com/buda-base/embedded-reader-import/blob/master/input/W1ERI0024.csv)
25. [དཀར་ཆག](https://github.com/buda-base/embedded-reader-import/blob/master/input/W1ERI0025.csv)
26. [དཀར་ཆག](https://github.com/buda-base/embedded-reader-import/blob/master/input/W1ERI0026.csv)
27.
28.
29.
30.
31.
32.
33.


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
