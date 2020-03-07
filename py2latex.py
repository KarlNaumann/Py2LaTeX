"""Py2LateX Widget
@ Author: Karl Naumann
@ GitHub: KarlNaumann
"""

import pandas as pd
from collections import Counter

class latexTable:
    '''Class to control the latex table creation

	Parameters
	---------------
	df 				required 	pandas dataframe of data for the table
	title 			required	(str) title of the table e.g. "Descriptive Statistics"
	label 			required 	(str) label for the title e.g. "tab:descriptive"
	columns			optional	(list fo str) list of strings serving as alternate
									column names must be the same length as the
									number of columns
	index 			optional	(boolean, default=True) will add the
									index to the table as far left column
	ixTitle			optional	(str, default=None) optional title for the index
	precision		optional	(int, default=3) precision of the rounded data
	threeparttable	optional	(boolean, default=False) whether to use
									threeparttable latex class
	sideways 		optional	(boolean, default=False) whether the table
									should be rotated sideways
	nanfill 		optional	(default='') what to fill the NaN values with,
									defaulting to not printing them

	Methods
	---------------
	export(self,filepath)		export the generated table as a .tex file at the given filepath
    '''

    def __init__(self,df,title,label,columns=None,index=True,ixTitle=None,precision=3,
    				threeparttable=False,sideways=False,nanfill=''):

        # Input checks
        assert isinstance(df,pd.DataFrame), "Input is data must be of pandas DataFrame class"

        if columns is not None:
        	assert len(columns) == df.shape[1],
        		"Columns length {} != data shape {}".format(len(columns),df.shape[1])
        	self.columns = columns
        else: self.columns = df.columns

        # Setup output
        self.output=[]

        # Setup given parameters
        self.title = title
        self.label = label
        self.index = index
        self.ixTitle = ixTitle
        self.precision = precision
        self.threeparttable	= threeparttable
        self.sideways = sideways
        self.nanfill = nanfill

        # Generate the table
        self._makeTableHeader()

        # Generate a multicolumn header if necessary
        if isinstance(df.columns,pd.core.indexes.multi.MultiIndex):
            self._makeMultiColHeader(columns,ixTitle)
            self.multicols = True
        else: self._makeColHeader(columns,ixTitle)

        # Generate table
        self._fillTable(df,index,precision)
        self._endTable(threeparttable,sideways)

        # Generate package requirements
        self.requirements = self._makeRequirements()

    def _makeTableHeader(self):
    	""" Make the table header, adjusting for the table being sideways or
    		a threeparttable
    		"""
    	if self.sideways:
    		self.output.append('\\begin{sidewaystable}')
        	self.output.append('\\centering')
        	self.output.append('\\scalebox{0.6}{')
        else:
        	self.output.append('\\begin{table}[H]')
        	self.output.append('\\centering')

        if self.threeparttable: self.output.append('\\begin{threeparttable}')

        self.output.append('\\caption{%s} \\label{%s}'%(self.title,self.label))

        # Right aligned columns and Left aligned index
        r = ''.join(['r' for x in self.columns])
        if self.index: r = 'l'+r
        self.output.append('\\begin{tabular}{%s}'%(r))

    def _makeColHeader(self):
        """Adds the column headings, and optionally the index heading"""
        self.output.append('\\toprule')
        header=''.join(['{%s} & '%col for col in self.columns])
        if self.ixTitle is not None: header = '{%s} &'%ixTitle + header
        else: header = '&'+header
        self.output.append(header[:-2] + '\\\\')
        self.output.append('\\midrule')

    def _makeMultiColHeader(self):
        """Adds the column headings based on multi-column - can be specified extra
            adds a cmidrule for all the main headings
        requires: column headings"""

        def rules(counts):
        	"""generates a set of midrules for given col widths"""
        	# Generate startend list first, then make midrules
        	locations = [[2+sum(counts[:j]),1+sum(counts[:j+1])] for j in range(len(counts))]
            return ["\\cmidrule(lr){{{}-{}}}".format(x[0],x[1]) for x in locations]

        # Get first level headings
        self.output.append('\\toprule')
        counts = dict(Counter(ix[0] for ix in self.columns))
        header = ["\\multicolumn{{{}}}{{c}}{{{}}}".format(counts[col],"\\textbf{{{}}}".format(str(col))) for col in counts]
        self.output.append('&'+'&'.join(header)+'\\\\')
        self.output.append(''.join(rules([counts[col] for col in counts])))

        supraHeadList = list(dict.fromkeys([ix[0] for ix in self.columns]))
        supraHeadList = [[x] for x in supraHeadList]
        # Sublevel headings
        for sublevel in range(1,len(self.columns.levels)):
            # Order preserved list of unique col supraheads
            unique=list(dict.fromkeys([ix[sublevel-1] for ix in self.columns]))
            # First level is already included
            if sublevel==1: priors = [tuple(i,) for i in supraHeadList]
            # Priors is tuple of supra headings that must be matched
            else: priors = [(*i,j) for i in supraHeadList for j in unique]
            tempHeader = []
            subcount = []
            for supraHead in priors:
                counts = dict(Counter(ix[sublevel] for ix in self.columns if ix[:sublevel]==supraHead))
                header = ["\\multicolumn{{{}}}{{c}}{{{}}}".format(counts[col],col) for col in counts]
                subcount.extend([counts[col] for col in counts])
                tempHeader.append('&'.join(header))
            self.output.append('&'+'&'.join(tempHeader)+'\\\\')
            if sublevel != len(self.columns.levels)-1:
                print([counts[col] for col in counts])
                self.output.append(''.join(rules(subcount)))

        # Put everything together
        if self.ixTitle is not None: self.output[-1] = '{%s} &'%self.ixTitle + self.output[-1][1:]
        self.output.append('\\midrule')

    def _fillTable(self,df,index,precision):
        """Fill the table with data from the dataframe"""
        nans = df.isna()
        for i in range(df.shape[0]):
            newrow =''
            if index: newrow+='\\textbf{%s} & '%df.index[i]
            for j in range(df.shape[1]):
                if nans.iloc[i,j]: val=self.nanfill
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

    def _makeRequirements(self):
    	"""Generate the requirements for the table based on used types"""
    	pass

    def export(self,filepath):
        """Export dataframe as latex file to use easily.
        Require file name, e.g. 'tab:results' with or with .tex to end"""
        if label[-4:]!='.tex':label=label+'.tex'
        with open(label,'w') as f:
            f.write('\n'.join(self.output))
            f.close()
