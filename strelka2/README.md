# strelka2 validation

Validation runs of [strelka2](http://dx.doi.org/10.1101/192872).

## Somatic NA12878/NA24385 mixture

A sequenced mixture dataset of two Genome in a Bottle samples simulating
a lower frequency set of calls. It has a 90x tumor genome consisting of 30% NA12878 
(tumor) and 70% NA24385 (germline) and a 30x normal genome of NA24385. Unique
NA12878 variants are somatic variations at 15% and 30%. This is a WGS dataset
subset to examine genome wide exome regions along with all of chromosome 20.

![NA12878-NA24385](NA12878-NA24385/grading-summary-gm1.png)

Versions:
- GRCh37 genome build
- Strelka 2.8.2
- GATK4.0b5
- FreeBayes 1.1.0.46
- VarDict 1.5.1
