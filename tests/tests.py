from py2latex import py2latex as ltx
import pandas as pd
import numpy as np


data = np.arange(30).reshape((10,3))
test_df = pd.DataFrame(data,columns=['A','B','C'])

x = ltx.latexTable(test_df,"Test",'tab:test',threeparttable=True,sidewaystable=True)
x.export('tab:test.tex')

