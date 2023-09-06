import requests
import string
import random
import datetime
import os
import json
import re

import gnuh_controls as gnuh




# Generate unic id
def generate_id(long:int):
    # def characters
    characters = string.ascii_letters + string.digits

    # Generate random id
    generated_id = ''.join(random.choice(characters) for _ in range(long))

    return generated_id
# Save a detailed log
def changeLog(txt:str):
    current_time = datetime.datetime.now()
    log_txt = f"{current_time}: "+f"{txt}"+f'\n'

    # folder name
    log_folder = "./logs"
    # logfile name
    logFile = os.path.join(log_folder, f"log{datetime.date.today()}.txt")
    try:
        with open(logFile,"a") as file:
            file.write(log_txt)
    except:
        # create folder if not exist
        if not os.path.exists(log_folder):
            os.makedirs(logFile)
        # create file if not exist
        if not os.path.exists(logFile):
            open(logFile, 'w').close()

# Get Info about DataSets filtered by name
def getDataSetInfoByName(name):
    """
    :param name: name used to filter in to data sets
    :return: This method return the basic information about specific dataset filtered by id
    """

    try:
        session = login()
        url = f"http://localhost:8080/api/dataSets.json?"
        params = {
            "filter":f"name:like:{name}"
        }
        response = session.get(url, headers={'content-type': 'application/json'}, params=params)
        changeLog(f"[FETCHING DATA-SET INFO] >> {response.text}")
        return response.text
    except Exception:
        changeLog("Unspected exception")
# Get Info about DataSets filtered by name
def getOrgUnitInfoByName(name):
    """
    :param name: name used to filter in to OrgUnits
    :return: This method return the basic information about specific organisation unit filtered by id
    """
    try:
        session = login()
        url = f"http://localhost:8080/api/organisationUnits.json?"
        params = {
            "filter": f"name:like:{name}"
        }
        response = session.get(url, headers={'content-type': 'application/json'}, params=params)
        changeLog(f"[FETCHING ORG-UNIT INFO] >> {response.text}")
        return response.text
    except Exception:
        changeLog("Unspected exception")
# Get Info about DataElements filtered by name
def getDataElementInfoByName(name):
    """
    :param name: name used to filter inn to Data Elements
    :return:  This method return the basic information about specific data element filtered by id
    """
    try:
        session = login()
        url = f"http://localhost:8080/api/dataElements.json?"
        params = {
            "filter": f"name:like:{name}"
        }
        response = session.get(url, headers={'content-type': 'application/json'}, params=params)
        changeLog(f"[FETCHING DATA-ELEMENT INFO] >> {response.text}")
        return response.text
    except Exception:
        changeLog("Unspected exception")
# Generate a session to makes request
def login():
    session = requests.Session()
    session.auth = ('admin', 'district')
    return session

def createDataElement(code:str,name:str, shortName:str,agregationType:str,domainType:str,valueType:str,zeroIsSignificant:bool):  # create a new data element into dhis
    """
    :param code:
    :param name:
    :param shortName:
    :param agregationType: [SUM,AVERAGE,MIN,MAX,COUNT,FIRST,LAST,STDDEV,VARIANCE,PERCENTILE,MEDIAN]
    :param domainType: [AGGREGATE,TRACKER]
    :param valueType: [TEXT,NUMBER,DATE,BOOLEAN,OPTION (like array list),ORGANISATION_UNIT,FILE_RESOURCE,COORDINATE,URL,CALCULATED_VALUE (for formula)
    :param zeroIsSignificant: True/False
    :return:
    """
    """
    NOTA el category combo es usado para agrupar datos y asociarlos a un id por ejemplo edades o elementos similes
    no es buena idea crear un id combo cada vez que se envian datos, hay que establecer un procedimiento para segun los
    datos que se quieran agrupar se genere un combo nuevo para esos datos
    """
    payload = {
    "code": code,
    "name": name,
    "shortName": shortName,
    "aggregationType": agregationType,
    "domainType": domainType,
    "valueType": valueType,
    "zeroIsSignificant": zeroIsSignificant,
    "categoryCombo": {
        "id": "bjDvmb4bfuf"
        }
    }
    # changeLog("Generated payload with id: "+catComboID)
    # sending data
    try:
        session = login()
        url = "http://localhost:8080/api/dataElements"
        response = session.post(url, json=payload, headers={'content-type': 'application/json'})
        changeLog("[CREATE DATA ELEMENT] >> "+response.text)
    except Exception:
        changeLog("Unspected exception")
def createDataSet(name:str,shortname:str,periodType:str,expiryDays:int,dataElementArr:[],orgUnitArr:[]):
    """
    :param name:
    :param shortname:
    :param periodType: Monthly,
    :param expiryDays: Limits of days until expire the data set ex: 365 or 1000 need to be int data type
    :param dataElementArr: an array list with all ids related to data elements example arrDE = list(["bDH5ZuaeyHH"])
    :param orgUnitArr: an arrat kust with the oute of organizations units starting from the root one
            Example: 'Sierra Leone', 'otherOrgUnit inside'
    :return:
    """

    """
    NOTE
    - The data elements is refered by uid from db and can be seen using '/api/dataElements.json'
    - This method automatically attach the data set to main org unit
    """
    changeLog(f"[CREATE DATA SET] >>  {len(dataElementArr)} DataElement(s) added to DataSet {name}")
    # Generate a data elements list to be added in payload dataSetElements section
    DataElementsList = []
    for x in dataElementArr:
        dataElement = {"dataElement": {"id": x}}
        changeLog(f"[CREATE DATA SET] >>  {x} DataElement added to DataSet {name}")
        DataElementsList.append(dataElement)
    # Generated a OrgUnit element list to be added in payload organisation units section
    OrgUnitList = []
    for x in orgUnitArr:
        OrgUnit = {'id': x}
        changeLog(f"[CREATE DATA SET] >>  {x} OrgUnit added to DataSet {name}")
        OrgUnitList.append(OrgUnit)
    payload = {
        'name': name,  # Name of the dataset
        'shortName': shortname,  # Short name for the dataset
        'periodType': periodType,  # Period type for the dataset
        'expiryDays': expiryDays,  # Number of days until dataset expires
        "dataSetElements": DataElementsList,
        "sharing": {
            "public": "rw------",
            "external": True,
        },
        "organisationUnits": OrgUnitList,
        #ImspTQPwCqd
    }
    try:
        session = login()
        url = "http://localhost:8080/api/dataSets"
        response = session.post(url, json=payload, headers={'content-type': 'application/json'})
        changeLog("[CREATE DATA SET] "+response.text)
    except Exception:
        changeLog("Unspected exception")

# Used to create an organisation unit
def createOrgUnit(code:str,name:str,shortname:str,preriodType:str):
    """
    :param code:
    :param name:
    :param shortname:
    :param preriodType:
    :return:
    """

    """parent its Sierra leone instance or main instance of organization unit"""
    payload = {
        'code': code,
        'name': name,
        'shortName': shortname,
        'openingDate': f"{datetime.date.today().strftime('%Y-%m-%d')}",
        'periodType': preriodType,
        "parent": {
            "id": "ImspTQPwCqd",
        }
    }
    try:
        session = login()
        url = "http://localhost:8080/api/organisationUnits"
        response = session.post(url, json=payload, headers={'content-type': 'application/json'})
        changeLog("[CREATE ORGANISATION UNIT] >> "+response.text)
    except Exception:
        changeLog("Unspected exception")
# Used to upload dava values to specific dara set
def addDataValue(DataSetName:str,OrgUnitName:str,DataValueSets):
    """
    :param DataSetName: used to find the id of the dataset
    :param OrgUnitName: used to find the id of the Organization units
                        need the exact structure in dhis for example "Sierra Leone","any other orgunit inside"
    :param DataValueSets: data vec with this format { "dataElement": "dataelement id", "value": "value to upload" }
    :return: none
    """
    # Getting data set id for payload
    DataSetLoaded = json.loads(getDataSetInfoByName(DataSetName))
    DataSetId = DataSetLoaded['dataSets'][0]['id']
    changeLog(f"[FETCHING DATA-SET ID] >> " + DataSetId)

    # Getting orgUnit id for payload
    OrgUnitLoaded = json.loads(getOrgUnitInfoByName(OrgUnitName))
    OrgUnitId = OrgUnitLoaded['organisationUnits'][0]['id']
    changeLog(f"[FETCHING ORG-UNIT ID] >> " + OrgUnitId)

    # Process data value sets for get all ids instead his name
    changeLog(f"[PROCESSING DATA] >> " + "Converting dataelement name to data element id")
    DataValueSets_loaded = json.loads(DataValueSets)
    for i in DataValueSets_loaded:
        dt_info = json.loads(getDataElementInfoByName(i['dataElement']))
        dt_id = dt_info['dataElements'][0]['id']
        i['dataElement'] = dt_id
    payload = {
        "dataSet": DataSetId,
        "completeDate": f"{datetime.date.today().strftime('%Y-%m-%d')}",
        "period": "202304",
        "orgUnit": OrgUnitId,
        "dataValues": DataValueSets_loaded
    }
    try:
        session = login()
        url = "http://localhost:8080/api/dataValueSets"
        response = session.post(url, json=payload, headers={'content-type': 'application/json'})
        changeLog("[INSERT DATA-VALUE-SET] >> "+response.text)
    except Exception:
        changeLog("Unspected exception")


"""
####################################################################
##                      PROCESSING DATA                           ##
####################################################################
"""
def postProcessingData(dataName:str,structName:str,orgUnit:str,value):
    """
    :param dataName: name of the data that you want to upload (that make reference to dataElemen of dhis2)
    :param structName: name of the group or related data (that make reference to DataSet)
    :param orgUnit: name of the organist that you can group all related DataSetsw
    :param value: value that you want upload
    :return: none
    """


    """Get data type"""
    valueType = str(type(value))
    filtedValueType = re.findall(r"'(.*?)'", valueType)[0]

    # Selecting type
    def number():
       return "NUMBER"
    def text():
        return "TEXT"
    def error():
        print("err")

    switch_schema = {
        "int": number,
        "float": number,
        "str": text,
        "error": error,
    }

    """Create data element"""
    createDataElement(dataName,dataName,dataName,"SUM","AGGREGATE",switch_schema.get(filtedValueType, error)(),False)

    """Create organization unit"""
    createOrgUnit(orgUnit,orgUnit,orgUnit,"Monthly")

    """Create Data Set"""
    """Getting all ids of necesary data elements"""
    DEID = json.loads(getDataElementInfoByName(dataName))["dataElements"][0]["id"]
    arrDE = list([DEID])

    """Gettig all ids of necesary Orgunits starting from root Orgunit"""
    # THIS PART IS COMPLETLY NECESARY TO MAKE VISIBLE THE ORGUNIT TO SUPER USER
    rootOrgUnit = json.loads(getOrgUnitInfoByName("Sierra Leone"))["organisationUnits"][0]["id"]
    orgunitID = json.loads(getOrgUnitInfoByName(orgUnit))["organisationUnits"][0]["id"]
    arrOrgUnit = list([rootOrgUnit,orgunitID])

    """Sending a request to create a data set"""
    createDataSet(structName,structName,"Monthly",365,arrDE,arrOrgUnit)

    """Adding data"""
    dataInput = [
        {"dataElement": dataName, "value": value},
    ]
    addDataValue(structName,orgUnit,json.dumps(dataInput))
