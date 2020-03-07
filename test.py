import pandas as pd
import numpy as np

import py2latex as lat
from collections import Counter

col_top = ['Reg 1','Reg 2','Reg 3']
col_bottom = ['coeff','tstat','pval']
col_tuple = [('Reg 1','coeff'),('Reg 1','tstat'),('Reg 2','coeff'),('Reg 2','tstat'),('Reg 3','coeff')]
micols = pd.MultiIndex.from_tuples(col_tuple)

micols = pd.MultiIndex.from_product([col_top,col_bottom,[1,2]], names=['Model', 'Results','Type'])
print(micols)
index = list(range(5))
test = pd.DataFrame(np.random.normal(0,1,size=(len(index),len(micols))),index=index,columns=micols)
temp = lat.latexTable(test,'title','label',threeparttable=True,sideways=True).export('tableTest.tex')