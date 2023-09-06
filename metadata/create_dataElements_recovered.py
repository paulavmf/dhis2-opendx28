import requests
import logging
from metadata import  *
import logging

'''
Import all dataElements for all diseases recovered data:
'''

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


if __name__ == "__main__":
    setup_logging('app.log')
    dhis_disease_list = get_dhis_disease_list()
    for disease in dhis_disease_list:
        payload = dataElementRecoveredPayload(disease)
        createDataElement(payload)





