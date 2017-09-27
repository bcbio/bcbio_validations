import sys
from bcbio.variation import validateplot

title="NA12878/NA24385 somatic like mixture"
validateplot.classifyplot_from_valfile(sys.argv[1], outtype="png", title=title)
