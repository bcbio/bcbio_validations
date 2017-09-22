import sys
from bcbio.variation import validateplot

title="GATK4 joint calling hg38"
validateplot.classifyplot_from_valfile(sys.argv[1], outtype="png", title=title)
