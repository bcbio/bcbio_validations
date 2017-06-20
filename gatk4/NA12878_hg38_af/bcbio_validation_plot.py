import sys
from bcbio.variation import validateplot

title="NA12878 hg38: low AF, quality, read position filter"

validateplot.classifyplot_from_valfile(sys.argv[1], outtype="png", title=title)
