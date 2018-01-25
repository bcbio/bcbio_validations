#!/usr/bin/env python
"""Summarize variant call from NA24385.
"""
from __future__ import print_function
import collections
import sys

import cyvcf2

def main(giab_file):
    out_file = giab_file.replace(".vcf.gz", ".bed")
    sample = {"short": "HG2", "standard": "HG002"}
    giab_iter = cyvcf2.VCF(giab_file)
    caller_counts = collections.defaultdict(lambda: collections.defaultdict(int))
    overall_counts = collections.defaultdict(lambda: collections.defaultdict(int))
    with open(out_file, "w") as out_handle:
        for rec in giab_iter:
            if not rec.FILTER:
                if _is_called(giab_iter.samples, rec, sample):
                    size = abs(rec.INFO.get("SVLEN", rec.end - rec.start))
                    size_cat = "<2kb" if size < 2000 else ">=2kb"
                    svtype = "%s %s" % (size_cat, rec.INFO["SVTYPE"])
                    support, caller_counts, overall_counts = \
                            _parse_support(rec.INFO.get("ClusterIDs"), sample, svtype,
                                           caller_counts, overall_counts)
                    out_handle.write("%s\t%s\t%s\t%s\t%s\n" % (rec.CHROM, rec.start, rec.end, svtype, support))
    print("* Overall")
    _summarize_overall_counts(overall_counts)
    print("* Per caller")
    _summarize_counts(caller_counts, overall_counts)

def _summarize_overall_counts(in_counts):
    all_keys = set([])
    for svtype, counts in in_counts.items():
        total = float(sum([v for v in in_counts[svtype].values()]))
        for k, v in counts.items():
            if v / total * 100.0 > 10.0:
                all_keys.add(k)
    all_keys = sorted(list(all_keys))
    print(" | ".join([" "] + all_keys))
    for svtype, counts in in_counts.items():
        total = float(sum([v for v in in_counts[svtype].values()]))
        cur = [svtype]
        for k in all_keys:
            v = counts[k]
            cur.append("%s (%.1f%%)" % (v, v / total * 100.0))
        print(" | ".join(cur))

def _summarize_counts(svtype_counts, overall_counts):
    for svtype, counts in svtype_counts.items():
        print("**", svtype)
        total = sum([v for v in overall_counts[svtype].values()])
        for k in sorted(counts.keys()):
            v = counts[k]
            print(k, v, "%.1f%%" % (float(v) / float(total) * 100.0))

def _sequencer_method(cur_id, sample):
    cur_sample, s, m, rep = cur_id.split("_")
    if cur_sample == sample["short"]:
        return (s, m)

def _parse_support(cluster_ids, sample, svtype, caller_counts, overall_counts):
    support = collections.defaultdict(set)
    for s_m in [_sequencer_method(x, sample) for x in cluster_ids.split(":")]:
        if s_m:
            s, m = s_m
            support[s].add(m)
    out = []
    for s, methods in support.items():
        caller_counts[svtype][s] += 1
        for m in methods:
            caller_counts[svtype][m] += 1
        out.append("%s:%s" % (s, ",".join(sorted(list(methods)))))
    overall_counts[svtype]["-".join(sorted(list(support.keys())))] += 1
    return ";".join(out), caller_counts, overall_counts

def _is_called(samples, rec, sample):
    sample_calls = dict(zip(samples, rec.gt_types))
    return sample_calls[sample["standard"]] in set([1, 3])

if __name__ == "__main__":
    main(*sys.argv[1:])
