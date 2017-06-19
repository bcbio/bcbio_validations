import sys
from bcbio.variation import validateplot

title="NA24385 10x data: trimming + low AF, quality, read position filter"
validateplot.classifyplot_from_valfile(sys.argv[1], outtype="png", title=title)
