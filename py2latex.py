'''Py2LaTeX Widget'''
'''Convert Pandas DataFrames to LaTeX threeparttable'''
'''Requirements: Pandas'''

import pandas as pd
from collections import Counter

class latexTable:
    '''Class to control the threeparttable'''

    def __init__(self,df,title,label,columns=None,index=True,ixTitle=None,precision=3,threeparttable=False,sideways=False,nanfill=''):
        self.output=[]
        self.nanfill=nanfill
        if columns==None: columns = df.columns
        if sideways:
                self._makeSidewaysHeader(index,title,label,columns,tpt=threeparttable)
        else: self._makeHeaderReg(index,title,label,df.columns.to_list(),tpt=threeparttable)
        if isinstance(df.columns,pd.core.indexes.multi.MultiIndex):
            print("Multi Test:\t",isinstance(df.columns,pd.core.indexes.multi.MultiIndex))
            self._makeMultiColHeader(columns,ixTitle)
        else: self._makeColHeader(columns,ixTitle)
        self._fillTable(df,index,precision)
        self._endTable(threeparttable,sideways)

    def _makeHeaderReg(self,index,title,label,cols,tpt):
        self.output.append('\\begin{table}[H]')
        self.output.append('\\centering')
        if tpt: self.output.append('\\begin{threeparttable}')
        self.output.append('\\caption{%s} \\label{%s}'%(title,label))
        r = ''.join(['r' for x in cols])
        if index: r = 'l'+r
        self.output.append('\\begin{tabular}{%s}'%(r))

    def _makeSidewaysHeader(self,index,title,label,cols,tpt=False):
        self.output.append('\\begin{sidewaystable}')
        self.output.append('\\centering')
        self.output.append('\\scalebox{0.6}{')
        if tpt: self.output.append('\\begin{threeparttable}')
        self.output.append('\\caption{%s} \\label{%s}'%(title,label))
        r = ''.join(['r' for x in cols])
        if index is not None: r = 'l'+r
        self.output.append('\\begin{tabular}{%s}'%(r))

    def _makeColHeader(self,columns,ixTitle):
        """Adds the column headings - can be specified extra
        requires: column headings"""
        self.output.append('\\toprule')
        header=''.join(['{%s} & '%col for col in columns])
        if ixTitle is not None: header = '{%s} &'%ixTitle + header
        else: header = '&'+header
        self.output.append(header[:-2] + '\\\\')
        self.output.append('\\midrule')

    def _makeMultiColHeader(self,micols,ixTitle):
        """Adds the column headings based on multi-column - can be specified extra
            adds a cmidrule for all the main headings
        requires: column headings"""

        # Mini functions to reduce repetition
        mc = lambda x: "\\multicolumn{{{}}}{{c}}{{{}}}".format(x[0],x[1])
        def rules(counts):
            midrule = lambda x: "\\cmidrule(lr){{{}-{}}}".format(x[0],x[1])
            return [midrule([2+sum(counts[:j]),1+sum(counts[:j+1])]) for j in range(len(counts))]

        # Get first level headings
        self.output.append('\\toprule')
        counts = dict(Counter(ix[0] for ix in micols))
        header = [mc([counts[col],"\\textbf{{{}}}".format(str(col))]) for col in counts]
        self.output.append('&'+'&'.join(header)+'\\\\')
        self.output.append(''.join(rules([counts[col] for col in counts])))

        supraHeadList = list(dict.fromkeys([ix[0] for ix in micols]))
        supraHeadList = [[x] for x in supraHeadList]
        # Sublevel headings
        for sublevel in range(1,len(micols.levels)):
            # Order preserved list of unique col supraheads
            unique=list(dict.fromkeys([ix[sublevel-1] for ix in micols]))
            # First level is already included
            if sublevel==1: priors = [tuple(i,) for i in supraHeadList]
            # Priors is tuple of supra headings that must be matched
            else: priors = [(*i,j) for i in supraHeadList for j in unique]
            tempHeader = []
            subcount = []
            for supraHead in priors:
                counts = dict(Counter(ix[sublevel] for ix in micols if ix[:sublevel]==supraHead))
                header = [mc([counts[col],col]) for col in counts]
                subcount.extend([counts[col] for col in counts])
                tempHeader.append('&'.join(header))
            self.output.append('&'+'&'.join(tempHeader)+'\\\\')
            if sublevel != len(micols.levels)-1:
                print([counts[col] for col in counts])
                self.output.append(''.join(rules(subcount)))

        # Put everything together
        if ixTitle is not None: self.output[-1] = '{%s} &'%ixTitle + self.output[-1][1:]
        self.output.append('\\midrule')

    def _fillTable(self,df,index,precision):
        """Fill the table with data from the dataframe"""
        nans = df.isna()
        for i in range(df.shape[0]):
            newrow =''
            if index: newrow+='\\textbf{%s} & '%df.index[i]
            for j in range(df.shape[1]):
                if nans.iloc[i,j]:val=self.nanfill
                else:
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
            self.output.append('\\item')
            self.output.append('\\end{tablenotes}')
            self.output.append('\\end{threeparttable}')
        if sidewaystable:
            self.output.append('}')
            self.output.append('\\end{sidewaystable}')
        else: self.output.append('\\end{table}')

    def export(self,label):
        """Export dataframe as latex file to use easily.
        Require file name, e.g. 'tab:results' with or with .tex to end"""
        if label[-4:]!='.tex':label=label+'.tex'
        with open(label,'w') as f:
            f.write('\n'.join(self.output))
            f.close()
