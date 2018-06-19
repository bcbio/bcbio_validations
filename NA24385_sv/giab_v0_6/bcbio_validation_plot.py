import sys
from bcbio.variation import validateplot

title="NA24385 GiaB germline structural variants: v0.6"
validateplot.classifyplot_from_valfile(sys.argv[1], outtype="png", title=title)
