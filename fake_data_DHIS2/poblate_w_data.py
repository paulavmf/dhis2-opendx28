
import datetime
import random
import requests
import json
import os
import pandas as pd

URL = "http://localhost:8080"
"https://dhis2.medtec4susdev.org"

## Poblate
dataElement = ['Yellow Fever (Suspected cases)', 'Yellow Fever (Confirmed cases)']
dataSet = ['IDS - Report: Suspected, Confirm, Death']
orgUnit_level4 = ['Hospital_Adeje',
 'Hospital_Adrar',
 'Hospital_Agaete',
 'Hospital_Agüimes',
 'Hospital_Agulo',
 'Hospital_Alajeró',
 'Hospital_Antigua',
 'Hospital_Arafo',
 'Hospital_Arico',
 'Hospital_Arona',
 'Hospital_Arrecife',
 'Hospital_Artenara',
 'Hospital_Arucas',
 'Hospital_Assaba',
 'Hospital_Barlavento',
 'Hospital_Barlovento',
 'Hospital_Betancuria',
 'Hospital_Boa Vista',
 'Hospital_Brakna',
 'Hospital_Brava',
 'Hospital_Breña Alta',
 'Hospital_Breña Baja',
 'Hospital_Buenavista del Norte',
 'Hospital_Candelaria',
 'Hospital_Dakar',
 'Hospital_Dakhlet Nouadhibou',
 'Hospital_Diourbel',
 'Hospital_El Paso',
 'Hospital_El Pinar de El Hierro',
 'Hospital_El Rosario',
 'Hospital_El Sauzal',
 'Hospital_El Tanque',
 'Hospital_Fasnia',
 'Hospital_Fatick',
 'Hospital_Firgas',
 'Hospital_Frontera',
 'Hospital_Fuencaliente de La Palma',
 'Hospital_Gáldar',
 'Hospital_Garachico',
 'Hospital_Garafía',
 'Hospital_Gorgol',
 'Hospital_Granadilla de Abona',
 'Hospital_Guía de Isora',
 'Hospital_Guidimaka',
 'Hospital_Güímar',
 'Hospital_Haría',
 'Hospital_Hermigua',
 'Hospital_Hodh Ech Chargui',
 'Hospital_Hodh El Gharbi',
 'Hospital_Icod de los Vinos',
 'sanitary_center_Adeje',
 'sanitary_center_Adrar',
 'sanitary_center_Agaete',
 'sanitary_center_Agüimes',
 'sanitary_center_Agulo',
 'sanitary_center_Alajeró',
 'sanitary_center_Antigua',
 'sanitary_center_Arafo',
 'sanitary_center_Arico',
 'sanitary_center_Arona',
 'sanitary_center_Arrecife',
 'sanitary_center_Artenara',
 'sanitary_center_Arucas',
 'sanitary_center_Assaba',
 'sanitary_center_Barlavento',
 'sanitary_center_Barlovento',
 'sanitary_center_Betancuria',
 'sanitary_center_Boa Vista',
 'sanitary_center_Brakna',
 'sanitary_center_Brava',
 'sanitary_center_Breña Alta',
 'sanitary_center_Breña Baja',
 'sanitary_center_Buenavista del Norte',
 'sanitary_center_Candelaria',
 'sanitary_center_Dakar',
 'sanitary_center_Dakhlet Nouadhibou',
 'sanitary_center_Diourbel',
 'sanitary_center_El Paso',
 'sanitary_center_El Pinar de El Hierro',
 'sanitary_center_El Rosario',
 'sanitary_center_El Sauzal',
 'sanitary_center_El Tanque',
 'sanitary_center_Fasnia',
 'sanitary_center_Fatick',
 'sanitary_center_Firgas',
 'sanitary_center_Frontera',
 'sanitary_center_Fuencaliente de La Palma',
 'sanitary_center_Gáldar',
 'sanitary_center_Garachico',
 'sanitary_center_Garafía',
 'sanitary_center_Gorgol',
 'sanitary_center_Granadilla de Abona',
 'sanitary_center_Guía de Isora',
 'sanitary_center_Guidimaka',
 'sanitary_center_Güímar',
 'sanitary_center_Haría',
 'sanitary_center_Hermigua',
 'sanitary_center_Hodh Ech Chargui',
 'sanitary_center_Hodh El Gharbi',
 'sanitary_center_Icod de los Vinos']


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

# Generate a session to makes request
def login():
    session = requests.Session()
    session.auth = ('admin', 'district')
    return session


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


def getOrgUnitsByLevel(level):
    response = get_data("organisationUnits")
    orgUnits = pd.DataFrame(response["organisationUnits"])
    same_level = list()
    for i in orgUnits["id"]:
        tmp = get_data(f"organisationUnits/{i}")
        if tmp['level'] == level:
            tmp['name']
            same_level.append(tmp['name'])
    return same_level

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


def generar_numero_ponderado(n, media):
    numeros = list(range(1, n+1))
    probabilidades = [1 / abs(x - media) if x != media else 1 for x in numeros]
    total_probabilidades = sum(probabilidades)
    ponderaciones = [p / total_probabilidades for p in probabilidades]

    numero_aleatorio = random.choices(numeros, weights=ponderaciones)[0]
    return numero_aleatorio

def generate_day_a_week(year,week_day_number):
    start_date = datetime.date(year, 1, 1)  # primer día del año
    end_date = datetime.date(year, 12, 31)  # último día del año
    delta = datetime.timedelta(days=1)

    week_day = []
    current_date = start_date

    while current_date <= end_date:
        if current_date.weekday() == week_day_number:  # 0 es lunes
            week_day.append(current_date.strftime('%Y-%m-%d'))
        current_date += delta

    return week_day

# Used to upload dava values to specific dara set
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
    print("no organisation unit:" + OrgUnitName )

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
        "dataValues": [{"dataElement":dt_id,"value":DataValueSets["value"]}]
    }
    try:
        session = login()
        url = "http://localhost:8080/api/dataValueSets"
        response = session.post(url, json=payload, headers={'content-type': 'application/json'})
        changeLog("[INSERT DATA-VALUE-SET] >> "+response.text)
    except Exception:
        changeLog("Unspected exception")


def export_random_data_test(orgUnit:str,years:list):
    import pandas as pd
    dataElement = 'Yellow Fever (Suspected cases)'
    dataSet = 'IDS - Report: Suspected, Confirm, Death'
    orgUnit = orgUnit
    #file = "extrapolated_data.csv"
    #data = pd.read_csv(file)
    # Convertir la columna 'Year' a formato de fecha y hora
    week_days = list()
    for y in years:
        week_days.extend(generate_day_a_week(y,1))
    data = dict()
    data["value"] = [generar_numero_ponderado(10,1) for n in range(len(week_days))]
    data["date"] = week_days
    data = pd.DataFrame(data)
    data.apply(addDataValue, axis = 1, args=(dataElement,dataSet,orgUnit,))
    return data


def create_random_suspected_yellow_fever(OrgUnits:list,Year:list): # %YYYY%MM%DD
    for org in OrgUnits:
        export_random_data_test(org,Year)
        return None

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

if __name__ == '__main__':
    orgUnit_level4 = getOrgUnitsByLevel(3)
    create_random_suspected_yellow_fever(orgUnit_level4,[2022])

