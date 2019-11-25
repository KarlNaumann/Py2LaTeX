'''Py2LaTeX Widget'''
'''Convert Pandas DataFrames to LaTeX threeparttable'''
'''Requirements: Pandas'''

import pandas as pd

class latexTable:
    '''Class to control the threeparttable'''
    
    def __init__(self,df,title,label,index=False):
        self.title = title
        self.label = df.index.tolist()
        self.rows,self.cols = df.shape
        self.index = index
        self.df = df
    
    def _beginTable(self):
        self.output = []
        self.output.append('\\begin{table}[H]')
        self.output.append('\\centering')
        self.output.append('\\caption{%s} \\label{%s}'%(title,label))
        r = ''.join(['r' for x in range(self.cols)])
        if self.index: r = 'l'+r
        self.output.append('\\begin{tabular}{%s}'%(r))
        
    def _header(self,header=False,indexTitle=False):
        if header:
            header = ''.join(['{%s & }'%col for col in header])
        else:
            header = ''.join(['{%s & }'%col for col in self.df.columns])
        if indexTitle: header = '{%s} &'%indexTitle + header
        self.output.append(header)

        def latex_table(df,title,label,indexTitle='',save=True,precision=None,index=True,verbose=False):
            output=[]
            #Basic beginning structure of the LaTeX matrix
            output.append('\\begin{table}[H]')
            output.append('\\centering')
            output.append('\\caption{%s} \\label{%s}'%(title,label[:-4]))
            #Formatting the alignment of the LaTeX matrix
            rows,cols = df.shape
            r = ''.join(['r' for x in range(len(df.columns))])
            if index: r = 'l'+r
            output.append('\\begin{tabular}{%s}'%(r))
            #Header row
            header=''
            if index: header+='{%s} &'%indexTitle
            for col in df.columns:
                header += '%s &'%col
            #Delete the last '&' and put '\\'
            output.append(header[:-2]+'\\\\')
            output.append('\\midrule')
            #Body of the table
            for i in range(rows):
                newrow =''
                if index: newrow+='\\textbf{%s} & '%df.index[i]
                for j in range(cols):
                    val = df.iloc[i,j]
                    if precision is not None: val = round(val, precision)
                    newrow+='{} & '.format(val) 
                output.append(newrow[:-2] + '\\\\')
            #End of table format
            output.append('\\bottomrule')
            output.append('\\end{tabular}')  
            output.append('\\end{table}') 
            #write the table to a file
            if save:
                with open(label,'w') as f:
                    f.write('\n'.join(output))
                    f.close()
            if verbose: print('\n'.join(output),'\n')
            #return string of the latex output
            return output