#!/usr/bin/env python
"""Compare manta calls to 0.5.0 GiaB reference set.
"""
from __future__ import print_function
import collections
import os
import subprocess
import sys

import cyvcf2

def main(manta_vcf, truth_bed):
    BUFFER = 1000
    manta_bed = manta_vcf.replace(".vcf", ".bed")
    with open(manta_bed, "w") as out_handle:
        for rec in cyvcf2.VCF(manta_vcf):
            if not rec.FILTER and rec.gt_types[0] in set([1, 3]):
                out_handle.write("%s\t%s\t%s\n" % (rec.CHROM, max(0, rec.start - BUFFER), rec.end + BUFFER))
    manta_compare = "%s-giab.bed" % (os.path.splitext(manta_bed)[0])
    cmd = "bedtools intersect -c -wa -a {truth_bed} -b {manta_bed} > {manta_compare}"
    subprocess.check_call(cmd.format(**locals()), shell=True)

    counts = collections.defaultdict(int)
    totals = collections.defaultdict(int)
    with open(manta_compare) as in_handle:
        for chrom, start, end, svtype, info, matches in (l.strip().split("\t") for l in in_handle):
            totals[svtype] += 1
            if int(matches) > 0:
                counts[svtype] += 1

    for svtype, total in totals.items():
        print("| %s | %s (%.1f%%) |" % (svtype, counts[svtype], float(counts[svtype]) / total * 100.0))

if __name__ == "__main__":
    main(*sys.argv[1:])
