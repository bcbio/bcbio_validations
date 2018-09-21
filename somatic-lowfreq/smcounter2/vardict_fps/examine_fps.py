#!/usr/bin/env python
"""Examine VarDict true/false positives to explore better depth and strand bias filters.
"""
from __future__ import print_function

import collections
import csv
import os
import sys

import cyvcf2
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

def main(tp_file, fp_file):
    max_af = 0.02
    max_dp = 30
    counts = collections.defaultdict(int)
    lf_counts = collections.defaultdict(int)
    stat_file = "vardict-tpfp_stats.csv"
    with open(stat_file, "w") as out_handle:
        writer = csv.writer(out_handle)
        writer.writerow(["metric", "vtype", "VD", "AF", "SBF", "NM"])
        for metric, fname in [("tp", tp_file), ("fp", fp_file)]:
            for vtype, vd, af, sbf, nm in _vcf_metrics(fname):
                counts[metric] += 1
                if af <= max_af:
                    lf_counts[metric] += 1
                if af <= max_af and vd <= max_dp:
                    writer.writerow([metric, vtype, vd, af, sbf, nm])

    df = pd.read_csv(stat_file)
    print(df.describe())
    print(dict(counts))
    print(dict(lf_counts))
    print("tp", df.query("metric == 'tp'").count())
    print(df.query("metric == 'tp'"))
    print(df.query("metric == 'tp'"))
    print("fp", df.query("metric == 'fp'").count())
    sns.set_style("whitegrid")
    g = sns.FacetGrid(df, col="metric", row="vtype")
    g = g.map(plt.scatter, "SBF", "VD", s=5)
    # g = g.map(plt.scatter, "ODDRATIO", "VD", s=5).set(xlim=(1, 5))
    # g = g.map(plt.scatter, "AF", "ODDRATIO", s=5).set(xlim=(0, max_af), ylim=(0, 3.0))
    # g = g.map(plt.scatter, "AF", "VD", s=5).set(xlim=(0, max_af))
    plt.savefig("%s.png" % os.path.splitext(stat_file)[0])

    classifiers = {}
    for vtype in ["snp", "indel"]:
        print(vtype)
        classifiers[vtype] = build_classifier(df.query("vtype == '%s'" % vtype))

    # Test our manual and built classifications
    for metric, fname in [("tp", tp_file), ("fp", fp_file)]:
        filters = collections.defaultdict(int)
        for rec in cyvcf2.VCF(fname):
            vd, af = rec.format("VD")[0][0], rec.format("AF")[0][0]
            if af <= max_af and vd <= max_dp:
                cur_score, cur_pred = score(rec, classifiers)
                man_pred = "fp" if cur_score < 0 else "tp"
                filter_pred = "fp" if cur_score < -2.5 else "tp"
                if man_pred != cur_pred:
                    print("***", metric, cur_score, man_pred, cur_pred)
                if filter_pred != metric:
                    print(metric, vd, af, cur_score, man_pred, cur_pred)
                filters[filter_pred] += 1
        print(metric, dict(filters))

def score(rec, classifiers):
    vd, sbf, nm = rec.format("VD")[0][0], rec.INFO.get("SBF"), rec.INFO.get("NM")
    vtype = "indel" if any([len(x) > 1 for x in [rec.REF] + rec.ALT]) else "snp"
    pred = classifiers[vtype].predict([[vd, sbf, nm]])
    if vtype == "snp":
        return -1.7075 + vd * 0.2206 + sbf * 1.6367 - 2.7534 * nm, pred[0]
    else:
        return -1.9549 + vd * 0.0755 + sbf * 0.9401 - 2.2070 * nm, pred[0]

def build_classifier(df):
    X = df[["VD", "SBF", "NM"]]
    y = df["metric"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=0)

    logreg = LogisticRegression()
    logreg.fit(X_train, y_train)

    print(logreg.intercept_)
    print(logreg.coef_)

    y_pred = logreg.predict(X_test)
    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    return logreg

def _vcf_metrics(fname):
    for rec in cyvcf2.VCF(fname):
        vtype = "indel" if any([len(x) > 1 for x in [rec.REF] + rec.ALT]) else "snp"
        yield vtype, rec.format("VD")[0][0], rec.format("AF")[0][0], rec.INFO.get("SBF"), rec.INFO.get("NM")

if __name__ == "__main__":
    main(*sys.argv[1:])
