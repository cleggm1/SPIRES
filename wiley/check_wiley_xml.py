# -- coding: utf-8 --"
import re, string
from lxml import etree
import xml.etree.ElementTree as ET
from pickle import load, dump


DOCUMENT = 'fermilab-wiley-2016.xml'

oclc_test = False
toc_test = False
author_test = False
edition_test = False

docs = {}

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
            au_structure = True
        if 'tag' in elt.attrib:
            content = elt.getchildren()
            oclc_test = False
            toc_test = False
            author_test = False
            edition_test = False
            isbn_test = False
            for child in content:
                if 'code' in child.attrib:
                    oclcs = []
                    isbns = []
                    child.text = re.sub(r'(.*)[\:\;\,\.]$', r'\1', child.text)
                    child.text = string.replace(child.text, ';', '')
                    if elt.attrib['tag'] == '020' and child.attrib['code'] == 'a':
                        matchobj = re.match('^(\w+)', child.text)
                        if matchobj:
                            isbn = matchobj.group(1)
                            isbn_test = True
                            isbns.append(isbn)
                    if elt.attrib['tag'] == '035' and child.attrib['code'] == 'a':
                        matchobj = re.match('.*?(\d+)', child.text)
                        if matchobj:
                            oclc = matchobj.group(1)
                            oclc_test = True
#                            print oclc
                            oclcs.append(oclc)
                    if elt.attrib['tag'] == '035' and child.attrib['code'] == 'z':
                        matchobj = re.match('.*?(\d+)', child.text)
                        if matchobj:
                            oclc = matchobj.group(1)
                            oclc_test = True
                            oclcs.append(oclc)
                    if elt.attrib['tag'] == '505' and child.attrib['code'] == 'a':
                        child.text = string.replace(child.text, '"', '')
                        toc = ';\ntoc = '.join(i for i in wrap(child.text, 235))
                        full_toc = 'toc = ' + toc + ';\n'
                        toc_test = True
                    if elt.attrib['tag'] == '100' and child.attrib['code'] == 'a':
                        author = child.text
                        author_test = True
                    if elt.attrib['tag'] == '250' and child.attrib['code'] == 'a':
                        ed = child.text
                        edition_test = True
#                    if oclc_test:
                    if isbn_test:
#                        for x in oclcs:
                        for x in isbns:
                            docs[x] = {}
                            if toc_test:
                                docs[x]['TOC'] = full_toc
                            if author_test:
                                docs[x]['A'] = author
                            if edition_test:
                                docs[x]['ED'] = ed

print len(docs)
with open('wiley_marc.out', 'wb') as output:
    dump(docs, output)
