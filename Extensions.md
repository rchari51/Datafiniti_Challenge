# Data Challenge Response
This project is in response to the Data Challenge from Datafiniti. Its goal is to write an application to extract as much information as possible about a book from a sample Amazon bookpage. While there may be many similarities in formatting between a sample bookpage and today's version of it on Amazon, there will be differences due to which the information extracted will be less if the application is tried on today's webpages.

This folder contains the application **package.py** and the ancillary file **bookpage.py**.
**bookpage.py** contains the class *Extractor* and its base class *BaseExtractor*  .
**package.py** is a driver which uses the information, and in particular, book weights extracted by Extractor.extract() from 20 given html files and solves a bin-packing problem (using a binpacking library) to pack those books into the smallest number of bins such that none of them holds more than 10 lbs. This greedy "first-fit" algorithm [1][2] is guaranteed to find a solution if it exists but may be suboptimal, the problem being NP-hard.

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

## Information Extracted from Amazon pages
The extract() method in Extractor extracts information about many more fields than are suggested in the README.md file attached to the dataset. The list extracted is open-ended and depends on the information available in the book page. The function exploits the machine-readable but unrendered meta data in the sample files, specifically the tags:
```sh
<meta name="title" content="<title>: [<subtitle>:] <author>: <ISBN-13>: <seller>: <product_category>"/>
<meta name="keywords" content = "<author>,<title>,[<subtitle>,]<publisher>,<ISBN-10>,<tag1>,<tag2>,...<tagn>"/>
```
where fields in angled brackets are to be replaced by values. Keywords may or may not be present in an Amazon webpage, but it is there in each element of the dataset, and since that is the object of analysis, we used them.

Deeper processing of the <publisher> field sometimes yields edition and publication date information as well, while the rating in terms of number of stars and the number of customer reviews are extracted from a field with name containing 'Review'. The 

In addition to the abovementioned tags, three tables embedded in the html were sources of information, namely :
```sh
<table .... id="productDetailsTable">     .......(1)
<table ... class="product">               .......(2)
<table id="rentalPriceBlockGrid">         .......(3)
```
Only one of (2) and (3) may be present. These have price information: list price and actual price in (2) and "buy new" price and "rent" price in (3). The former is applicable to "regular" books while the latter applies mainly to textbooks which can be sold back to Amazon and rented.
## Assumptions
In order to extract information from the sample Amazon webpages, we looked at the structure of the html sources with the desired information in mind. We encoded our observations about how to get the most information from webpages in this format. Thus we found that title metadata contained title, author, ISBN-13, seller (Amazon.com), product_category(in this case Books). When a subtitle was present, it was inserted right after Title. Similarly, the keyword metadata is a string containing author, title, optional subtitle, publisher, ISBN-10. This is followed by a variable number of "Tags" which is cataloging/classification data which can be used for fetching books of a certain genre or subject matter. The information in the product details table is in the general format 'key':'value' where 'value' may have a rich structure and more than one interesting value. An attempt has been made to extract such things as the publication date' and the edition. We totally ignore everything including and following the 'Rank' fields.

Prices are retrieved from the the two price tables, only one of which may logivally exist in a web page. One of the price tables gives the 'List Price' and the 'Price'. When there is no discount, there may only be a 'Price' field. We ignore fields such as 'Deal Price'. The other price table format is used mainly for textbooks which may be sold back to Amazon and rented from it or bought new. The 'New' price as well as the 'Rent' price are extracted.
## Extensions
1. **Other Amazon Pages**: It should be clear that extract() depends on many assumptions about the structure of the input html. These assumptions are true for the sample dataset and seem to be largely obeyed on current Amazon pages for books. For example for the book 'Zen Flesh, Zen Bones', we get:
```sh
{
    "Title": " Nyogen Senzaki",
    "Author": "Paul Reps",
    "ISBN-13": "978-0804837064",
    "Seller": " Paul Reps, Nyogen Senzaki",
    "Product_Category": " Books",
    "Publisher": "Tuttle Publishing",
    "ISBN-10": "0804837066",
    "Tags": [
        "Tuttle Publishing",
        "0804837066",
        "Zen",
        "Zen Buddhism",
        "Zen literature",
        "BODY",
        " MIND & SPIRIT / Mindfulness & Meditation",
        "Buddhism - Zen",
        "GENERAL",
        "General Adult",
        "Inspirational/Devotional",
        "Non-Fiction",
        "Oriental & Indian philosophy",
        "PHILOSOPHY / Taoist",
        "PHILOSOPHY / Zen",
        "Philosophy",
        "RELIGION / Buddhism / General (see also PHILOSOPHY / Buddhist)",
        "RELIGION / Buddhism / Zen (see also PHILOSOPHY / Zen)",
        "Readings/Anthologies/Collected Works",
        "Religion / Buddhism / Zen",
        "Religion/Buddhism - Zen (see also Philosophy - Zen)",
        "United States",
        "eastern religions; eastern religious books; buddhist sayings; zen sayings",
        "eastern religions;eastern religious books;buddhist sayings;zen sayings",
        "zen Buddhism; zen buddhism books; zen meditation books",
        "zen Buddhism;zen buddhism books;zen meditation books",
        "zen monks; zen books; meditation books",
        "zen monks; zen books; meditation books; eastern religions; eastern religious books; buddhist sayings; zen sayings; zen Buddhism; zen buddhism books; zen meditation books",
        "zen monks;zen books;meditation books",
        "BODY",
        " MIND & SPIRIT / Mindfulness & Meditation",
        "Buddhism - Zen",
        "PHILOSOPHY / Taoist",
        "PHILOSOPHY / Zen",
        "RELIGION / Buddhism / General (see also PHILOSOPHY / Buddhist)",
        "RELIGION / Buddhism / Zen (see also PHILOSOPHY / Zen)",
        "Religion / Buddhism / Zen",
        "Religion/Buddhism - Zen (see also Philosophy - Zen)",
        "Philosophy",
        "Oriental & Indian philosophy"
    ],
    "Hardcover": "224 pages",
    "Edition": "boxed set/slip cased/casebound edition",
    "Pub. Date": "11/10/2008",
    "Language": "English",
    "Dimensions": "4.5 x 1.1 x 7.2 inches",
    "Shipping Weight": "1.2 pounds",
    "weight": 0
}
```

but similar good behavior is not seen in the case of, say "Eye and Brain: The Psychology of Seeing". This has to do with the latter html's non-conformity with the template. Compare:
```sh
"Eye and Brain: The Psychology of Seeing - Fifth Edition (Princeton Science Library): 9780691165165: Medicine & Health Science Books @ Amazon.com"
```
with:
```sh
"Coding the Matrix: Linear Algebra through Applications to Computer Science: Philip N. Klein: 9780615880990: Amazon.com: Books".
```
The second one complies with the template:
['Title', 'Subtitle', 'Author', 'ISBN-13', 'Seller', 'Product_Category']
whereas the first one does not. I do not have an immediate idea for a generalization that will accommodate all the ad-hoc formats these strings can come in, but see below under **Intelligent Extraction**. **However, for extension to products other than books, the semantics of the meta strings will have to be specified per product type.** 

Extension of this application to other sites is also not easy, since for full functionality it needs at least meta information strings to be present with a certain syntax and semantics which is product-specific and also a product details table. The solution would be some kind of seq2seq model which is trained on a variety of (meta string, field-names) pairs. More investigation and study of Web 2.0 "standards" is obviously necessary.
2. **Efficient bin-packing:** I have not made any attempt towards very efficient bin packing that will scale to millions of items. But research is still on for more efficient and scalable algorithms and heuristics for basic bin-packing as well as variants (multi-capacity, etc.) variants thereof. 
3. **Intelligent Extraction:** This application is aware of the two <meta/> tags and 3 <table>s to look for. What if we did not have any such pointers? I suggest that we can always look for <meta/> tags since they are for carrying machine-readable as opposed to rendered content and are present in most modern e-commerce webpages. Each of these gives us a string which can be split by means of a separator which should be clear from the string. It is the semantics of these substrings that is the question. In order to interpret what these substrings mean, I suggest that we first create a large corpus by collecting together from each page on this website (to reduce variation) all the abovementioned substrings as well as all clean, readable text/content of <li> tags inside <ul> lists or <td> tags inside rows <tr>. Assuming that this collection of text from eah page of this huge website is large enough, we can get an embedding for each word/phrase by using pre-trained word2vec or fastText. We can then find the "value-attribute" relation by using for each substring of a meta-data string the analogy:
```sh
'Toby Segaran': 'Author' :: <substring>:?
'Zen Flesh, Zen Bones':'Title'::<substring>:?
```
    The top most frequent answers to the analogies give us a good idea what these <substring>s mean. With the positional information we have, we can now parse each particular type of meta tag.
    Tables are much easier to parse when they have a structure like:
```sh
<table> 
        <tr>
        <td class="priceBlockLabel">List Price:</td>
        <td><span id="listPriceValue"  class="listprice">$27.99</span></td>
        </tr>
</table>
```
4. **Outputs in other than JSON format**: Extract.extract() returns a dictionary of key-value pairs which can be dumped in json format or any key-value store, such as Redis.

## References
[1] [Bin-packing, First-Fit Algorithm, Wikipedia](https://en.wikipedia.org/wiki/Bin_packing_problem#First-fit_algorithm)
[2] [Bin Packing Problem](https://www.geeksforgeeks.org/bin-packing-problem-minimize-number-of-used-bins/)
[3] [Datefinder package](https://pypi.org/project/datefinder/)
[4] [Beautiful Soup (bs4) package](https://pypi.org/project/beautifulsoup4/)
[5] [Binpacking package](https://pypi.org/project/binpacking/)

