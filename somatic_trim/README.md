## Read trimming

The goal of this experiment was to explore the impact of 3' read trimming on run
times and quality performance for [a sequenced mixture dataset of two Genome in a Bottle
samples](ftp://ftp-trace.ncbi.nlm.nih.gov/giab/ftp/use_cases/mixtures/UMCUTRECHT_NA12878_NA24385_mixture_10052016/)
simulating a lower frequency set of calls. It has a 90x tumor genome consisting
of 30% NA12878 (tumor) and 70% NA24385 (germline) and a 30x normal genome of
NA24385. Unique NA12878 variants are somatic variations at 15% and 30%.

This sample has slow runtimes with many callers, potentially due to read quality
issues. Inspired by [DNAnexus' work examining problematic reads with Readshift](https://blog.dnanexus.com/2018-01-16-evaluating-the-performance-of-ngs-pipelines-on-noisy-wgs-data/)
we looked at the impact of 3' quality trimming on runtimes. We also added polyG
trimming to avoid G errors at the end of NovaSeq reads, and polyX trimming to
remove other low complexity regions that could contribute to slow alignment and
variant calling times.

Two different trimming methods [atropos](https://github.com/jdidion/atropos)
and [fastp](https://github.com/OpenGene/fastp) had different impacts on read
calls and runtimes. Both callers helped improve sensitivity of SNP and indel
detection.  However, atropos improved runtimes for both alignment and variant
calling, while fastp runtimes were about identical to untrimmed. To explore
further, we examined more aggressive polyX tripping with fastp and less
aggressive trimming with atropos. Runtime improvements were dependent on how
aggressively we trimmed polyA tails. With the default settings, atropos is 
quite aggressive and will trim the 3' end of any read with a polyA stretch of
3 basepairs or more due to non-anchored 3' trimming and a
[default overlap default of 3](https://atropos.readthedocs.io/en/latest/guide.html#reducing-random-matches).
While this did not impact sensitivity/specificity in this validation set, it
trims too much for low frequency detection where we have the potential to remove
real variants and less datasets to ensure this doesn't happen.

This allowed us to identify the contributions different trimming components make
to both validations and runtime. Adjusting aggressiveness in 3'
quality trimming with fastp did not change variant calling runtimes, suggesting
the runtime difference is due to polyX trimming. When examining the top 3' ends
remaining after atropos and fastp trimming, the fastp ends primarily included
polyA, polyT and polyC stretches. This indicates that our crude method of
trimming these using adapter sequences is more effective with atropos, and that
removing these stretches provides the greatest runtime improvements in this
dataset. We provide runtime tradeoffs and trimming aggressiveness for the 3
methods in part of an ongoing validation process.

Thanks to the [The University of Melbourne Centre for Cancer Research](
http://mdhs.unimelb.edu.au/our-organisation/institutes-centres-departments/the-university-of-melbourne-centre-for-cancer-research) and [AstraZeneca Oncology](https://www.astrazeneca.com/our-focus-areas/oncology.html) 
for support in running these evaluations.

### Quality changes

Both atropos and fastp improve sensitivity of detection, which appears to be due
to removal of low quality bases at the 3' ends of reads:

![giab-mix-trim](giab-mix/grading-summary-gm1-trim.png)

### Post-trimming Runtime changes

#### minimap2 alignment

Alignment runtimes for atropos trimming fastq files
are 75-80% of the original non-trimmed runs, while fastp are
20:14-21:11
the same: untrimmed (1:10), atropos (0:53), fastp (1:07)

#### Variant calling runtimes for the worst case region (chr20 full region)

atropos improves runtimes, especially for callers like MuTect2 that struggled
with slow runs on this data. fastp has a smaller improvement in runtime.
Aggressive trimming with atropos provides a baseline for potential improvements,
but 3' trimming of anything with polyX stretches greater than 3bp was too
excessive.

caller   | untrimmed | atropos | fastp | atropos aggressive |
--- | --- | --- | --- | --- |
vardict  |  1:46 |  1:12 67% |  1:25 80% |  1:08 65% |
mutect2  |  5:59 |  3:45 62% |  5:03 84% |  2:38 44% |
strelka2 |  0:36 |  0:27 75% |  0:32 89% |  0:28 78% |

### Trimming runtimes

Trimming times on a 16 core AWS machine with SSD storage:

- atropos 1:26
- fastp 1:19

### Trimming differences

The differences in runtime appear to be due to removal of polyA, polyT and polyC
read ends during trimming. polyG stretches, which are often present in new
NovaSeq data, get removed consistently by both callers. The aggressiveness of
trimming 3' ends containing other polyA/T/C stretches determines runtime
improvements by avoid extra computational work aligning and variant calling in
these low complexity region. We're working with the fastp team to discuss 
improved approaches to help remove these as part of the fastp trim so the two
methods consistently trim reads.

Top 15 remaining 3' ends for fastp trimming:

     TTTTTTTTTT 33136
     AAAAAAAAAA 14707
     TTTTTTTTTA 4754
     TTTTTTTTTG 4588
     CCCCCCCCCC 4296
     TTTTTTTTGT 2609
     TTTTTTTTTC 2379
     AAAAAAAAAG 2354
     AAAAAAAAAT 1799
     TTTTTTTTGA 1653
     GTGTGTGTGT 1584
     CTTTTTTTTT 1476
     TGTGTGTGTG 1474
     TTTTTTTTAA 1473
     ACACACACAC 1452

For atropos trimming:

     ACTCTGTCTC 4067
     ACTCCATCTC 3961
     GTGTGTGTGT 3670
     ACTCCGTCTC 3634
     CTTCTGCTTG 2576
     CTAAAAATAC 2203
     CACACACACA 2178
     ACACACACAC 2044
     TGGGATTACA 1972
     ATCCCAGCAC 1968
     TGGAATGGAA 1719
     GGAATGGAAT 1679
     TTTTCTTTTC 1538
     CATTCCATTC 1533
     ACTCCAGCCT 1489
