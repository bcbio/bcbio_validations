#!/bin/bash

#bcftools query -i 'FILTER="PASS" && SVTYPE="DEL"' -f '%CHROM\t%POS\t%END\n' metasv.vcf.gz | grep -v GL > metasv.DEL.bed

bname=`basename $1 .bed`

cat $1 | awk '{len=$3-$2+1;if(len<100) print $0;}' > $bname.100.bed
cat $1 | awk '{len=$3-$2+1;if(len>=100 && len<450) print $0;}' > $bname.450.bed
cat $1 | awk '{len=$3-$2+1;if(len>=450 && len<2000) print $0;}' > $bname.2000.bed
cat $1 | awk '{len=$3-$2+1;if(len>=2000 && len<4000) print $0;}' > $bname.4000.bed
cat $1 | awk '{len=$3-$2+1;if(len>=4000 && len<20000) print $0;}' > $bname.20000.bed
cat $1 | awk '{len=$3-$2+1;if(len>=20000 && len<60000) print $0;}' > $bname.60000.bed
cat $1 | awk '{len=$3-$2+1;if(len>=60000 && len<1000000) print $0;}' > $bname.1000000.bed


for size in {100,450,2000,4000,20000,60000,1000000}
do
    echo $size `cat $bname.$size.bed | wc -l` `bedtools intersect -f 0.5 -F 0.5 -wa -a $bname.$size.bed -b HuRef.SV.merged.$2.$size.bed | wc -l`
done
