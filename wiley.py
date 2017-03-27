# -- coding: utf-8 --"
"""
Parse a tab delimitted sheet of Wiley ebooks, remove withdrawn ebooks, and create an additions file to upload to SPIRES
"""
import re
from pickle import load, dump

record = ''
counter = 0
marc_counter = 0
withdrawnisbns = []
yearly_series = 'Wiley 2016 package purchase'

with open('wiley_input.in', 'r') as input:
    inlist = [line for line in input.readlines()]
    print "In:", len(inlist)
with open('wiley_withdrawn.in', 'r') as withdrawn:
    nolist = [line for line in withdrawn.readlines()]
for line in nolist:
    matchobj = re.match(r'.*?\t(\w{13}).*', line)
    if matchobj:
        isbn = matchobj.group(1).strip()
        withdrawnisbns.append(isbn)
print "skip:", len(withdrawnisbns)

with open('wiley_marc.out', 'rb') as marc_in:
    marc_dict = load(marc_in)

for line in inlist:
#    matchobj = re.match(r'(.*?)\t(.*?)\t(.*?)\t(\d.*?\t|\t).*?(\d+)\t(http.*?)\t(\d{4})\t(\d+)(\t.*)', line)
    matchobj = re.match(r'(.*?)\t(.*?)\t(\w{10})\t(\w{10})\t(\w{13})\t(\w{13})\t.*?\t(.*?)\t(\d+)\t(http.*?)\t(\d{4})\t(\d+)(\t.*)', line)
    if matchobj:
        author = matchobj.group(1)
        title = matchobj.group(2)
        print_isbn10 = matchobj.group(3).strip()
        ebook_isbn10 = matchobj.group(4).strip()
        print_isbn13 = matchobj.group(5).strip()
        ebook_isbn13 = matchobj.group(6).strip()
        isbns = [print_isbn10, ebook_isbn10, print_isbn13, ebook_isbn13 ]
        sh = matchobj.group(7)
        oclc = matchobj.group(8)
#        if len(oclc) == 1:
#            oclc = False
        url = matchobj.group(9)
        year = matchobj.group(10)
        pages = matchobj.group(11)
        pbn = matchobj.group(12)
        pbn = pbn.strip()
        edition = False
        toc = False
#        if oclc in marc_dict:
#            if 'A' in marc_dict[oclc]:
#                author = marc_dict[oclc]['A'].encode('utf-8')
#            if 'ED' in marc_dict[oclc]:
#                edition = marc_dict[oclc]['ED'].encode('utf-8')
#            if 'TOC' in marc_dict[oclc]:
#                toc = marc_dict[oclc]['TOC'].encode('utf-8')
        for x in isbns:
            if x in marc_dict.keys():
                marc_counter +=1
                if 'A' in marc_dict[x]:
                    author = marc_dict[x]['A'].encode('utf-8')
                if 'ED' in marc_dict[x]:
                    edition = marc_dict[x]['ED'].encode('utf-8')
                if 'TOC' in marc_dict[x]:
                    toc = marc_dict[x]['TOC'].encode('utf-8')

        if ebook_isbn13 not in withdrawnisbns:
            counter += 1
            record += """ADD;
ASTR;
  A = %s;
T = %s;
ISBN = %s;
ISBN = %s;
ISBN = %s;
ISBN = %s;
CL = %s:ONLINE;
SH = %s;
OCLC = %s;
FT = %s;
D = %s;
DESC = 1 online resource (%s p.);
SER = eBooks;
SER = Wiley Online Library;
SER = %s;
TYPE = ONLINE;
""" % (author, title, print_isbn13, print_isbn10, ebook_isbn13, ebook_isbn10, print_isbn10, sh, oclc, url, year, pages, yearly_series)
            if pbn != '':
                record += "PBN = %s;\n" % pbn
            if edition:
                record += "ED = %s;\n" % edition
            if toc:
                record += toc
            record += ";\n"

#print record.encode('utf-8')
with open('wiley_output.out', 'w') as output:
    output.write(record)
print counter
print marc_counter, "records matched to MARC"

