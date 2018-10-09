import sys
from bcbio.variation import validateplot

title="smCounter2 UMI: VarDict 1.5.6; octopus 0.5.1b"
validateplot.classifyplot_from_valfile(sys.argv[1], outtype="png", title=title)
