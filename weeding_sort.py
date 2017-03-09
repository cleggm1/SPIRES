"""
Input list of books to weed in the following format:

 CALL-NUMBER = .*;
   TITLE = .*;

Matches title to call number and sorts by call number
"""
import sys
import re


#main = '5yearmain2017.in'
#pop = '5yearpop2017.in'

def main(doc):
    if '.in' in doc:
        out_doc = re.sub('.in$', '.txt', doc)
    else:
        out_doc = doc+'.txt'
    with open(doc, 'r') as input:
        li = [line for line in input.readlines()]
    idx = 0
    unsorted_list = []
    for x in li:
        thiselem = li[idx]
        idx = (idx + 1) % len(li)
        nextelem = li[idx]
        check_cl = re.match('\sCALL-NUMBER = .*;', thiselem)
        check_t = re.match('\s+TITLE = .*;', nextelem)
        if check_cl and check_t:
            unsorted_list.append((check_cl.group(0), check_t.group(0)))
    sorted_list = list(enumerate(sorted(unsorted_list), start=1))
    flat_list = ['['+str(x[0])+']'+x[1][0]+'\n'+x[1][1]+'\n' for x in sorted_list]
    with open(out_doc, 'w') as output:
        output.write('\n'.join(flat_list))


if __name__ == '__main__':
    doc = sys.argv[1:][0]
    try:
        main(doc)
    except KeyboardInterrupt:
        print 'Exiting'
