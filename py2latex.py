'''Py2LaTeX Widget'''
'''Convert Pandas DataFrames to LaTeX threeparttable'''
'''Requirements: Pandas'''

import pandas as pd

class latexTable:
    '''Class to control the threeparttable'''
    
    def __init__(self,df,title,label,columns=None,index=True,ixTitle=None,precision=3,threeparttable=False,sideways=False):
        self.output=[]
        if columns==None: columns = df.columns
        if sideways:
                self._makeSidewaysHeader(index,title,label,columns,tpt=threeparttable)
        else: self._makeHeaderReg(index,title,label,df.shape[1])
        self._makeColHeader(columns,ixTitle)
        self._fillTable(df,index,precision)
        self._endTable(threeparttable,sideways)
    
    def _makeHeaderReg(self,index,title,label,cols):
        self.output.append('\\begin{table}[H]')
        self.output.append('\\centering')
        self.output.append('\\caption{%s} \\label{%s}'%(title,label))
        r = ''.join(['r' for x in cols])
        if index: r = 'l'+r
        self.output.append('\\begin{tabular}{%s}'%(r))
        
    def _makeSidewaysHeader(self,index,title,label,cols,tpt=False):
        self.output.append('\\being{sidewaystable}')
        self.output.append('\\centering')
        self.output.append('\\scalebox{0.6}{')
        if tpt: self.output.append('\\begin{threeparttable}')
        self.output.append('\\caption{%s} \\label{%s}'%(title,label))
        r = ''.join(['r' for x in cols])
        if index is not None: r = 'l'+r
        self.output.append('\\begin{tabular}{%s}'%(r))
        
    def _makeColHeader(self, columns,ixTitle):
        """Adds the column headings - can be specified extra
        requires: column headings"""
        self.output.append('\\toprule')
        if columns is not None:
            header = ''.join(['{%s & }'%col for col in columns])
        else:
            header = ''.join(['{%s & }'%col for col in self.df.columns])
        if ixTitle is not None: header = '{%s} &'%ixTitle + header + '\\\\'
        self.output.append(header)
        self.output.append('\\midrule')
    
    def _fillTable(self,df,index,precision):
        """Fill the table with data from the dataframe"""
        for i in range(df.shape[0]):
            newrow =''
            if index: newrow+='\\textbf{%s} & '%df.index[i]
            for j in range(df.shape[1]):
                val = df.iloc[i,j]
                if precision is not None: val = round(val, precision)
                newrow+='{} & '.format(val) 
            self.output.append(newrow[:-2] + '\\\\')
        #End of table format
        self.output.append('\\bottomrule')
        self.output.append('\\end{tabular}')  
    
    def _endTable(self,threeparttable,sidewaystable):
        if threeparttable:
            self.output.append('\\begin{tablenotes}')
            self.output.append('\\end{tablenotes}')
            self.output.append('\\end{threeparttable}')
        if sidewaystable:
            self.output.append('}')
            self.output.append('\\end{sidewaystable}')
            
        self.output.append('\\end{table}')
        
    def export(self,label):
        """Export dataframe as latex file to use easily. 
        Require file name, e.g. 'tab:results' with or with .tex to end"""
        if label[-4:]!='.tex':label=label+'.tex'
        with open(label,'w') as f:
            f.write('\n'.join(self.output))
            f.close()
