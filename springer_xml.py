#!/usr/bin/python

#this script takes xml input from Springer Verlag and converts it to a SPIRES compatible
#file for batch input to the BOOKS subfile.  It uses the lxml library methods to mine
#needed meta data according to the Springer xml schema.

#unzip -l springer_marc.zip
#unzip -j -p springer_marc ENIN_MathematicsStatistics_1929.xml > test.xml

import re, string
from lxml import etree
import xml.etree.ElementTree as ET

DOCUMENT = '/nashome/c/cleggm1/Springer_2017_Math_LNM.xml'
doc_out = 'tmp_out_'+re.match('/nashome/c/cleggm1/(.*)', DOCUMENT).group(1)

#Now doing all physics through 2009.

out = ''
pub_print = False
isbn_test = False
year_test = False
cl_test = False
#no_isbn_counter = 0
numbers = re.compile('\d+(?:\d+)?')

tree = ET.parse(DOCUMENT)
doc = tree.getroot()

def wrap(txt, width):
    tmp = ""
    for i in txt.split():
        if len(tmp) + len(i) < width:
            tmp+=" "+i
        else:
            yield tmp.strip()
            tmp = i
    yield tmp

for elt in doc.getiterator():
    if len(elt) > 0:
        if 'record' in elt.tag:
            out +=  ';\nadd;\nlocation = ONLINE;\nseries = eBooks;\nseries = Springer eBooks;\nseries = Springer 2017 package;\n'
            au_structure = True
        if 'tag' in elt.attrib:
            content = elt.getchildren()
            cl_test = False
            for child in content:
                if 'code' in child.attrib:
                    child.text = re.sub(r'(.*)[\:\;\,\.]$', r'\1', child.text)
                    child.text = string.replace(child.text, ';', '')
                    if elt.attrib['tag'] == '245' and child.attrib['code'] == 'a':
                        child.text = re.sub('\/$', '', child.text).strip()
                        out += 'title = ' + child.text + ';\n'
                    if elt.attrib['tag'] == '245' and child.attrib['code'] == 'b':
                        child.text = re.sub('\/$', '', child.text)
                        out += 'st = ' + child.text + ';\n'
                    if elt.attrib['tag'] == '020' and child.attrib['code'] == 'a':
                        isbn = re.match('\w+', child.text).group()
                        out += 'isbn = ' + isbn + ';\n'
                        isbn_test = True
#                    if elt.attrib['tag'] == '024' and child.attrib['code'] == 'a':
#                        out += 'note = ' + child.text + ';\n'
                    #if elt.attrib['tag'] == '050' and child.attrib['code'] == 'a':
                        #out += 'cl = ' + child.text + ';\n'
                    if elt.attrib['tag'] == '100' and child.attrib['code'] == 'a':
                        if au_structure:
                            out += 'astr;\n'
                            au_structure = False
                        out += 'a = ' + child.text + ';\n'
                    if elt.attrib['tag'] == '250' and child.attrib['code'] == 'a':
                        out += 'ed = ' + child.text + ';\n'
                    if elt.attrib['tag'] == '300' and child.attrib['code'] == 'a':
                        pages = child.text
#                        pages = re.sub(r'^.*?(\d+) [\.a-z]+[ \:\;\.\(\)a-zA-Z0-9]*$', r'\1', pages)
                        out += 'description = 1 online resource (' + pages + ' p.);\n'
                    if elt.attrib['tag'] == '505' and child.attrib['code'] == 'a':
                        child.text = string.replace(child.text, '"', '')
                        toc = ';\ntoc = '.join(i for i in wrap(child.text, 235))
                        out += 'toc = ' + toc + ';\n'
                    if elt.attrib['tag'] == '650' and child.attrib['code'] == 'a':
                        out += 'sh = ' + child.text + ';\n'
#                    if elt.attrib['tag'] == '710' and child.attrib['code'] == 'a':
#                        out += 'series = ' + child.text + ';\n'
                    if elt.attrib['tag'] == '856' and child.attrib['code'] == 'u':
                        out += 'ft = ' + child.text + ';\n'
                    if elt.attrib['tag'] == '264' and child.attrib['code'] == 'a':
                        pbn = 'pbn = ' + child.text + ': '
                    if elt.attrib['tag'] == '264' and child.attrib['code'] == 'b':
                        if pub_print == True:
                            pass
                        else:
                            pbn += child.text
                            out += pbn + ';\n'
                            pbn = ''
                            pub_print = True
                    if elt.attrib['tag'] == '264' and child.attrib['code'] == 'c':
                        date = numbers.search(child.text).group()
                        out += 'date = ' + date + ';\n'
#                    if elt.attrib['tag'] == '773' and child.attrib['code'] == 't':
#                        out += 'series = ' + child.text + ';\n'
#                    if elt.attrib['tag'] == '830' and child.attrib['code'] == 'a':
#                        series = child.text + ': '
#                    if elt.attrib['tag'] == '830' and child.attrib['code'] == 'v':
#                        out += 'series = ' + series + child.text + ';\n'
                    if isbn_test and not cl_test:
                        cl = isbn + ':ONLINE;\n'
                        out += 'cl = ' + cl
                        cl_test = True
                        isbn_test = False
out += ';'
out.encode('utf-8')
print out.encode('utf-8')
with open(doc_out, 'w') as output:
    output.write(out.encode('utf-8'))
out = ''
exit()
