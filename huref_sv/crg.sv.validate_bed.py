#!/usr/bin/env python2

""" Calculates sensitivity and precision for 2 bed files, modified from bcbio.structural.validate
    $1 = bed file to evaluate
    $2 = truth set
    $3 = caller
    output: caller.csv, caller.df.csv
"""

import csv
import sys

import pybedtools

from bcbio.structural import validate


EVENT_SIZES = [(50, 100), (100, 300), (300, 500), (500, 1000), (1000, 10000),
               (10000, 100000), (100000, int(1e6))]

def _test(caller, svtype, size_range, ensemble, truth, data):
    efeats = pybedtools.BedTool(ensemble).sort().merge().saveas()
    tfeats = pybedtools.BedTool(truth).sort().merge().saveas()
    match = efeats.intersect(tfeats,u=True,r=0.5,R=0.5).sort().merge().saveas(),count()
    print(match)

data='ploidy'
svtype = 'DEL'
vcaller = sys.argv[3]

with open(vcaller+".csv","w") as out_handle:
    with open(vcaller+".df.csv", "w") as df_out_handle:
        writer = csv.writer(out_handle)
        dfwriter = csv.writer(df_out_handle)
        writer.writerow(["svtype", "size", "caller", "sensitivity", "precision"])
        dfwriter.writerow(["svtype", "size", "caller", "metric", "value", "label"])
        for size in EVENT_SIZES:
            str_size = "%s-%s" % size
#            _test(vcaller,svtype,size,sys.argv[1],sys.argv[2],data)
            evalout = validate._evaluate_one(vcaller,svtype,size,sys.argv[1],sys.argv[2],data)
            writer.writerow([svtype, str_size, vcaller,
                             evalout["sensitivity"]["label"], evalout["precision"]["label"]])
            for metric in ["sensitivity", "precision"]:
                dfwriter.writerow([svtype, str_size, vcaller, metric,
                                   evalout[metric]["val"], evalout[metric]["label"]])
