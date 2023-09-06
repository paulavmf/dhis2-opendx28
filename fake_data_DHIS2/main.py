import json
from fake_data_DHIS2.gen import *

def org_units_dict():
    org_units_sen = ["y9Klh0O59vB",
                     "W8ZmxXgvCkY",
                     "kJIGh9lW8a8",
                     "UeC7s1uajH8",
                     "E24bLyrjfPI",
                     "xYhOeNPEaHg",
                     "BBKMl3wPek3",
                     "Sx7WMf3JxPL",
                     "u3qWtYM1nMY",
                     "Nekj896sgXP",
                     "vE39as9Ji6J",
                     "nhEFDv2BoVO",
                     "qbcz4wAp08p",
                     "LkwyLAppt46"]
    senegal_population = {
        'Dakar': 3120000,
        'Diourbel': 1410000,
        'Fatick': 640000,
        'Kaffrine': 554000,
        'Kaolack': 1119000,
        'Kédougou': 171000,
        'Kolda': 831000,
        'Louga': 873000,
        'Matam': 605000,
        'Saint-Louis': 939000,
        'Sédhiou': 451000,
        'Tambacounda': 858000,
        'Thiès': 1864000,
        'Ziguinchor': 621000
    }

    org_units = {
        "id": org_units_sen,
        "name": list(senegal_population.keys()),
        "pop": list(senegal_population.values())
    }
    return  org_units

def post_data_value_sets(data_value_sets):
    # Login
    url = "http://localhost:8080/api/me"
    #     payload = {"username": "admin", "password": "district"}
    session = requests.Session()
    session.auth = ('admin', 'district')

    # Post data value sets
    url = "http://localhost:8080/api/dataValueSets"
    headers = {"Content-Type": "application/json"}
    response = session.put(url, json=data_value_sets, headers=headers)

    # Check if posting was successful
    if response.status_code == 200:
        print("Data value sets posted successfully")
    else:
        print("Posting data value sets failed")
        print(json.loads(response.text))

    return response


def send_period_data_values(week,year,org_units,dataElements_df,dataSet_id,max_range):
    periods = periods_dict(year, 1)
    dataSet_id = "OTvkNTijYQY"
    response = []

    n = 0
    for org in org_units['id']:
        fake_df = gen_data_fake_dataframe(org_units["pop"][n], dataElements_df, max_range)
        dataValue = build_dataElement_bulk_json(week, periods[week], org, dataSet_id, fake_df)
        n = +1
        r = post_data_value_sets(dataValue)
        response.append(r)
    return response


def import_dataElements_metadata():
    xlsx = 'IDS_AGG_1.2.0_DHIS2.39/IDS_AGG_COMPLETE_1.2.0_DHIS2.39/IDS_AGG_COMPLETE_1.2.0_DHIS2.39.xlsx'
    sheet_1 = 'dataElements'
    sheet_2 = 'validationRules'
    dataElements_df = pd.read_excel(xlsx, sheet_1)
    # validationRules = pd.read_excel(xlsx, sheet_2)
    return dataElements_df


if __name__ == '__main__':
    org_units = org_units_dict()
    dataElements_df = import_dataElements_metadata()
    dataset_id = "OTvkNTijYQY"
    response_list = send_period_data_values("20W2022", 2022, org_units, dataElements_df,dataset_id, 0.3)


