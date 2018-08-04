import sys
from bcbio.variation import validateplot

title="smCounter2 UMI low frequency: fgbio min-base-quality 40"
validateplot.classifyplot_from_valfile(sys.argv[1], outtype="png", title=title)
