import sys, os, re, codecs
from bs4 import BeautifulSoup #pip install bs4
import json
import datefinder #pip install datefinder
from datetime import datetime
from copy import copy
class BaseExtractor(object):
    def __init__(self, file):
        if not os.path.isfile(file):
            print(file, ": no such file")
            sys.exit(1)
        if not file.endswith('.html'):
            print(file, "is not an html file")
            sys.exit(2)
        self.file = file
        html = codecs.open(file, 'r', encoding='utf-8', errors='ignore')
        self.soup = BeautifulSoup(html, features="html5lib")
        self.dict = {}
    def to_json(self):
        return json.dumps(self.dict, indent=4)
    def getmeta(self, name):
        h = self.soup.find('meta', {'name':name})
        return h['content'] if h else ""
 
import sys, os, re, codecs
from bs4 import BeautifulSoup #pip install bs4
import json
import datefinder #pip install datefinder
from datetime import datetime
from copy import copy

class Extractor(BaseExtractor):
    TEMPLATE1 = ['Title', 'Author', 'ISBN-13', 'Seller', 'Product_Category']
    TEMPLATE15 = ['Title', 'Subtitle', 'Author', 'ISBN-13', 'Seller', 'Product_Category']
    TEMPLATE2 = ['Author', 'Title', 'Publisher', 'ISBN-10']
    SEP1 = ':'
    SEP2 = ','
    def __init__(self, file):
        super().__init__(file)
    
    def process_meta_inf(self, metastring, sep, template1, template2):
        mydict = {}
        fields = metastring.split(sep)
        template = self.select_template(len(fields), template1, template2)
        for i, field in enumerate(template):
            mydict[field] = fields[i]
        if (len(fields) > len(template)):
            mydict['Tags'] = fields[len(template):]
        return mydict
    def process_metatitle(self):
        metastring = self.getmeta('title')
        res={}
        if metastring:
            res = self.process_meta_inf(metastring,  Extractor.SEP1, Extractor.TEMPLATE1, Extractor.TEMPLATE15)
        return res
    
    def process_keywords(self):
        keywds = self.getmeta('keywords')
        res={}
        if(keywds):
            res = self.process_meta_inf(keywds, Extractor.SEP2, Extractor.TEMPLATE2, Extractor.TEMPLATE2) #duplication intended!
        return res
    
    def get_subtitle_if_any(self, template):
        mydict = {}
        if  ':' in self.dict['Title']:
            splt = self.dict['Title'].split(':')
            mydict['Title'] = splt[0]
            mydict['Subtitle'] = splt[1]
        return mydict
    
    def select_template(self, lenfields, template1, template2):
        for template in [template1, template2]:
            if (lenfields == len(template)): return template
        return template2
    
    def extract_product_details(self, table):
        '''Extract information from the Product Details Table'''
        '''
        Example:
        <table cellpadding="0" cellspacing="0" border="0" id="productDetailsTable">
        <tr>
           <td class="bucket">
              <h2>Product Details</h2>
              <ul>
                 <li><b>Hardcover:</b> 1192 pages</li>
                 <li><b>Publisher:</b> Wolfram Media; 1 edition (May 14, 2002)</li>
                 <li><b>Language:</b> English</li>
                 <li><b>ISBN-10:</b> 1579550088</li>
                 <li><b>ISBN-13:</b> 978-1579550080</li>
                 <li><b>
                        Product Dimensions: 
                    </b>
                    2.4 x 8.3 x 9.8 inches
                </li>
                <li><b>Shipping Weight:</b> 5.6 pounds (<a>.......</a>)</li>
                <li><b>Average Customer Review</b> <script type='text/javascript'>.............</script>
                .....</li>
                
                <li id="SalesRank">.....</li>
                .....
            </ul>
           </td>
        </tr>
    </table>

    '''
        jd = {}
        if not table: return jd
        tbody = table.tbody
        rows = tbody.find_all('tr')
        main = rows[0]
        tds = main.find_all("td")
        divs = tds[0].find_all('div')
        ul = divs[0].find_all('ul')
        lis = ul[0].find_all('li')
        stars = ''
        numreviews=''
        for li in lis:
            txt = li.text.strip()
            if ('Review' in txt):
                txt = txt.split('\n')[-1].lstrip(' ')
                if 'stars' in txt:
                    stars =  txt[:txt.index('stars')] + 'stars'
                    jd['Rating'] = stars
                revindex = txt.find('See all reviews')
                if revindex > 0:
                    numreviews = txt[revindex + len('See all reviews ('):-1]
                    jd['Number_of_Reviews'] = numreviews.split(' customer reviews')[0]
            elif ('Dimensions' in txt):
                lines = txt.split('\n')
                jd['Dimensions'] = lines[-1].strip()
            elif ('Shipping Weight' in txt):
                kv = txt.split(':')
                jd['Shipping Weight'] = kv[1].strip().split('pounds')[0] + 'pounds'
            elif ('Publisher' in txt):
                #if there is a semi-colon in txt, it is followed by edition info and optionally pub. date info
                #else look for a date in txt after the publisher info
                kv = txt.split(':')
                if (';' in kv[1]):kvsplit = kv[1].strip().split(';')
                else: kvsplit = kv[1].strip().split('(')
                jd['Publisher'] = kvsplit[0]
                if len(kvsplit) > 1:
                    if ('edition' in kvsplit[1].lower()):
                        ed_date = kv[1].strip().split('; ')[1].lower()
                        if ('edition' in ed_date):
                            jd['Edition'] = ed_date.split('edition')[0] + 'edition'
                date = list(datefinder.find_dates(txt))
                if date:
                    jd['Pub. Date'] = date[0].strftime('%m/%d/%Y')
            
            elif ('Rank' in txt): break
            else:
                if (':' in txt): 
                    kv = txt.split(':')
                    kv[1] = kv[1].split('\n')[0]
                    jd[kv[0]] = kv[1].strip()   
                
        return jd
    
    def get_weight(self):
        '''tries to return weight in tenths of a lb as an integer'''
        if ("Shipping Weight" not in self.dict): return 0
        weight = self.dict["Shipping Weight"]
        myunit= 'pound'
        units = ['lb.', 'lb', 'pounds', 'pound','oz.', 'oz', 'ounces', 'ounce']
        for unit in units:
            if unit in weight:
                try:
                    myunit=unit
                    weight = float(weight.strip().rstrip(unit).strip())
                    if (myunit in ['lb', 'lb.', 'lbs', 'pound', 'pounds']):
                        return round(weight * 10)
                    elif (myunit in ['oz', 'oz.', 'ounce', 'ounces']):
                        wt = round(weight/16.0 *10)
                        if (wt==0): wt=1
                        return wt
                except:
                    return 0
    
 
    def extract_prices(self, pricetable):
        jd={}
        if not pricetable: return jd
        body = pricetable.tbody
        rows = body.find_all('tr')
        for row in rows:
            price=''
            tds = row.find_all("td")
            span1 = tds[1].find('span')
            if (span1):
                if ('<b' in span1.text):
                    price = span1.find('b').text.strip()
                else:
                    price = span1.text.strip()
            else: price=tds[1].text
            if (price):
                jd[tds[0].text.rstrip(':')] = price
    
        '''
        <tr>
        <td class="priceBlockLabel">List Price:</td>
        <td><span id="listPriceValue"  class="listprice">$27.99</span></td>
        </tr>
        '''
        jd.pop("", None)
        return jd
    
    def extract_rental_price(self, rtable):
        jd = {}
        body = rtable.tbody
        rows = body.find_all('tr')
        cells = rows[0].find_all("td")
        for cell in cells:
            if cell.find("div").text == 'Buy New':
                jd['Buy New'] = cell.find("span").text
            elif cell.find("div").text == "Rent":
                jd['Rent'] = cell.find("span").text
        return jd
    def eliminate(self,key):
        self.dict.pop(key, None)
    
    def extract(self):
        #Look for <meta name="title"... > tag and process content if found
        #mtitle = self.getmeta('title')
        #if mtitle:
            #mtitle = mtitle['content']
        self.dict.update(self.process_metatitle())
    
        #Look for <meta name="keywords" and process content if found 
        self.dict.update(self.process_keywords())
    
        #Grab the product details table and extract info from it
        table = self.soup.find("table", id = "productDetailsTable")
        self.dict.update(self.extract_product_details(table))
        self.dict['weight'] = self.get_weight() #weight in tenths of a pound to be used for packing
    
        #extract list and actual price information from the "priceBlock"
        div = self.soup.find("div", {'id':'priceBlock'})
        if div:
            pricetable = div.find("table", attrs={"class":"product"})
            self.dict.update(self.extract_prices(pricetable))
        #extract new and rental price where applicable from "rentalPriceBlockGrid"
        tab = self.soup.find("table", id = "rentalPriceBlockGrid")
        if (tab):
            self.dict.update(self.extract_rental_price(tab))
        #if 'You Save' in jdict:
        #    jdict['You Save'] = jdict['You Save'].split('\n')[0]
        self.dict.pop('You Save', None)
        return self.dict 

