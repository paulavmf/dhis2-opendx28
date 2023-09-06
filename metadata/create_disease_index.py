import json
from metadata import setup_logging

from metadata import createDataElement, get_dhis_disease_list
import pandas as pd

"""

Index por enfermedad:

DailyConfirmed
DailyDeath
DailyRecovered
DailySolved
ActiveCases
PreActiveCases
DeathsPercentage
RecoveredPercentage
aHSI
dHSI
hPOR
icuPORr

B	HospitalBedOccupancyt
I	ICUBedOccupancyt
A	HospitalDischarget
PHC	PrimatyCareDischarget

St	Suspectedt
Ct	Confirmedt
Dt	Deathst
Rt	Recoveredt
Bt	HospitalBedOccupancyt
It	ICUBedOccupancyt
At	HospitalDischarget
PHCt	PrimatyCareDischarget
TB	HospitalBedCapacity
TI	ICUBedCapacityt
Solvedt	Solvedt
DailyConfirmedt	DailyConfirmedt
DailyDeatht	DailyDeatht
DailyRecoveredt	DailyRecoveredt
DailySolvedt	DailySolvedt
ActiveCasest	ActiveCasest
PreActiveCasest	PreActiveCasest
DeathsPercentaget 	DeathsPercentaget
RecoveredPercentaget	RecoveredPercentaget
aHSIt	Accumulated Health Sufficiency Index
dHSIt	Daily Health Sufficiency Index
hPORt	Potential Occupancy Ratio
icuPORr	ICU Potential Occupancy Ratio

Index por hospital:

TB	HospitalBedCapacity
TI	ICUBedCapacityt


"""


def dataElementRecoveredPayload(name):
    payload = {
        "name": f"IDS - {name} (Recovered)",
        f"shortName": f"{name} (Recovered)",
        "description": "Surveillance",
        "dimensionItemType": "DATA_ELEMENT",
        "aggregationType": "SUM",
        "valueType": "INTEGER_ZERO_OR_POSITIVE",
        "domainType": "AGGREGATE",
        "zeroIsSignificant": True,
        "optionSetValue": False,
        "dimensionItem": "bXn9Kmxnd3r",
        "dataElementGroups": [
            {
                "id": "ZE7pzepVQfy"
            }
        ],
        "categoryCombo": {
            "id": "eg8enaFY861"
        },
        "displayFormName": f"{name} cases recovered  during the week",

    }
    return payload



def createPayloadDF(df):
    from helpers import  limit_character
    import ast
    dataElementsID = pd.DataFrame(columns=["name","uid","datasetName","datasetCode","period","organisationUnits"])
    payloads = df.to_dict(orient='records')
    n = 0
    for row in payloads:
        payload_keys = ["aggregationType","domainType","name","shortName","formName","categoryCombo","valueType"]
        payload = {}
        for key in payload_keys:
            payload[key] = row[key]
        payload["categoryCombo"] = ast.literal_eval(payload["categoryCombo"])
        if row["perDissease"] == True:
            dhis_disease_list = get_dhis_disease_list()
            for disease in dhis_disease_list:
                new_payload = {}
                new_payload["name"] = f"{disease} {payload['name']}"
                new_payload["formName"] = f"{disease} {payload['formName']}"
                new_payload["shortName"] = f"{disease} {payload['shortName']}"
                new_payload["shortName"] = limit_character(new_payload["shortName"], 40)
                keys = ["aggregationType","domainType","categoryCombo","valueType"]
                for key in keys:
                    new_payload[key] = payload[key]
                response = createDataElement(new_payload)
                if response["httpStatus"] == "Created":
                    dataElementsID.loc[n] = [payload["name"], response["response"]["uid"], row["datasetName"],
                                             row["datasetCode"],row["period"],row["organisationUnits"]]
                    n = n + 1
        else:
            response = createDataElement(payload)
            if response["httpStatus"] == "Created":
                dataElementsID.loc[n] = [payload["name"], response["response"]["uid"], row["datasetName"],
                                         row["datasetCode"],row["period"], row["organisationUnits"]]
                n = n + 1
    return dataElementsID




    return dataElementsID








if __name__ == '__main__':
    # test_payload = {
    #   "name": "IDS - invented (Deaths) ",
    #   "shortName": "invented (Deaths)",
    #   "code": "IVN",
    #   "description": "test",
    #   "domainType": "AGGREGATE",
    #   "valueType": "INTEGER_ZERO_OR_POSITIVE",
    #   "aggregationType": "SUM",
    #   "categoryCombo": {
    #     "id": "bjDvmb4bfuf"
    #   }
    # }
    #
    # createDataElement(test_payload)
    setup_logging("app.log")

    df = pd.read_csv("dataElemts_per_diseases.csv")
    df = createPayloadDF(df)
    df.to_csv("dataElementsID.csv")



