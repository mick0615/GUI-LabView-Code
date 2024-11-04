import pygsheets

class GoogleSheetAPI( ):
    def __init__(self):
        self.gc = None
        self.sh = None
        self.wks = None

    def loginAuth( self, authFile ):
        self.gc = pygsheets.authorize(service_account_file=authFile)

    #==========================================#
    # spread sheet config
    #==========================================#
    def setSpreadSheet ( self, sheetName="newSheet" ):
        #========= Get Sheet Method ==========#
        # open sheet url
        #sheet_url = "https://docs.google.com/spreadsheets/d/18pfe3HmMO1nU2tv20vbHlTtx7lnEzBmX5vXqxO4TlNU/edit#gid=0" 
        #sh = gc.open_by_url(sheet_url)

        # connect cloud open sheet file
        self.sh = self.gc.open( sheetName )
    
    def getSpreadSheetJSON( self ):
        return self.sh.to_json()
    
    def getWksList( self ):
        wksList = []
        for idx, val in enumerate( self.sh.worksheets() ):
            wksList.append( str( val ) )
        return wksList
    
    def delWks( self, index=0 ):
        delWksId = self.sh[ index ]
        self.sh.del_worksheet( delWksId )

    #==========================================#
    # work sheet config
    #==========================================#
    def setWks( self, index=0 ):
        workSheetList = self.getWksList()
        if index >= len(workSheetList):
            raise IndexError( "The index sheet not found" )
        self.wks = self.sh[ index ]

    def addWks( self, workName="work1", rowVal=1, colVal=1 ):
        workSheetList = self.getWksList()
        for idx, val in enumerate( workSheetList ):
            if val.title == workName:
                raise NameError( "The work name already exists in this spread sheet" )
        self.sh.add_worksheet( workName, rowVal, colVal )

    def appendNewData( self, dataArray, start=None, end=None, dimension='rows', overwrite=False ):
        if self.wks.rows == 1 and len(self.wks.get_value( "A1" )) == 0:
            self.wks.update_values( "A1", [dataArray] )
        else:
            try:
                self.wks.append_table( dataArray, start=start, end=end, dimension=dimension, overwrite=overwrite )
            except Exception as e:
                print( e.args[0] )
                pass

    def getWksSize( self ):
        rowVal = self.wks.rows
        colVal = self.wks.cols
        return [rowVal, colVal]

    def getWksAllData( self ):
        return self.wks.get_all_values()

    def getWksRowData( self, index=1 ):
        if index < 1:
            raise IndexError( "The minimum row index is 1" )
        return self.wks.get_row( index )
    
    def updValue( self, rowIdx=1, colIdx=1, val="" ):
        self.wks.update_value( ( rowIdx, colIdx ), val )

    def delRowData( self, index=1, length=1 ):
        self.wks.delete_rows( index=index, number=length )
    
    def delColData( self, index=1, length=1 ):
        self.wks.delete_cols( index=index, number=length )

    def clsWks( self ):
        if self.wks.rows == 1:
            self.wks.clear( "A1" )
        else:
            self.wks.clear()