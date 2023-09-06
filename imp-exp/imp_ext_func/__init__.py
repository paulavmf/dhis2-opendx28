import requests
import json
import pandas as pd
import random
# from etl.dhis_controls import *



URL = "http://localhost:8080"

def open_session(user = "admin", password = "district", URL = URL  ):
    session = requests.Session()
    session.auth = (user, password)
    return session




def get_data(key):
    url = URL + "/api/me"
    session = requests.Session()
    session.auth = ('admin', 'district')
    response = session.get(URL + "/api/" + key )
    if response.status_code == 200:
        json_response = json.loads(response.text)
        return json_response
    else:
        print("bad response: " + str(response.status_code))
        return None


def getDataValueSetByDataSetID(datasetID: str):
    try:
        session = login()
        url = f"http://localhost:8080/api/dataSets/{datasetID}/dataValueSet"
        response = session.get(url)
        changeLog("[FETCHING DATA-VALUE-SET INFO] >> " + response.text)
        return response.text
    except Exception:
        changeLog("Unspected exception")


def getCategoryOptionCombo(datasetID:str,dataElementID:str):
    DataValueSetLoaded = json.loads(getDataValueSetByDataSetID(datasetID))
    for i in DataValueSetLoaded['dataValues']:
        if i["dataElement"] == dataElementID:
            return i["categoryOptionCombo"]
        else:
            changeLog(f"Cant find categoryOptionCombo for data element {dataElementID} in dataset {datasetID}")


def addDataValue(DataValueSets,DataElement:str,DataSetName:str,OrgUnitName:str):
    from datetime import datetime
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
    #DataValueSets_loaded = json.loads(DataValueSets)
    dt_info = json.loads(getDataElementInfoByName(DataElement))
    dt_id = dt_info['dataElements'][0]['id']
    # Convertir la cadena a un objeto datetime
    date_obj = datetime.strptime(DataValueSets["date"], "%Y-%m-%d")

    # Convertir el objeto datetime al formato deseado
    formatted_date = date_obj.strftime("%YW%U")
    payload = {
        "dataSet": DataSetId,
        "completeDate": DataValueSets["date"],
        "period": formatted_date,
        "orgUnit": OrgUnitId,
        "dataValues": [{"dataElement":dt_id,"value":DataValueSets["Value"]}]
    }
    try:
        session = login()
        url = "http://localhost:8080/api/dataValueSets"
        response = session.post(url, json=payload, headers={'content-type': 'application/json'})
        changeLog("[INSERT DATA-VALUE-SET] >> "+response.text)
    except Exception:
        changeLog("Unspected exception")
