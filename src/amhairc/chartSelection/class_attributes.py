# -*- coding: utf-8 -*-
"""
Created: 2021-02-11
Updated:
Python: 3.7
@author: EddPineda
Version: 1.0
"""
#chartIdentification
import pandas as pd

chartAbout = {"barplot":"<div style='width:70%;'><h3 style='margin-bottom:0px;'>Bar Chart</h3><div style='text-indent:10px;'><ul style='list-style-type:disc;'><li>A bar chart shows the relationship between a numeric and a categoric variable -  Each entity of the categoric variable is represented as a bar - The size of the bar represents its numeric value.</li><li>It is versatile chart to display counts, proportions or parts of a whole</li><li>A bar chart tells us about the numerical counts or proportions of data</li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Notes</h4><ul style='list-style-type:disc;margin-top:5px;'><li>Sorting data from high to low (read left to right) improves readability</li><li>Using pre-attentive attributes to highlight key columns improves insights</li><li>For multiple columns use a maximum of five colours</li><li>For long category names flip the bar chart from vertical to horizontal</li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Alternatives</h4><p style='text-indent:25px;line-height:0px;'>Spider / Radar, Lollipop, Parallel</p></div></div>",
              "histogram":"<div style='width:70%;'><h3 style='margin-bottom:0px;'>Histogram</h3><div style='text-indent:10px;'><ul style='list-style-type:disc;'><li>Useful for plotting the dispersion of univariate data (one numerical variable) although can be used for plotting multi variate (two or more numerical variables)</li><li>It is useful for the visualization of the distribution of data</li><li>Histogram tells us about the skewness of data plotted</li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Notes</h4><ul style='list-style-type:disc;margin-top:5px;'><li>The shape of the histogram is dependent on the size of the bar widths (also known as bins, blocks or breaks)</li><li>It can be difficult to compare whether to histograms are similar using only a visual inspection</li><li>The shape of the histogram is dependent on the chart aspect ratio (AR), therefore a chart AR of between 1.2 - 1.5 is recommended</li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Alternatives</h4><p style='text-indent:25px;line-height:0px;'>Boxplot, Density, Violin, Ridgeline</p></div></div>",
              "lineplot":"<div style='width:70%;'><h3 style='margin-bottom:0px;'>Lineplot (Time Series)</h3><div style='text-indent:10px;'><ul style='list-style-type:disc;'><li>Useful for plotting the dispersion of univariate data (one numerical variable) although can be used for plotting multi variate (two or more numerical variables)</li><li>A line chart is often used to visualize a trend in data over intervals of time – a time series – thus the line is often drawn chronologically/li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Notes</h4><ul style='list-style-type:disc;margin-top:5px;'><li>When plotting multiple series it is best practice to display no more than five series on a single chart - Best practice is to facet (split series into multiple charts beside each other)</li><li>To improve chart readability and insights use pre-attentive elements such as line thickness, line dashing and colour to differentiate between series</li><li>The use of dual Y axis line charts is strongly discouraged and considered bad practice</li><li>The amount of the trend is dependent on the chart aspect ratio (AR), therefore a chart AR of between 1.5 - 1.75 is recommended</li><li>When plotting multiple series a line plot can display 'anti-patterns' known as a spurious correlation (i.e. two or more datasets look correlated but are independent)</li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Alternatives</h4><p style='text-indent:25px;line-height:0px;'>Area, Stacked Area, Streamchart</p></div></div>",
              "scatterplot":"<div style='width:70%;'><h3 style='margin-bottom:0px;'>Scatterplot</h3><div style='text-indent:10px;'><ul style='list-style-type:disc;'><li>Useful for plotting the relationship of multi variate (two or more numerical variables) data</li><li>With the use of colour, multi variate data can be displayed by 'subgroups'</li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Notes</h4><ul style='list-style-type:disc;margin-top:5px;'><li>When working with grouped data, the readability of the chart is dependent on the chromatic distance (colour hue and intensity) between groups</li><li>When working with large data points, a scatterplot can be difficult to read if lots of points overlap (known as over-plotting)</li><li>The shape of the scatterplot is highly dependent on the chart aspect ratio (AR), therefore a chart AR of between 1.0 - 1.2 is recommended</li></ul></div><div style='text-indent:10px;'><h4 style='margin-bottom:0px;margin-top:0px;'>Alternatives</h4><p style='text-indent:25px;line-height:0px;'>Heatmap, Correlogram, Bubble, 2D-Density</p></div></div>"}

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
        'dfCM' : pd.read_csv('../db/decision_tree.csv').astype(object),
        'dCMT' : chartAbout,
        'aggCols' : ['sum', 'count'],
        'sercat' : {'timeseries' : 1, 'numeric' : 3, 'categoric' : 1, 'numcat' : 1},
        'opg' : ['gt1', '1'],
        'pl' : ['indcategory', 'nestcategory', 'subcategory', 'adjcategory'],
        'ml' : ['indpendent', 'nested', 'subgroup', 'adjacency'],
        'ac' : 'about', 'gt' : 'gt', 'cs' : ',',
        'msg' : 'The selected data columns do not align within current chart matrix.'}