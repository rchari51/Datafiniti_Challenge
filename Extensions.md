
While there may be many similarities in formatting between a sample bookpage and today's version of it on Amazon, there may also be differences due to which this application may not be as  successful. In this document I will briefly touch on some extensions that can be made to the application to make it more generally applicable, powerful and useful.

## Information Extracted from Amazon pages
The extract() method in Extractor extracts information about many more fields than are suggested in the README.md file attached to the dataset. The list of fields extracted is open-ended and depends on the information available in the book page. The function exploits the machine-readable but unrendered meta data in the sample files, specifically the tags:
```sh
<meta name="title" content="<title>: [<subtitle>:] <author>: <ISBN-13>: <seller>: <product_category>"/>
<meta name="keywords" content = "<author>,<title>,[<subtitle>,]<publisher>,<ISBN-10>,<tag1>,<tag2>,...<tagn>"/>
```
where fields in angled brackets are to be replaced by values. The meta tag named "keywords" may or may not be present in an Amazon webpage, but it is there in each element of the dataset, and since that is the object of analysis, we used them.

The <publisher> field sometimes contains edition and publication date information as well, while the rating in terms of number of stars and the number of customer reviews are contained in a field with name which includes 'Review'. This application goes to great lengths to extract publisher, edition, publication date, star rating and number of reviews wherever possible. 

In addition to the abovementioned tags, three tables embedded in the html were sources of information, namely :
```sh
<table .... id="productDetailsTable">     .......(1)
<table ... class="product">               .......(2)
<table id="rentalPriceBlockGrid">         .......(3)
```
Only one of (2) and (3) may be present. These have price information: list price and actual price in (2) and "buy new" price and "rent" price in (3). The former is applicable to "regular" books while the latter applies mainly to textbooks which can be sold back to Amazon and rented.

## Assumptions
In order to extract information from the sample Amazon webpages, we looked at the structure of the html sources and the information embedded within the noise therein. We found two meta tags in each file contaning important machine-readable data. The sequence of data in the meta tag with name="title" could be interpreted as title, author, ISBN-13, seller(?) (Amazon.com) and product_category(in this case 'Books'). When a subtitle was present, it was inserted right after Title. Similarly, the meta tag with name="keywords" has a string containing author, title, optional subtitle, publisher, ISBN-10. This is followed by a variable number of what I call "Tags" which is cataloging/classification data which can be used for fetching books of a certain genre or subject matter. All other meta tags are irrelevant for our purposes.

A product details table one of two kinds of "price tables" are found in each sample webpage. The information in the product details table is in the general format 'key':'value' where 'value' may have a rich structure and more than one interesting value. An attempt has been made to extract such things as the publication date' and the edition. We totally ignore everything including and following the 'Rank' fields.

Prices are retrieved from the the two price tables, only one of which may logically exist in a web page. One of the price tables gives the 'List Price' and the 'Price'. When there is no discount, there may only be a 'Price' field. We ignore fields such as 'Deal Price'. The other price table format is used mainly for textbooks which may be sold back to Amazon and rented from it or bought new. The 'New' price as well as the 'Rent' price are extracted.

Note that in web pages for non-book items such as electronic goods or apparel on Amazon, the abovementioned meta tags may not make sense and may not be (both) present, or , when present, may not have the same syntax and semantics. When the product details table is present in such cases, the keys may be very different. Not only that, the table structure in html may be different. All these pose problems for generalization. The situation gets worse as we proceed to e-commerce pages from, say bnb.com or target.com.

## Extensions
1.A. **Other Amazon Book Pages**: It should be clear that extract() depends on many assumptions about the structure of the input html. These assumptions are true for the sample dataset and seem to be largely obeyed on current Amazon pages for books. For example for the book 'Zen Flesh, Zen Bones', we get:
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
whereas the first one does not. See below under **Intelligent Extraction** for some workaround ideas. However, for extension to products other than books, the semantics of the meta strings will have to be specified *per product type.* 

The approach doesn't work even with pages of other types of items, e.g.,  a camera (https://www.amazon.com/PANASONIC-Mirrorless-14-42mm-Megapixels-DMC-G7KS/dp/B00X409PQS/ref=sr_1_7?ie=UTF8&qid=1544390473&sr=8-7&keywords=panasonic%2Blumix%2Bcamera&th=1). Here the meta keywords string is:""PANASONIC,PANASONIC LUMIX G7 4K Mirrorless Camera, with 14-42mm MEGA O.I.S. Lens, 16 Megapixels, 3 Inch Touch LCD, DMC-G7KK (USA BLACK),Panasonic,DMC-G7KK ", and the meta title string is similar: "Amazon.com : PANASONIC LUMIX G7 4K Mirrorless Camera, with 14-42mm MEGA O.I.S. Lens, 16 Megapixels, 3 Inch Touch LCD, DMC-G7KK (USA BLACK) : Camera & Photo". The metadata string format is totally different and the field names are also not separated by delimiters. It requires intelligence and domain knowledge to separate the attributes from one another and label them.

Extension of this application to other online bookstores is even less straightforward if only because of the non-standard structure of meta tags.  A solution could be some kind of seq2seq model which is trained on a variety of (meta string, field-names) pairs. More investigation and study of Web 2.0 "standards" is obviously necessary.
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
4. **Outputs in formats other than JSON:** Extract.extract() returns a dictionary of key-value pairs which can be dumped in json format or any key-value store, such as Redis.

## References
#### [1] [Bin-packing, First-Fit Algorithm, Wikipedia](https://en.wikipedia.org/wiki/Bin_packing_problem#First-fit_algorithm)
#### [2] [Bin Packing Problem](https://www.geeksforgeeks.org/bin-packing-problem-minimize-number-of-used-bins/)
#### [3] [Datefinder package](https://pypi.org/project/datefinder/)
#### [4] [Beautiful Soup (bs4) package](https://pypi.org/project/beautifulsoup4/)
#### [5] [Binpacking package](https://pypi.org/project/binpacking/)

