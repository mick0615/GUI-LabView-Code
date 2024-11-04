import sheetAPI
import json

api = sheetAPI.GoogleSheetAPI()

apiCmd = {
    "loginAuth": lambda recv: api.loginAuth( authFile=recv["authFile"] ),
    "setSpreadSheet": lambda recv: api.setSpreadSheet( sheetName=recv["sheetName"] ),
    "setWks": lambda recv: api.setWks( index=int( recv["idx"] ) ),
    "getWksList": lambda recv: api.getWksList(),
    "delWks": lambda recv: api.delWks( index=int( recv["idx"] ) ),
    "addWks": lambda recv: api.addWks( workName=recv["wksName"], rowVal=int( recv["rowSize"] ), colVal=int( recv["colSize"] ) ),
    "appendNewData": lambda recv: api.appendNewData( dataArray=recv["dataArray"] ),
    "getAllData": lambda recv: api.getWksAllData(),
    "getRowData": lambda recv: api.getWksRowData( index=int( recv["idx"] ) ),
    "getSpreadSheetJSON": lambda recv: api.getSpreadSheetJSON(),
    "updValue": lambda recv: api.updValue( rowIdx=int( recv["rowIdx"] ), colIdx=int( recv["colIdx"] ), value=int( recv["val"] ) ),
    "delRowData": lambda recv: api.delRowData( index=int( recv["idx"] ), length=int( recv["len"] ) ),
    "delColData": lambda recv: api.delColData( index=int( recv["idx"] ), length=int( recv["len"] ) ),
    "clsWks": lambda recv: api.clsWks()
}

def main( cmdJSON=None, error="" ):
    response = {
        "res": "",
        "errMsg": "",
        "valid": "0"
    }
    try:
        if cmdJSON is None:
            raise AttributeError( "command is none" )
        else:
            recv = json.loads( cmdJSON )
            cmd = recv["cmd"]
            returnVal = apiCmd.get( cmd, "command error" )( recv )
        response["res"] = returnVal
        response = json.dumps( response )
    except Exception as e:
        error = e.args[0]
        response["errMsg"] = error
        response = json.dumps( response )
    return response