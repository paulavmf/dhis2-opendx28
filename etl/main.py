import json
import re
import dhis_controls as dhis
import gnuh_controls as gnuh

if __name__ == '__main__':
    """
    #############################################################################
    ##                                                                         ##
    ##                          Upload test Zone                               ##
    ##                                                                         ##
    #############################################################################"""

    # """Create data element"""
    # dhis.createDataElement("AR1","AR1","AR1","SUM","AGGREGATE","TEXT",False)
    # dhis.createDataElement("AR2","AR2","AR2","SUM","AGGREGATE","TEXT",False)
    # """Create organization unit"""
    # dhis.createOrgUnit("AR_ORFUNIT1","AR_ORFUNIT1","AR_ORFUNIT1","Monthly")
    # """Create Data Set"""
    # #Getting all ids of necesary data elements
    # DEID = json.loads(dhis.getDataElementInfoByName("AR1"))["dataElements"][0]["id"]
    # DEID2 = json.loads(dhis.getDataElementInfoByName("AR2"))["dataElements"][0]["id"]
    # arrDE = list([DEID,DEID2])
    # #Gettig all ids of necesary Orgunits starting from root Orgunit
    # rootOrgUnit = json.loads(dhis.getOrgUnitInfoByName("Sierra Leone"))["organisationUnits"][0]["id"]
    # orgunit = json.loads(dhis.getOrgUnitInfoByName("AR_ORFUNIT1"))["organisationUnits"][0]["id"]
    # arrOrgUnit = list([rootOrgUnit,orgunit])
    # #Sending a request to create a data set
    # dhis.createDataSet("AR_DATSET1_ORGURECT_HARDCODED_2","AR_DATSET1_ORGURECT_HARDCODED_2","Monthly",365,arrDE,arrOrgUnit)
    # """Adding data"""
    # DEID = json.loads(dhis.getDataElementInfoByName("AR1"))["dataElements"][0]["id"]
    # dataInput = [
    #     {"dataElement": "AR1", "value": "texto1"},
    #     {"dataElement": "AR2", "value": "texto1"},
    #
    # ]
    # dhis.addDataValue("AR_DATSET1","AR_ORFUNIT1",json.dumps(dataInput))

    """
    #############################################################################
    ##                                                                          ##
    ##                          Getting Data                                    ##
    ##                                                                          ##
    #############################################################################"""

    analyteReturnedVec = gnuh.getAnalyte("MCV")
    #discompose vars
    innerJsonLoad = json.loads(analyteReturnedVec[0])
    analyteName = innerJsonLoad["analyte_name"]
    comefrom = innerJsonLoad["model_comefrom"]
    timestamp = innerJsonLoad["timestamp"]
    analyteTestAvg = 0

    analyteReturnedVec.__delitem__(0)
    analyteTestAvg = gnuh.avgDataSet(analyteReturnedVec)

    """
    #############################################################################
    ## TRESPASSED VALUES FROM BEHIND:  analyteTestAvg                          ##
    ##                               ETL Zone                                  ##
    ##                                                                         ##
    #############################################################################"""

    dhis.postProcessingData("AVG_HGB","AVG_LAB_TEST","LAB_TEST",analyteTestAvg)
