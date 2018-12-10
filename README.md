# Data Challenge Response
This project is in response to the Data Challenge from Datafiniti. Its goal is 1) to write an application to extract as much information as possible about a book from a given sample of Amazon book pages, and 2) to automate the process of packing a given set of books into fixed sized boxes, i.e., to solve a bin-packing problem. The two problems are very different: the second one is well-understood and there are multiple open-source solutions available for it. We therefore focus on the first. 

While there may be many similarities in formatting between a sample bookpage and today's version of it on Amazon, there may also be differences due to which this application may not be as  successful. In this document I will briefly touch on some extensions that can be made to the application to make it more generally applicable, powerful and useful.

This folder contains this file, the application **package.py** and the ancillary file **bookpage.py**.
**bookpage.py** contains the class *Extractor* and its base class *BaseExtractor*  .
**package.py** is a driver which uses the information, and in particular, book weights extracted by Extractor.extract() from the 20 given html files and solves a bin-packing problem (using a binpacking library) to pack those books into the smallest number of bins such that none of them holds more than 10 lbs. This greedy "first-fit" algorithm [1][2] is guaranteed to find a solution if it exists but may be suboptimal, the problem being NP-hard.

## Dependencies
**bookpage.py** requires, besides the built-ins *codecs*, *json* and *datetime* the packages *datefinder* [3] and *bs4* [4] which contains *BeautifulSoup*. **package.py** requires *binpacking"[5], a library for, well, binpacking. You can install bs4, datefinder and binpacking using pip or conda, thus:
```sh
$pip install bs4
$pip install datefinder
$pip install binpacking
```
## Running the Application
1. To extract information from an Amazon book webpage formatted similarly to the sample of 20 files in the data directory, open a python 3.6 shell and type:
```sh
>> from bookpage import Extractor
>> import codecs, json
>> bookpage = '/path/to/html/file'
>> html = codecs.open(bookpage, 'r', encoding='utf-8', errors='ignore')
>> extractor = Extractor(html)
>> jdict = extractor.extract() 
>> print(json.dumps(jdict), indent=4)
```
2. To create a packing "schedule" for a set of books all in a single direcory to be packed into boxes with a capacity of C lbs, do
```sh
$ python package.py 
```
and follow the prompts to supply the data directory, the capacity of each box and the output file path. All the html files in the data directory will be processed.
The outout will be written to stdout if '-' is supplied as the output file path.
