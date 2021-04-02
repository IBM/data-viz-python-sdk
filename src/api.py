import json
from flask import Flask, request, jsonify

import src.amhairc.dataProcessing.data_processing as dp
import src.amhairc.chartSelection.chart_identification as cid
import src.amhairc.chartGeneration.generate_chart as gc

app = Flask(__name__)

@app.route('/test', methods=['POST','GET'])
def test():
    app.logger.info("Test Page")
    return ""


@app.route('/api/process', methods=['POST','GET'])
def process():
    content = request.json

    folderPath = content['folderPath']
    fileName = content['fileName']
    columns = content['columns']
    chartId = content['chartId']
    app.logger.info(columns)
    app.logger.info(folderPath)
    app.logger.info(fileName)

    names = []
    indices = []
    types = []
    for column in columns:
        name = column['name']
        index = column['index']
        type = column['type']
        names.append(name)
        indices.append(index)
        types.append(type)
        print(name)
        print(index)
        print(type)

    generate_chart(folderPath, fileName, names, indices,types,chartId)

    return ""


def generate_chart(folderPath, fileName,names,indices,types,chartId):

    app.logger.info("Starting plotting")

    DATA_FILE = folderPath + "/" + fileName

    COLS_SELECTED = names
    kc = indices
    kct = types

    app.logger.info("kc:"+str(kc))
    app.logger.info("kct:"+str(kct))

    # 1. Load and Process Data
    data_definition = dp.DataDefinition(DATA_FILE,COLS_SELECTED)
    df = data_definition.get_pandas_dataframe()
    app.logger.info(df.head())

    ds = dp.DataPreProcessing({'kc':kc,'kct':kct})
    dfOut = ds.dataProcess(df)

    data_to_process = dp.DataProcess(df)
    #app.logger.info("3.", data_to_process.data_types_strings)

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
    #app.logger.info("4.", chartD['chartType']._member_map_[list(chartD['chartType']._member_map_)[0]])

    #chart_selection = ic.ChartSelection(data_to_process.data_types_strings,COLS_SELECTED)

    chartFound = chartD['chartType']._member_map_[list(chartD['chartType']._member_map_)[0]].value

    # 3. Chart Generation
    #app.logger.info("5.", dfOut)
    #app.logger.info("6.", chartFound)
    #app.logger.info("7. Number of series:", chartD['chartCriteria']['series'].values.tolist()[0])

    #app.logger.info(dfOut)
    #app.logger.info(chartFound)
    #app.logger.info(str("Sample " + chartFound + " Plot"))

    if str(chartD['chartCriteria']['about'][0]) != "None":
        about_str = chartD['chartCriteria']['about'][0]
    else:
        about_str = ""

    chart_location = str(folderPath) + "/" + str(chartId) + ".html"

    chart = gc.Chart(chartD, chartFound, dfOut, 700, 400, about_str,chart_location)
    pass

app.run(port="8080",host="0.0.0.0",debug=True)