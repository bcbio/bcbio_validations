import sys
from bcbio.variation import validateplot

title="CHM and NA12878 validation: exome + chr20"
validateplot.classifyplot_from_valfile(sys.argv[1], outtype="png", title=title)
