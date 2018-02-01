# DeepVariant validations

Validations of [DeepVariant](https://github.com/google/deepvariant) with Genome
in a Bottle and [the CHM based synthetic diploid truthset](https://gatkforums.broadinstitute.org/gatk/discussion/10912/what-is-truth-or-how-an-accident-of-nature-can-illuminate-our-path).

- [Description of inputs and running](https://github.com/bcbio/bcbio_validation_workflows#synthetic-diploid-chm-and-genome-in-a-bottle)
- [CWL workflow](https://github.com/bcbio/bcbio_validation_workflows/tree/master/giab-chm)

## CHM and NA12878 from Genome in a Bottle

![giab-chm](giab-chm/grading-summary-combined.png)

The CHM dataset with filtering for problematic indels (1bp and >50bp) looks
reasonably comparable to NA12878. It has ~2x more false negatives for SNPs and
~4x more false negatives for indels, so either has potential noise or is
identifying regions that Illumina based callers fail to identify.
DeepVariant has improved sensitivity on SNPs for both NA12878 and CHM,
indicating that training on Genome in a Bottle inputs does not bias towards
those samples.

Versions:
- hg38 genome build
- GATK4.0b6
- FreeBayes 1.1.0.46
- strelka 2.8.4
- DeepVariant 0.4.1

## Resources

- [NA12878 false positives for GATK4 and DeepVariant](https://s3.amazonaws.com/chapmanb/validation/giab-chm/NA12878-gatk4-dp-fps.tar.gz) 
