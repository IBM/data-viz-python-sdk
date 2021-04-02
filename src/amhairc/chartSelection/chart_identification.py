# -*- coding: utf-8 -*-
"""
Created: 2020-11-12
Updated: 2021-03-04
Python: 3.7
@author: EddPineda
Version: 1.0.3

The attributes and their purpose for the class are:
    kct          - the column data type for the used data frame columns as a list of strings
    sortThres    - since there are different sort algorithms used that differ in sorting
                   special characters, a workaround was needed to account for data
                   is sorted from a human point of view - the sortThres is the variance
                   limit for the data to be considered sorted as a float
    grphThres    - the maximum number of features on a single plot as a int
    outlierThres - float to determine the line for outliers as a float (ex 2.698 2 standard deviations - normal distribution)
    lenThres     - number of observations in a dataset - histogram limits as int
    binRng       - bin range ex 1 to 11 - again for histogram limits tuple length of 2
    binSzF       - formula for calculating the bin size (ex: Freedman–Diaconis, Square-root choice {used by Excel}) as a string
    catVals      - the distinct list of chart data categories as a list of strings
    dtaCats      - a dictionary of data types and their category
    attCols      - dataframe attribute names as a list of strings
    attAddlCols  - additional dataframe attributes as a list of strings
    dfLen        - the length (number of rows) of the dataframe used for the chart default set to zero and updated in getDFattribs
    aggCols      - aggregate items that become the dataframe column names as a list of strings (should be ['sum', 'count'])
    sercat       - chart data categories and their "max" value before getting to gtn in the chart matrix as a dictionary
    opg          - values for opportunities per group as a list of strings
    pl           - user input list of categoric types as a list of strings
    ml           - used in conjunction with pl to get to chart matrix values for cattype as a list of strings
    ac           - column name for the about information for the top chart
    gt           - string value for the distinction of greater than in the chart matrix as a string
    cs           - the character used for separating the chart types in the chart matrix as a string
    msg          - the message set to chartType when the data doesn't align with a chart type in the chart matrix
    cd           - chart dictionary keys as a list

The methods for the class are:
    isSorted        - tests to see if feature (dataframe column) is sorted and takes the following parameters:
                      dta    - the dataframe column as a series
    stats           - creats stats for a feature (dataframe column) and takes the following parameters:
                      dta    - the dataframe column as a series
    getDFattribs    - the "parent" method for the stats method that handles the dataframe stats and takes the following parameters:
                      df     - dataframe
    getChartType    - the work horse function that selects the "best" chart (and the x axis) for the given
                      dataframe - the method returns the best charts as a pandas series, the column index as an integer
                      for the chart x axis and the criteria for the selected chart as a pandas dataframe:
                      df     - dataframe
"""

import pandas as pd
import numpy as np
import statistics
from enum import Enum

chartAbout = {"barplot":"<div style='width:70%;'><h3 style='margin-bottom:0px;'>Bar Chart</h3><div style='text-indent:10px;'><ul style='list-style-type:disc;'><li>A bar chart shows the relationship between a numeric and a categoric variable.</li><li>Each entity of the categoric variable is represented as a bar.</li><li>The size of the bar represents its numeric value.</li><li>It is versatile chart to display counts, proportions or parts of a whole.</li><li>A bar chart tells us about the numerical counts or proportions of data.</li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Notes</h4><ul style='list-style-type:disc;margin-top:5px;'><li>Sorting data from high to low (read left to right) improves readability</li><li>Using pre-attentive attributes to highlight key columns improves insights</li><li>For multiple columns use a maximum of five colours</li><li>For long category names flip the bar chart from vertical to horizontal</li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Alternatives</h4><p style='text-indent:25px;line-height:0px;'>Spider / Radar, Lollipop, Parallel</p></div></div>",
              "histogram":"<div style='width:70%;'><h3 style='margin-bottom:0px;'>Histogram</h3><div style='text-indent:10px;'><ul style='list-style-type:disc;'><li>Useful for plotting the dispersion of univariate data (one numerical variable) although can be used for plotting multi-variate (two or more numerical variables).</li><li>It is useful for the visualization of the distribution of data.</li><li>Histogram tells us about the skewness of data plotted.</li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Notes</h4><ul style='list-style-type:disc;margin-top:5px;'><li>The shape of the histogram is dependent on the size of the bar widths (also known as bins, blocks or breaks)</li><li>It can be difficult to compare whether to histograms are similar using only a visual inspection</li><li>The shape of the histogram is dependent on the chart aspect ratio (AR), therefore a chart AR of between 1.2 - 1.5 is recommended</li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Alternatives</h4><p style='text-indent:25px;line-height:0px;'>Boxplot, Density, Violin, Ridgeline</p></div></div>",
              "lineplot":"<div style='width:70%;'><h3 style='margin-bottom:0px;'>Lineplot (Time Series)</h3><div style='text-indent:10px;'><ul style='list-style-type:disc;'><li>Useful for plotting the dispersion of univariate data (one numerical variable) although can be used for plotting multi variate (two or more numerical variables).</li><li>A line chart is often used to visualize a trend in data over intervals of time - a time series - thus the line is often drawn chronologically.</li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Notes</h4><ul style='list-style-type:disc;margin-top:5px;'><li>When plotting multiple series it is best practice to display no more than five series on a single chart - Best practice is to facet (split series into multiple charts beside each other)</li><li>To improve chart readability and insights use pre-attentive elements such as line thickness, line dashing and colour to differentiate between series</li><li>The use of dual Y axis line charts is strongly discouraged and considered bad practice</li><li>The amount of the trend is dependent on the chart aspect ratio (AR), therefore a chart AR of between 1.5 - 1.75 is recommended</li><li>When plotting multiple series a line plot can display 'anti-patterns' known as a spurious correlation (i.e. two or more datasets look correlated but are independent)</li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Alternatives</h4><p style='text-indent:25px;line-height:0px;'>Area, Stacked Area, Streamchart</p></div></div>",
              "scatterplot":"<div style='width:70%;'><h3 style='margin-bottom:0px;'>Scatterplot</h3><div style='text-indent:10px;'><ul style='list-style-type:disc;'><li>Useful for plotting the relationship of multi variate (two or more numerical variables) data.</li><li>With the use of colour, multi-variate data can be displayed by 'subgroups'.</li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Notes</h4><ul style='list-style-type:disc;margin-top:5px;'><li>When working with grouped data, the readability of the chart is dependent on the chromatic distance (colour hue and intensity) between groups</li><li>When working with large data points, a scatterplot can be difficult to read if lots of points overlap (known as over-plotting)</li><li>The shape of the scatterplot is highly dependent on the chart aspect ratio (AR), therefore a chart AR of between 1.0 - 1.2 is recommended</li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Alternatives</h4><p style='text-indent:25px;line-height:0px;'>Heatmap, Correlogram, Bubble, 2D-Density</p></div></div>",
              "groupedscatter":"<div style='width:70%;'><h3 style='margin-bottom:0px;'>Scatterplot</h3><div style='text-indent:10px;'><ul style='list-style-type:disc;'><li>Useful for plotting the relationship of multi variate (two or more numerical variables) data</li><li>With the use of colour, multi variate data can be displayed by 'subgroups'</li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Notes</h4><ul style='list-style-type:disc;margin-top:5px;'><li>When working with grouped data, the readability of the chart is dependent on the chromatic distance (colour hue and intensity) between groups</li><li>When working with large data points, a scatterplot can be difficult to read if lots of points overlap (known as over-plotting)</li><li>The shape of the scatterplot is highly dependent on the chart aspect ratio (AR), therefore a chart AR of between 1.0 - 1.2 is recommended</li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Alternatives</h4><p style='text-indent:25px;line-height:0px;'>Heatmap, Correlogram, Bubble, 2D-Density</p></div></div>",
              "boxplot":"<div style='width:70%;'><h3 style='margin-bottom:0px;'>Boxplot</h3><div style='text-indent:10px;'><ul style='list-style-type:disc;'><li>A boxplot is used to display the dispersion between two or more numeric variables. The box is constructed as follows: The ends of each box are the upper and lower quartiles (25% and 75%) value. The central line is the median line (50% value).</li><li>The lines extending from each end of the box are known as the 'whiskers' and represent extreme but non-outlier values. Finally outliers (values most distant from the median) are represented by dots outside of box and whisker lines.</li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Notes</h4><ul style='list-style-type:disc;margin-top:5px;'><li>Boxplots can be arranged horizontally or vertically, it is a matter of preference.</li><li>In order to show both relative dispersion (between variables) and absolute dispersion (dispersion between a minimum value) the box plot numerical (typically Y) axis should start at 0.</li><li>If a boxplot chart starts at a non-zero value it will show relative dispersion (between variables), but absolution dispersion will be hidden, and this effect will distort the level of relative dispersion.</li><li>When plotting multiple variables in a single plot, it may be useful to order the variables by median value.</li><li>The visual display of dispersion of dependent on the chart aspect ratio, therefore an aspect ratio of 1:1.2 is recommended.</li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Alternatives</h4><p style='text-indent:25px;line-height:0px;'>Violin Plot</p></div></div>"}

cica = {'sortThres' : .05,
        'grphThres' : 7,
        'outlierThres' : 2.698,
        'lenThres' : 2000,
        'binRng' : (1, 11),
        'binSzF' : '(2 * (((np.percentile(dta.dropna(), 75, interpolation = \'midpoint\') - np.percentile(dta.dropna(), 25, interpolation = \'midpoint\'))) / (len(dta.dropna()) ** (1/3))))',  #Freedman–Diaconis
        'catVals' : ['categoric', 'numeric', 'timeseries', 'numcat'],
        'dtaCats' : {'text' : 'text',
                     'currency' : 'numeric',
                     'date' : 'timeseries',
                     'time' : 'timeseries',
                     'datetime' : 'timeseries',
                     'dtatetimestamp' : 'timeseries',
                     'name' : 'text',
                     'float' : 'numeric',
                     'intlfloat' : 'numeric',
                     'int' : 'numeric',
                     'intlint' : 'numeric',
                     'category' : 'categoric',
                     'indcategory' : 'categoric',
                     'nestcategory' : 'categoric',
                     'subcategory' : 'categoric',
                     'adjcategory' : 'categoric'
                     },
        'dfLen' : 0,
        'attCols' : ['column', 'sparsity', 'sparsity_pct', 'unique', 'unique_pct', 'col_typ', 'datacat', 'sorted'],
        'attAddlCols' : ['mean', 'median', 'max', 'min', 'var', 'stdev', 'binsize', 'bins'],
        'dfCM' : pd.read_csv('/opt/src/amhairc/chartSelection/decision_tree.csv').astype(object),
        'dCMT' : chartAbout,
        'aggCols' : ['sum', 'count'],
        'sercat' : {'timeseries' : 1, 'numeric' : 3, 'categoric' : 1, 'numcat' : 1},
        'opg' : ['gt1', '1'],
        'pl' : ['indcategory', 'nestcategory', 'subcategory', 'adjcategory'],
        'ml' : ['indpendent', 'nested', 'subgroup', 'adjacency'],
        'ac' : 'about', 'gt' : 'gt', 'cs' : ',',
        'msg' : 'The selected data columns do not align within current chart matrix.',
        'cd' : ['chartType', 'X', 'chartCriteria']}

class ChartType():

    HISTOGRAM = "histogram"
    LINEPLOT = "lineplot"
    SCATTERPLOT = "scatterplot"
    TIMESERIES = "timeSeries"
    BOXPLOT = "boxplot"
    BARPLOT = "barPlot"
    BUBBLEPLOT = "bubblePlot"
    DENDOGRAM = "dendogram"


class chartIdentification:
    def __init__(self, cv):
        self.__dict__.update(**cv)
        self.__dict__.update(**cica)
        print('chart identification class initiated')

    def __del__(self):
        print('chart identification class destroyed')

    def isSorted(self, dta):
        try:
            return (np.diff(dta) > 0).all()
        except:
            try:
                return (len([b for i, (a, b) in enumerate(zip(dta.str.lower(), dta.str.lower().sort_values())) if a != b]) / len(dta)) < self.sortThres
            except:
                return False

    def stats(self, dta): #re work based on call comment below
        try:
            binSz = eval(self.binSzF)
            return statistics.mean(dta), statistics.median(dta), max(dta), min(dta), statistics.pvariance(dta), statistics.stdev(dta), binSz, int(round((max(dta.dropna()) - min(dta.dropna())) / binSz, 0))
        except:
            return tuple(None for _ in range(len(self.attAddlCols)))

    def getDFattribs(self, df):
        self.dfLen = len(df)
        dfStat = pd.DataFrame(df.isnull().sum(axis = 0).reset_index())
        dfStat.columns = self.attCols[:2]
        dfStat[self.attCols[2]] = dfStat[self.attCols[1]] / self.dfLen
        dfStat = dfStat.join(pd.DataFrame(df.nunique(dropna=False, axis=0).reset_index(drop=True),
                                          columns=[self.attCols[3]]))
        dfStat[self.attCols[4]] = dfStat[self.attCols[3]] / self.dfLen
        dfStat[self.attCols[5]] = self.kct
        dfStat[self.attCols[6]] = [self.dtaCats[k] for k in list(dfStat[self.attCols[5]])]
        dfStat[self.attCols[7]] = [self.isSorted(df[c]) for c in df.columns]

        return dfStat.join(pd.DataFrame([self.stats(df[df[c].notnull()][c])
                                         if dfStat[self.attCols[6]][i] == self.catVals[1]
                                         else tuple(None for _ in range(len(self.attAddlCols))) for i, c in enumerate(dfStat[self.attCols[0]])],
                                        columns=self.attAddlCols))

    def getChartType(self, df, ct):
        dfj = 'inner'
        x = 0

        # summarize and consolidate the "stats" df from the getAttribs method to "match" to the chart matrix
        dfSum = df[self.attCols[-2:]].groupby(
            [df.columns[6]])[df.columns[7]].agg([(self.aggCols[0]),
                                                 (self.aggCols[1])]).reset_index().rename(columns={self.aggCols[1]:self.dfCM.columns[1]})
        dfSum.loc[((dfSum[self.dfCM.columns[0]] == self.catVals[1]) &
                   (dfSum[dfSum[self.dfCM.columns[0]] == self.catVals[1]][self.dfCM.columns[1]] > 1)),
                  self.dfCM.columns[3]] = (dfSum.loc[((dfSum[self.dfCM.columns[0]] == self.catVals[1]) &
                                                      (dfSum[dfSum[self.dfCM.columns[0]] == self.catVals[1]][self.dfCM.columns[1]] > 1))][self.aggCols[0]]) if (self.catVals[2] not in list(dfSum[self.dfCM.columns[0]])) and (sum(df[df[self.dfCM.columns[0]] == self.catVals[0]][df.columns[4]]) != 1) else None
        dfSum.drop(self.aggCols[0], axis = 1, inplace = True)
        dfSum.loc[((dfSum[self.dfCM.columns[0]] == self.catVals[1]) &
                   (dfSum[self.dfCM.columns[1]] == 2)), self.dfCM.columns[4]] = int(self.dfLen > self.lenThres)
        dfSum.loc[((sorted(dfSum[self.dfCM.columns[0]])[:2] == self.catVals[:2]) &
                   (dfSum[self.dfCM.columns[0]] == self.catVals[0]) &
                   pd.isnull(dfSum[dfSum[self.dfCM.columns[0]] == self.catVals[1]][self.dfCM.columns[3]].values[0] if self.catVals[1] in list(dfSum[self.dfCM.columns[0]]) else np.NaN)), self.dfCM.columns[5]] = self.opg[int(sum(df[df[df.columns[6]] == self.catVals[0]][df.columns[4]]) == 1)]
        dfSum.loc[(dfSum[self.dfCM.columns[0]] == self.catVals[0]) &
                  (dfSum[self.dfCM.columns[1]] > self.sercat[dfSum[self.dfCM.columns[0]][0]]),
                  self.dfCM.columns[6]] = self.ml[self.pl.index(list(set(df[df.columns[5]]) &
                                                                     set(self.pl[int(len(dfSum) > 1):]))[0])] if len(list(set(df[df.columns[5]]) & set(self.pl[int(len(dfSum) > 1):]))) else None
        dfSum.loc[(dfSum[self.dfCM.columns[0]] == self.catVals[0]) &
                  (sorted(dfSum[self.dfCM.columns[0]])[:2] == self.catVals[:2]),
                  self.dfCM.columns[2]] = self.opg[int(dfSum.loc[(dfSum[self.dfCM.columns[0]] == self.catVals[0])][self.dfCM.columns[1]] == 1)] if (sorted(dfSum[self.dfCM.columns[0]])[:2] == self.catVals[:2]) else None
        dfSum.loc[((dfSum[self.dfCM.columns[0]] == self.catVals[0]) &
                   (sorted(dfSum[self.dfCM.columns[0]])[:2] == self.catVals[:2])) |
                  (dfSum[self.dfCM.columns[0]] == self.catVals[2]), self.dfCM.columns[1]] = None
        dfSum = dfSum[self.dfCM.columns[:-1]].astype(object)

        # from the 3 main categories of charts at time of writing, select the chart(s) based on the "match" to the matrix
        # also identify the x column for the plot
        if self.catVals[2] in list(dfSum[self.dfCM.columns[0]]): #timeseries
            dfC = dfSum.loc[[(dfSum[self.dfCM.columns[0]].values == self.catVals[2]).argmax()]].reset_index(drop=True)
            dfC[self.dfCM.columns[1]] = int(float(dfSum[self.dfCM.columns[1]][(dfSum[self.dfCM.columns[0]].values != self.catVals[2]).argmax()]))
            x = (df[df.columns[6]].values == self.catVals[2]).argmax()
        elif sorted(dfSum[self.dfCM.columns[0]])[:2] == self.catVals[:2]: #numcat
            dfC = dfSum.loc[[(dfSum[self.dfCM.columns[0]].values == self.catVals[0]).argmax()]].reset_index(drop=True)
            dfC[self.dfCM.columns[1]] = int(dfSum[dfSum[self.dfCM.columns[0]] == self.catVals[1]][self.dfCM.columns[1]])
            dfC[self.dfCM.columns[3]] = int(dfSum[dfSum[self.dfCM.columns[0]] == self.catVals[1]][self.dfCM.columns[3]]) if pd.notnull(dfSum[dfSum[self.dfCM.columns[0]] == self.catVals[1]][self.dfCM.columns[3]].values[0]) else np.NaN
            dfC[self.dfCM.columns[0]] = self.catVals[3]
            x = min(df[(df[df.columns[6]].values == self.catVals[1]) &
                       (df[df.columns[7]].values == True)].index) if True in list(df[df[df.columns[6]] == self.catVals[1]][self.dfCM.columns[3]]) else (df[df.columns[6]].values == self.catVals[0]).argmax()
        else: #everything else
            dfC = dfSum.copy()
            dfC[self.dfCM.columns[1]] = int(float(dfC[self.dfCM.columns[1]]))
            x = min(df[(df[df.columns[7]].values == True)].index) if True in list(df[self.dfCM.columns[3]]) else 0

        dfC[self.dfCM.columns[1]] = self.gt + str(self.sercat[dfC[self.dfCM.columns[0]][0]]) if dfC[self.dfCM.columns[1]][0] > self.sercat[dfC[self.dfCM.columns[0]][0]] else str(dfC[self.dfCM.columns[1]][0])
        dfC = dfC.astype(object)
        srsC = pd.Series(pd.merge(dfC, self.dfCM, on=list(dfC.columns), how=dfj)[self.dfCM.columns[7]][0].split(self.cs)) if len(pd.merge(dfC, self.dfCM, on=list(dfC.columns), how=dfj)) > 0 else pd.Series(self.msg)
        dfC[self.ac] = self.dCMT.get(srsC[0])

        return {self.cd[0] : Enum(ct, dict((e.upper(), e) for e in srsC)), self.cd[1] : x, self.cd[2] : dfC}
