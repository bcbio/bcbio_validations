# GATK4 validation

Validation runs of the new open source GATK4 release

## NA12878 hg38

NA12878 validation using [50x HiSeq 2000 data](http://www.ebi.ac.uk/ena/data/view/PRJEB3381) from
[Illumina Platinum Genomes](https://www.illumina.com/platinumgenomes.html)

![NA12878_hg38](NA12878_hg38/grading-summary-giab.png)

For GATK4, this comparison includes runs with the Strand Odds Ratio (SOR) included
(`gatk4-haplotype-sor`) and excluded (`gatk4-haplotype`). The
[GATK best practice hard filter recommendations](https://software.broadinstitute.org/gatk/documentation/article?id=2806) include this additional strand bias filter. It improve specificity (~2000 FPs removed)
at the cost of lowering sensitivity (~6000 TPs lost). We don't include the SNP
SOR filter in bcbio to avoid the loss in sensitivity.

The new quality score calculations in GATK4 reduces indel sensitivity
(~26k TPs removed) compared to GATK3 quality scores, but do improve specificity
(~11k FPs removed). We'll explore QD filter tuning in bcbio to help restore some
of the lost sensitivity.

Wall clock timings on AWS m4.4xlarge (16 cores), measured via log timestamps:

- FreeBayes: 6:23
- GATK3: 9:56
- GATK4: 6:05
- VarDict: 2:39
- Sentieon haplotyper: 2:23

Versions:
- hg38 genome build
- GATK4.0a1.2.7.2
- FreeBayes 1.1.0
- GATK3.7
- VarDict 1.5.0
- Sentieon Haplotyper 201704
- Genome in a Bottle NA24385 truth set v3.3.2


## NA24385 10x data on GRCh37

NA24385 validation using [50x HiSeqX inputs from 10x genomics](https://support.10xgenomics.com/de-novo-assembly/datasets)

### bcbio original

GATK based approaches appear to over-call likely due to soft-clipped adapters. Need to explore
approaches to filter and remove these. GATK3, GATK4 and Sentieon haplotyper
perform similarly.

![NA24385_bcbio_orig](NA24385_bcbio_orig/grading-summary-NA24385.png)

Wall clock timings on AWS m4.4xlarge (16 cores), measured via log timestamps:

- FreeBayes: 9:34
- GATK3: 15:59
- GATK4: 25:22
- Sentieon haplotyper: 11:47 -- not full utilization at end, waiting for a few
  slow regions to finish (@10:49313060 -- 7:30, @16:49979430 -- 5:30); Need to
  retest with improved bcbio region sorting; could
  also likely improve with downsampling

Versions:
- GRCh37 genome build
- GATK4.0a1.2.7.2
- FreeBayes 1.1.0
- GATK3.7
- Sentieon Haplotyper 201704
- Genome in a Bottle NA24385 truth set v3.3.2

