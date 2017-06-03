# GATK4 validation

Validation runs of the new open source GATK4 release

## NA24385

NA24385 validation using 50x HiSeqX inputs from 10x genomics:
https://support.10xgenomics.com/de-novo-assembly/datasets

### bcbio original

GATK based approaches appear to over-call likely due to soft-clipped adapters. Need to explore
approaches to filter and remove these. GATK3, GATK4 and Sentieon haplotyper
perform similarly.

![NA24385_bcbio_orig](NA24385_bcbio_orig/grading-summary-NA24385.png)

Versions:
- GATK4.0a1.2.7.2
- FreeBayes 1.1.0
- GATK3.7
- Sentieon Haplotyper 201704
- Genome in a Bottle NA24385 truth set v3.3.2

Timings on AWS m4.4xlarge (16 cores), measured via log timestamps:

- FreeBayes: 9:34
- GATK3: 15:59
- GATK4: 25:22
- Sentieon haplotyper: 11:47 -- not full utilization at end, waiting for a few
  slow regions to finish (@10:49313060 -- 7:30, @16:49979430 -- 5:30); could
  likely improve with downsampling.
