import re

uses = []
With open('usage_stats.in', 'r') as input:
    for line in input.readlines():
        """Jan-Mar"""
#        matchObj = re.search(r'DATE-BORROWED = 0[123]/\d{2}/17;', line)
        """Apr-June"""
#        matchObj = re.search(r'DATE-BORROWED = 0[456]/\d{2}/17;', line)
        """Jul-Sep"""
#        matchObj = re.search(r'DATE-BORROWED = 0[789]/\d{2}/17;', line)
        """Oct-Dec"""
#        matchObj = re.search(r'DATE-BORROWED = 1[012]/\d{2}/17;', line)
        if matchObj:
            uses.append(line)

print "%i circs in quarter" % len(uses)
with open('usage_stats.out', 'w') as output:
    output.writelines(uses)

