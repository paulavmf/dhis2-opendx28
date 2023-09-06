import json

from proteus import config, Model
import statistics
from datetime import datetime
import dhis_controls as dhis

"""
Server conf
"""
user = 'admin'
password = "opendx28"
dbname = "ghs1"
hostname = 'localhost'
port = '8000'
health_server = 'http://'+user+':'+password+'@'+hostname+':'+port+'/'+dbname+'/'
conf = config.set_xmlrpc(health_server)

def getAnalyte(analyte:str):
    """
    :param: analyte: Hemoglobin, RBC etc.
    :return: a list with all non None values from an analyte
    """
    ModelName = Model.get('gnuhealth.lab.test.critearea')
    records = ModelName.find(["name","=",analyte])
    dhis.changeLog("[FETCHING ANALYTE DATA] >> ANALYTE:"+analyte)

    resultsValues = []
    # add head to the package, this is used to know in dhis the name and where come from the data
    # this data is used to create the name of data sets and data elements
    now = datetime.now()
    dataHeader = {
        "model_comefrom":'gnuhealth.lab.test.critearea',
        "analyte_name":analyte,
        "timestamp": now.strftime("%d/%m/%Y %H:%M:%S")
    }
    jsonData = json.dumps(dataHeader)
    resultsValues.insert(0,jsonData) # setting the analyte name in first place
    # Mostrar la información de cada registro
    for record in records:
        if record.result != None:
            resultsValues.append(record.result)
        dhis.changeLog(f"Data: {record.id}:{record.name}:{record.result}")
        print(record.result)

    return resultsValues

def avgDataSet(dataSet:[float]):
    """
    :param dataSet: ["Hemoglobin",10.0,5.9,11.0]
    :return: the average of float dataSet values
    """
    del dataSet[0] #Delete the name of analyte to operate with numbers only
    return statistics.mean(dataSet)

def getDataStructure(model:str):
    """
    Show in log the data structure of a model throw in params
    :param model: example 'gnuhealth.lab.test.critearea'
    :return: None
    """
    # Obtain data model structure
    ModelName = Model.get(model)
    context = {}
    properties = ModelName.fields_get(context)
    # show up the structure fields
    for field_name, field_props in properties.items():
        dhis.changeLog(f"field: {field_name}, {field_props['string']}, {field_props['type']}")
