#!/bin/bash
# read1
OUTDIR=fastq
mkdir -p ${OUTDIR}
for file in $(cut -f10 PRJNA252360.txt | sed 1d | cut -f1 -d";")
do
    samplename=$(basename ${file} _1.fastq.gz)
    wget $file -O ${OUTDIR}/${samplename}
# wget $file
done
# read2
for file in $(cut -f10 PRJNA252360.txt | sed 1d | cut -f2 -d";")
do
    samplename=$(basename ${file} _2.fastq.gz)
    wget $file -O ${OUTDIR}/${samplename}
done
