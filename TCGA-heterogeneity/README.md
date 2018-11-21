# Heterogeneity Analysis

## TCGA LUAD

Characterize low frequency variant calls, copy number calls, purity and ploidy
in [TCGA Lung Adenocarcinoma (TCGA
LUAD)](https://portal.gdc.cancer.gov/projects/TCGA-LUAD) samples. We lack full
truth sets for somatic heterogeneity calling, so this attempts to take advantage
of available TCGA samples that also have associated external data, like
[systematic pan-cancer analysis of tumour purity](https://www.nature.com/articles/ncomms9971).
It compares multiple methods and outcomes to help improve preparation of
heterogeneity inputs (CNVs and small variants).

The TCGA LUAD samples are exome tumor/normal pairs,
[sequenced by the Broad Institute with a custom Agilent capture
panel](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0204912).
This appears to be `whole_exome_agilent_1.1_refseq_plus_3_boosters.targetIntervals.bed`
from this [cghub bitbucket repository](https://bitbucket.org/cghub/cghub-capture-kit-info).

## TCGA-05-4395

This sample features a several large deletion/LOH events, as well
as some large amplifications. Because of the instability, both PureCN and
TitanCNA prefer solutions with an overall ploidy of around 3.
PureCN calculates a purity of 0.58 and a ploidy of 3.2. The diploid solutions
for purity/ploidy also have low purity. TitanCNA has a similar solution, with a
purity of 0.57 and a ploidy of 2.9.
TCGA supplied purity estimates range from 0.61-0.80; the low side is in the
range of TitanCNA and PureCN estimates, so this is a promising output.

There is an apparent whole chromosome loss in chromosome 6, indicating LOH for
the HLA regions. This can be seen in both the CNVkit normalized depth as well as
the allele frequency changes.

### CNVkit
![TCGA-05-4395](tcga_luad/TCGA-05-4395-01A-cnvkit.png)

### TitanCNA

![TCGA-05-4395](tcga_luad/TCGA-05-4395-01A-titan_CNA.png)
![TCGA-05-4395](tcga_luad/TCGA-05-4395-01A-titan_LOH.png)

### PureCN
![TCGA-05-4395](tcga_luad/TCGA-05-4395-01A-purecn.png)
![TCGA-05-4395](tcga_luad/TCGA-05-4395-01A-purecn-optima.png)

### PURPLE

![TCGA-05-4395](tcga_luad/TCGA-05-4395-01A.purple.genomecnv.png)


## TCGA-05-4396

This sample has more overall stability with few high copy number regions but
several whole/large chromosome deletion/LOH events. Both PureCN and TitanCNA
prefer ploidy/purity estimates with high overall ploidy of 4. PureCN calculates
a low purity (0.36) and high ploidy (3.8) while TitanCNA finds 3 subclones, a
purity of 0.87 and a ploidy of 3.5. PURPLE calculates a purity of 0.98 with a
ploidy estimate of 0 and estimates a large number of the genome as zero copy.
TCGA supplied purity estimates range from 0.75-0.89, so the PureCN
calculation here seem to overestimate normal contamination. There is a solution
with purity of 0.79 and ploidy of 1.9 that would seem to better fit with other
estimates, although it has a goodness of fit of 0%. We need to explore how to
prioritize the diploid solutions for these more unstable/LOH cases.

We don't see evidence for LOH in chr6 HLA regions, in either the copy number or
allele frequency data.

### CNVkit

![TCGA-05-4396](tcga_luad/TCGA-05-4396-01A-cnvkit.png)

### TitanCNA

![TCGA-05-4396](tcga_luad/TCGA-05-4396-01A-titan_CNA.png)
![TCGA-05-4396](tcga_luad/TCGA-05-4396-01A-titan_LOH.png)

### PureCN

![TCGA-05-4396](tcga_luad/TCGA-05-4396-01A-purecn.png)
![TCGA-05-4396](tcga_luad/TCGA-05-4396-01A-purecn-optima.png)

### PURPLE

![TCGA-05-4396](tcga_luad/TCGA-05-4396-01A.purple.genomecnv.png)

## TCGA LUAD LOHHLA comparison

We compare determination of HLA copy loss with
[LOHHLA](https://bitbucket.org/mcgranahanlab/lohhla/src/master/) with detection
of LOH regions in [chromosome 6 HLA
region](https://www.ncbi.nlm.nih.gov/grc/human/regions/MHC) using standard
copy number and heterogeneity tools. To run LOHHLA, we use fastq reads in HLA
regions extracted using hg38 alternative contigs, baseline HLA calls from
OptiType and purity and ploidy estimated from PureCN.

Overall, we can see many of the events predicted by LOHHLA. For clear cases, we
see good correlation between outcomes: TCGA-05-4395 is a whole chromosome 6 LOH
we see across all methods; TCGA-05-4396 has no apparent HLA LOH. For other
complex cases involving higher copy number coupled with specific allele loss,
the results are less clear, although we see overlap.

### TCGA-05-4389-01A

For HLA-A and HLA-C LOHHLA predicts allele specific deletion of allele 1 with 2
copies of allele 2, so overall ploidy is the same. PureCN replicates this
result, TitanCNA predicts closer to the HLA B estimate from LOHHLA with copy
number duplication of one allele and retention of 1 copy of the other.

#### LOHHLA

Values are p-value of LOH, HLA allele 1, HLA allele 2, copy number of allele 1
and copy number of allele 2.

```
['0.00063140314322408', 'hla_a_02_01_01_01', 'hla_a_32_01_01', '0.458722205661275', '2.96376490842718']
['0.00762452681631165', 'hla_b_15_01_01_01', 'hla_b_44_03_01', '1.3865223986659', '3.18916334128258']
['0.00377407278770889', 'hla_c_03_04_01_01', 'hla_c_16_01_02', '0.182653026069621', '2.70073231713514']
```
#### PureCN
```
['chr6', '656143', '37664356', 'p', '3', '0', 'LOH']
```
#### TitanCNA
```
['chr6', '311938', '29975290', '4', '1', '3', 'ASCNA']
['chr6', '31138712', '32589645', '5', '1', '4', 'ASCNA']
['chr6', '32641370', '32665018', '0', '0', '0', 'HOMD']
['chr6', '32741465', '37663992', '4', '1', '3', 'ASCNA']
```
#### GATK CNV
```
chr6	292288	32829733	2100	-0.066026	0
chr6	32829734	37664356	819	-0.019858	0
```
#### CNVkit
```
['chr6', '500', '38192599', '2', '2', '0']
```

### TCGA-05-4395-01A

A whole chromosome 6 LOH predicted by all methods.

#### LOHHLA
```
['0.000148652350753824', 'hla_a_02_01_01_01', 'hla_a_03_01_01_01', '2.19051316573237', '0.305428006444932']
['0.000786684934282189', 'hla_b_35_01_01_01', 'hla_b_51_01_01', '3.17379346547541', '-0.103923179632395']
['0.000220094380126556', 'hla_c_01_30', 'hla_c_04_01_01_05', '0.824245749199903', '2.50035252715176']
```
#### PureCN
```
['chr6', '1742560', '58553888', 'p', '2', '0', 'WHOLE ARM COPY-NEUTRAL LOH']
```
#### TitanCNA
```
['chr6', '350829', '32460064', '2', '0', '2', 'NLOH']
['chr6', '32519395', '32530211', '1', '0', '1', 'DLOH']
['chr6', '32580804', '170318563', '2', '0', '2', 'NLOH']
```
#### GATK CNV
```
chr6	292288	31507350	1506	-0.384101	-
chr6	31507351	170584833	7295	-0.362979	-
```
#### CNVkit
```
['chr6', '500', '170584583', '1', '1', '0']
```

### TCGA-05-4396-01A

No apparent LOH in chromosome 6, confirmed by all methods. PureCN and TitanCNA
prefer high ploidy solutions but without LOH.

#### LOHHLA
```
['0.30845780569987', 'hla_a_01_01_01_01', 'hla_a_02_01_01_01', '1.50098080697196', '0.421768552095252']
['0.295469124489989', 'hla_b_08_01_01', 'hla_b_40_01_01', '2.12990140845275', '1.31282399564865']
['0.476281061361324', 'hla_c_03_04_01_01', 'hla_c_07_01_01_01', '1.76865616013129', '2.34182738319228']
```
#### PureCN
```
['chr6', '304636', '58553888', 'p', '4', '2', '']
```
#### TitanCNA
```
['chr6', '656555', '32530198', '5', '2', '3', 'UBCNA']
['chr6', '32581606', '32746391', '6', '1', '5', 'ASCNA']
['chr6', '32847198', '170569705', '5', '2', '3', 'UBCNA']
```
#### GATK CNV
```
chr6	292288	32460337	2077	0.126617	0
chr6	32519118	32746646	17	0.067354	0
chr6	32812964	50843644	1957	0.135966	0
```
#### CNVkit
```
['chr6', '27911243', '31815995', '2', '2', '0']
['chr6', '31815995', '31837437', '3', '3', '0']
['chr6', '31839540', '55760535', '2', '2', '0']
```

### TCGA-44-2656-01A

LOHHLA predics copy neutral LOH in HLA-B and HLA-C. PureCN replicates this
result for part of the HLA region with amplification in the surrounding regions.
TitanCNA calls a higher ploidy solution with overall gain.

#### LOHHLA
```
['0.000482787387863338', 'hla_b_18_01_01_01', 'hla_b_39_06_02', '3.28998411896744', '0.150759330131169']
['6.82848908481982e-05', 'hla_c_05_01_01_01', 'hla_c_07_02_01_01', '3.29279971741086', '-0.130630653114102']
```
#### PureCN
```
['chr6', '21594283', '29830634', 'p', '4', '2', '']
['chr6', '29942302', '32222905', 'p', '2', '0', 'COPY-NEUTRAL LOH']
['chr6', '32222906', '33801415', 'p', '4', '2', '']
```
#### TitanCNA
```
['chr6', '4031764', '29588087', '4', '2', '2', 'BCNA']
['chr6', '29942845', '32222707', '3', '1', '2', 'GAIN']
['chr6', '32293730', '53655059', '4', '2', '2', 'BCNA']
```
#### GATK CNV
```
chr6	21594283	29830634	466	0.151833	+
chr6	29942302	32222905	859	-0.201268	-
chr6	32222906	33801415	414	0.155308	+
```
#### CNVkit
```
['chr6', '13053364', '31980550', '2', '2', '0']
['chr6', '31980651', '32223088', '1', '1', '0']
['chr6', '32223853', '69928034', '2', '2', '0']
```

### TCGA-69-7980-01A

LOHHLA predicts copy number specific loss of HLA alleles with a complementary
copy number gain of the other alleles. PureCN replicates this result across the
HLA region. TitanCNA also detects but with a smaller copy number gain
intervening (so a more complex event), based on the GATK CNV segmentation.

#### LOHHLA
```
['1.77545350482363e-10', 'hla_a_02_01_01_01', 'hla_a_31_01_02', '-0.428989636540513', '4.26162050700963']
['1.60587006356982e-11', 'hla_b_14_01_01', 'hla_b_57_01_01', '4.93736910090715', '-0.190521170078914']
['1.44446811565386e-09', 'hla_c_06_02_01_01', 'hla_c_08_02_01', '-0.0555397950953069', '3.97924278890843']
```
#### PureCN
```
['chr6', '13159954', '29441206', 'p', '3', '0', 'LOH']
['chr6', '29461518', '29726112', 'p', '4', '0', 'LOH']
['chr6', '29726113', '30984271', 'p', '5', '0', 'LOH']
['chr6', '30985985', '32442939', 'p', '3.81130895846539', '0', 'LOH']
['chr6', '32442940', '35797540', 'p', '5', '1', '']
```
#### TitanCNA
```
['chr6', '24290975', '29829919', '4', '0', '4', 'ALOH']
['chr6', '29942559', '29975228', '8', '3', '5', 'UBCNA']
['chr6', '30068694', '32222613', '4', '0', '4', 'ALOH']
['chr6', '32293730', '32460064', '5', '1', '4', 'ASCNA']
['chr6', '32519398', '32519532', '7', '3', '4', 'UBCNA']
['chr6', '32519561', '35787881', '5', '1', '4', 'ASCNA']
```
#### GATK CNV
```
chr6	13159954	29441206	670	-0.127840	0
chr6	29461518	29726112	47	0.041316	0
chr6	29726113	30984271	284	0.241001	+
chr6	30985985	32043949	454	-0.004173	0
chr6	32045925	32442939	163	0.043453	0
chr6	32442940	35797540	594	0.250982	+
```
#### CNVkit
```
['chr6', '26246678', '32299938', '2', '2', '0']
['chr6', '32300677', '35797290', '3', '3', '0']
```
