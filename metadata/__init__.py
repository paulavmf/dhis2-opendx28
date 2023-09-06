import requests
import datetime
import json
import pandas as pd
import re
import logging


URL = "http://localhost:8080"
# "https://dhis2.medtec4susdev.org"

def setup_logging(log_filename, log_level=logging.INFO):
    """
    Set up basic logging configuration.

    Parameters:
    - log_filename (str): The name of the file to log messages to.
    - log_level: The root logger level (default is logging.INFO).
    """
    # Set up the basic configuration
    logging.basicConfig(filename=log_filename,
                        level=log_level,
                        format='%(asctime)s - %(levelname)s - %(message)s')


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


def login():
    session = requests.Session()
    session.auth = ('admin', 'district')
    return session


def createDataElement(payload):  # create a new data element into dhis

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
    # payload = {
    #     "code": code,
    #     "name": name,
    #     "shortName": shortName,
    #     "aggregationType": agregationType,
    #     "domainType": domainType,
    #     "valueType": valueType,
    #     "zeroIsSignificant": zeroIsSignificant,
    #     "categoryCombo": {
    #         "id": "bjDvmb4bfuf"
    #     }
    # }
    # changeLog("Generated payload with id: "+catComboID)
    # sending data
    try:
        session = login()
        url = "http://localhost:8080/api/dataElements"
        response = session.post(url, json=payload, headers={'content-type': 'application/json'})
        logging.info("[CREATE DATA ELEMENT] >> " + response.text)
        return json.loads(response.text)
    except Exception:
        logging.error("Unspected exception")


def get_dhis_disease_list():

    dhis_list =  [
    'Acute Flacid Paralysis (confirmed cases VDPV)',
    'Cholera (Confirmed cases)',
    'Dengue Fever (Confirmed cases)',
    'Diarrhoea with blood (Shigella)  (Confirmed cases)',
    'Diptheria (Confirmed cases)',
    'Measles (Confirmed cases)',
    'Pertussis (Confirmed cases)',
    'Plague (Confirmed cases)',
    'Rabies  (Confirmed cases)',
    'Rubella (Confirmed cases)',
    'Viral hemorrhagic fever (confirmed cases)',
    'Yellow Fever (Confirmed cases)',
    'Acute Flacid Paralysis (confirmed cases WPV)']

    clean_list = [re.sub(r'\s*\([^)]*\)', '', item).strip() for item in dhis_list]
    return clean_list

