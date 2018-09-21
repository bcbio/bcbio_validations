import sys
from bcbio.variation import validateplot

title="smCounter2 UMI: VarDict low frequency filters; fgbio min-reads 2"
validateplot.classifyplot_from_valfile(sys.argv[1], outtype="png", title=title)
