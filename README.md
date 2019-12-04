# Py2LaTeX
Building a small class for exporting pandas DataFrames into LaTeX three-part-tables automatically

## Getting Started

Currently this project is in its infancy, hence download the py2latex.py file and add it to your current working directory. Then use `import py2latex` to get going.

### Prerequisites

Requires you have the latest pandas package installed

## Functions

```
Class LatexTable(df,title,label,columns=None,index=True,ixTitle=None,precision=3,threeparttable=False,sideways=False)
```

Parameter | Type | Description
----------|------|-------------
df | pd.DataFrame | DataFrame containing the data for the table, ideally with the index and columns already as desired (required)
title | string | Title of the desired Table (required)
label | string | Label for the desired Table (required)
columns | list | List of column titles to use, needs to be the same length as number of columns in dataframe (optional, default = None )
index | Boolean| Can choose to turn the index of the DataFrame off (optional, default = False)
ixTitle | String | Title for the index column (optional, default = None)
precision | int | Number of decimal places to round all values to (optional, default=3)
threeparttable | Boolean | Will ensure that the output is of the threeparttable variety, requires \usepackage{threeparttable} in LaTeX
sideways | Boolean | Will generate a sideways facing table with default scalebox of size 0.6

```LatexTable.export(label)```
This function takes a `String` label representing the desired filename for the .tex file. The function automatically adds .tex if not included in the filename. Exports to the current project directory

## To Be Added
- [ ] Raising errors and checks
- [ ] For regression results having *** for the p-values (perhaps a child class for OLS results)
- [ ] Child class for statsmodels OLS results
- [ ] Bold formatting for the titles

## Authors

* **Karl Naumann** - [GitHub](https://github.com/karlnaumann)
