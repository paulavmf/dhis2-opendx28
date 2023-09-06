import requests
import logging
from metadata import  *
import logging

"""
Occupation
Hospital discharges
Primary care discharges
Hospital beds
ICU beds


"""

def createDataElementPayloadHospital():
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

