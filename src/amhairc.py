import src.amhairc.dataProcessing.data_processing as dp
# import src.amhairc.chartSelection.identify_chart as ic
import src.amhairc.chartSelection.chart_identification as cid
import src.amhairc.chartGeneration.generate_chart as gc

import logging

LOG_FILENAME = 'amhairc.out'
logging.basicConfig(filename=LOG_FILENAME,
                    level=logging.DEBUG,
                    )

""" TIMESERIES/ LINEPLOT """

DATA_FILE = "/opt/data/datafiles/data.csv"

COLS_SELECTED = ["Time","Outbound","Total_Outbound"]

# 1. Load and Process Data
data_definition = dp.DataDefinition(DATA_FILE,COLS_SELECTED)
df = data_definition.get_pandas_dataframe()
print(df.head())

kc = [0,2]
kct = ['date','float']

ds = dp.DataPreProcessing({'kc':kc,'kct':kct})
dfOut = ds.dataProcess(df)

data_to_process = dp.DataProcess(df)
print("3.", data_to_process.data_types_strings)

# 2. Chart Selection

ci = cid.chartIdentification({'kct':kct})

chartD = ci.getChartType(ci.getDFattribs(dfOut), 'chartType')

# the chart about text is in the about column of the chartCriteria dataframe
# chartType is a enum with the top chart choice "first"
# the full list
[print('?', '{:9} = {}'.format(c.name, c.value)) for c in chartD['chartType']]
#or the first item
chartD['chartType']._member_map_[list(chartD['chartType']._member_map_)[0]].value

#to retain the enum for the first item
print("4.", chartD['chartType']._member_map_[list(chartD['chartType']._member_map_)[0]])

#chart_selection = ic.ChartSelection(data_to_process.data_types_strings,COLS_SELECTED)

chartFound = chartD['chartType']._member_map_[list(chartD['chartType']._member_map_)[0]].value

# 3. Chart Generation

print("5.", dfOut)
print("6.", chartFound)
print("7. Number of series:", chartD['chartCriteria']['series'].values.tolist()[0])

print(dfOut)
print(chartFound)
print(str("Sample " + chartFound + " Plot"))

chartLocation = "/opt/data/chart_output/lineplot.html"

if str(chartD['chartCriteria']['about'][0]) != "None":
    about_str = chartD['chartCriteria']['about'][0]
else:
    about_str = ""

chart = gc.Chart(chartD, chartFound, dfOut, 700, 400, about_str,chartLocation)

######################

""" SCATTERPLOT """

DATA_FILE = "/opt/data/datafiles/scatterplot_data.csv"
COLS_SELECTED = ["flower_name","petal_length","petal_width"]

# 1. Load and Process Data
data_definition = dp.DataDefinition(DATA_FILE,COLS_SELECTED)
df = data_definition.get_pandas_dataframe()

kc = [0, 1, 2]
kct = ['category', 'float', 'float']

ds = dp.DataPreProcessing({'kc':kc,'kct':kct})
dfOut = ds.dataProcess(df)

data_to_process = dp.DataProcess(df)

# 2. Chart Selection
ci = cid.chartIdentification({'kct':kct})

chartD = ci.getChartType(ci.getDFattribs(dfOut), 'chartType')

# the chart about text is in the about column of the chartCriteria dataframe
# chartType is a enum with the top chart choice "first"
# the full list
[print('?', '{:9} = {}'.format(c.name, c.value)) for c in chartD['chartType']]
#or the first item
chartD['chartType']._member_map_[list(chartD['chartType']._member_map_)[0]].value

#to retain the enum for the first item
chartFound = chartD['chartType']._member_map_[list(chartD['chartType']._member_map_)[0]].value

# 3. Chart Generation
chartLocation = "/opt/data/chart_output/scatterplot.html"

if str(chartD['chartCriteria']['about'][0]) != "None":
    about_str = chartD['chartCriteria']['about'][0]
else:
    about_str = ""

chart = gc.Chart(chartD, chartFound, dfOut, 700, 400, about_str,chartLocation)

######################

""" BARCHART """

DATA_FILE = "/opt/data/datafiles/barchart_fruits.csv"

COLS_SELECTED = ["Fruits"]

# 1. Load and Process Data
data_definition = dp.DataDefinition(DATA_FILE,COLS_SELECTED)
df = data_definition.get_pandas_dataframe()

kc = [0]
kct = ['category']

ds = dp.DataPreProcessing({'kc':kc,'kct':kct})
dfOut = ds.dataProcess(df)

data_to_process = dp.DataProcess(df)

# 2. Chart Selection
ci = cid.chartIdentification({'kct':kct})

chartD = ci.getChartType(ci.getDFattribs(dfOut), 'chartType')

# the chart about text is in the about column of the chartCriteria dataframe
# chartType is a enum with the top chart choice "first"
# the full list
[print('?', '{:9} = {}'.format(c.name, c.value)) for c in chartD['chartType']]
#or the first item
chartD['chartType']._member_map_[list(chartD['chartType']._member_map_)[0]].value

#to retain the enum for the first item
chartFound = chartD['chartType']._member_map_[list(chartD['chartType']._member_map_)[0]].value

# 3. Chart Generation
chartLocation = "/opt/data/chart_output/barchart.html"

if str(chartD['chartCriteria']['about'][0]) != "None":
    about_str = chartD['chartCriteria']['about'][0]
else:
    about_str = ""

chart = gc.Chart(chartD, chartFound, dfOut, 700, 400, about_str,chartLocation)

#####################

""" HISTOGRAM """
DATA_FILE = "/opt/data/datafiles/data.csv"

COLS_SELECTED = ["Inbound"]

# 1. Load and Process Data
data_definition = dp.DataDefinition(DATA_FILE,COLS_SELECTED)
df = data_definition.get_pandas_dataframe()

kc = [1]
kct = ['int']

ds = dp.DataPreProcessing({'kc':kc,'kct':kct})
dfOut = ds.dataProcess(df)

data_to_process = dp.DataProcess(df)

# 2. Chart Selection
ci = cid.chartIdentification({'kct':kct})

chartD = ci.getChartType(ci.getDFattribs(dfOut), 'chartType')

# the chart about text is in the about column of the chartCriteria dataframe
# chartType is a enum with the top chart choice "first"
# the full list
[print('?', '{:9} = {}'.format(c.name, c.value)) for c in chartD['chartType']]
#or the first item
chartD['chartType']._member_map_[list(chartD['chartType']._member_map_)[0]].value

#to retain the enum for the first item
chartFound = chartD['chartType']._member_map_[list(chartD['chartType']._member_map_)[0]].value

# 3. Chart Generation
chartLocation = "/opt/data/chart_output/histogram.html"

if str(chartD['chartCriteria']['about'][0]) != "None":
    about_str = chartD['chartCriteria']['about'][0]
else:
    about_str = ""

chart = gc.Chart(chartD, chartFound, dfOut, 700, 400, about_str,chartLocation)

#####################

""" BOX PLOT """
DATA_FILE = "/opt/data/datafiles/heights.csv"

COLS_SELECTED = ["height","sex"]

# 1. Load and Process Data
data_definition = dp.DataDefinition(DATA_FILE,COLS_SELECTED)
df = data_definition.get_pandas_dataframe()

kc = [1,2]
kct = ['float','category']

ds = dp.DataPreProcessing({'kc':kc,'kct':kct})
dfOut = ds.dataProcess(df)

data_to_process = dp.DataProcess(df)

# 2. Chart Selection
ci = cid.chartIdentification({'kct':kct})

chartD = ci.getChartType(ci.getDFattribs(dfOut), 'chartType')

# the chart about text is in the about column of the chartCriteria dataframe
# chartType is a enum with the top chart choice "first"
# the full list
[print('?', '{:9} = {}'.format(c.name, c.value)) for c in chartD['chartType']]
#or the first item
chartD['chartType']._member_map_[list(chartD['chartType']._member_map_)[0]].value

#to retain the enum for the first item
chartFound = chartD['chartType']._member_map_[list(chartD['chartType']._member_map_)[0]].value

# 3. Chart Generation
chartLocation = "/opt/data/chart_output/boxplot.html"

if str(chartD['chartCriteria']['about'][0]) != "None":
    about_str = chartD['chartCriteria']['about'][0]
else:
    about_str = ""

chart = gc.Chart(chartD, chartFound, dfOut, 700, 400, about_str,chartLocation)

#####################

# Output Log File
print("")
print("")
print("Output main log file from container")
f = open(LOG_FILENAME, 'rt')
try:
    body = f.read()
finally:
    f.close()

print('FILE:')
print(body)
