## bcbio validations

A collection of validations run using [bcbio (Blue Collar Bioinformatics)](
http://bcb.io/), using this [community built collection of validation workflows](https://github.com/bcbio/bcbio_validation_workflows). This repository organizes validation interpretation done as part of
developing and improving analyses. Many previous validations are also available
in [these albums](https://chapmanb.imgur.com/).


We're happy to answer questions about any validations, most are works in
progress. We typically write up more details on finalized runs to share more
widely.

- gatk4 -- Comparisons with the new open source GATK4.
- freebayes -- Version updates and filter changes with FreeBayes.
- deepvariant -- Validations with the DeepVariant caller and CHM datasets.
- somatic-lowfreq -- Cancer calling of low frequency somatic variants, including
  tumor-only and FFPE samples.
- [huref_sv](https://github.com/bcbio/bcbio_validations/tree/master/hurev_sv) -- SV calling validation of 8 algorithms in 2018 and 2019 using HuRef benchmark.