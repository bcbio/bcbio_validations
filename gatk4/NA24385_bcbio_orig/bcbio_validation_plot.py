import sys
from bcbio.variation import validateplot

title="NA24385 10x data: GATK4, Sentieon Haplotyper"
validateplot.classifyplot_from_valfile(sys.argv[1], outtype="png", title=title)
