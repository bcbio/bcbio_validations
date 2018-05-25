import sys
from bcbio.variation import validateplot

title="Pisces NA12878/NA12877 titration series"
validateplot.classifyplot_from_valfile(sys.argv[1], outtype="png", title=title)
