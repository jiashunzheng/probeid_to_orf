#! /usr/bin/env python
import sys
import re

"""Convert probe id to orf"""


#store probe_info from GPLXX file
probe_info = {}
pattern1 = re.compile('.*platform_table_begin')
pattern2 = re.compile('.*platform_table_end')
with open(sys.argv[1]) as gpl:
    line = gpl.readline()
    probeLine = False
    while line:
        match = pattern1.match(line)
        if match:
            line = gpl.readline()
            probeLine = True
        elif probeLine:
            match2 = pattern2.match(line)
            if match2:
                probeLine=False
            else:
                items = line.strip().split('\t')
                probe_info[items[0]]=items
        line = gpl.readline()

#for probe_id in probe_info:
#    print probe_id,probe_info[probe_id][1],probe_info[probe_id][11]

pattern3 = re.compile('.*series_matrix_table_begin')
pattern4 = re.compile('.*series_matrix_table_end')
title_pattern = re.compile('.*Sample_title')
with open(sys.argv[2])as matrix:
    line = matrix.readline()
    head = None
    in_data = False
    while line:
        title_match = title_pattern.match(line)
        if title_match:
            title = re.sub('\"','',line)
            title = re.sub('^\!','',title)
            print title.strip()
        match = pattern3.match(line)
        if match:
            head = matrix.readline()
            #print head.strip()
            in_data = True
        else:
            match = pattern4.match(line)
            if match:
                in_data = False
            elif in_data:
                items = line.strip().split("\t")
                probe_id = items[0][1:-1]
                if probe_id in probe_info and probe_info[probe_id][11]:
                    print probe_info[probe_id][11]+"\t"+"\t".join(items[1:])
        line = matrix.readline()

