import binpacking
from bookpage import Extractor
import os, sys, codecs
import json

'''
The problem of packing a set of books, each with a given weight, into N boxes, each of a certain capacity (100 * 0.1 lbs) 
is an instance of the one-dimensional binpacking problem. Here I conveniently use a library aptly called binpacking, which I installed using pip.
In order to get thepacking schedule, I use the API call:
	binpacking.to_constant_volume(book_weights, capacity)
where capacity is the maximum weight that a box can hold, and book-weights can be a dictionary with book-titles or ids as keys and weights as values.
'''

while True:
    path_to_data_dir = input("Path to html file directory: ")
    if (os.path.isdir(path_to_data_dir)): break
    print(path_to_data_dir, ':no such directory')
while True:
    capacity = input("Capacity of a box in lbs: ")
    try:
        capacity = int(float(capacity)*10)
        break
    except:
        print('please enter a valid number')    
outfilename = input("output file name: ")
if (outfilename == '-'): fout = sys.stdout
else: fout = codecs.open(outfilename, 'w', encoding='utf-8', errors='ignore')


htmls = [os.path.join(path_to_data_dir, file) for file in os.listdir(path_to_data_dir) if file.endswith('.html')]
weights = {}
id = 0
dicts=[]
for html in htmls:
    extractor = Extractor(html)
    jdict = extractor.extract()
    print(extractor.to_json())
    weights[id] = extractor.get_weight()
    extractor.eliminate('weight')
    jdict.pop('weight', None)
    dicts.append(jdict)
    id += 1
    
packages = binpacking.to_constant_volume(weights, capacity)
package_weights = [sum(package.values()) for package in packages]
#list(zip(packages, package_weights))
out_dict = []
for id, pkg in enumerate(packages):
    d = {}
    d['id'] = id
    d['totalWeight'] = package_weights[id]/10.0
    d['contents'] = [dicts[i] for i in pkg]
    out_dict.append(d)
fout.write(json.dumps(out_dict, indent=4))
fout.write('\n')
if fout != sys.stdout: fout.close()
print('Done.')
