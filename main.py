import pandas as pd
import re
from math import isnan
from tkinter.filedialog import askopenfilename
from portmaster_lib import Portmaster_Lib as test
from packaging.version import parse

def isnumber(a) -> int :
        if isinstance(a, float) == True and isnan(a) == False or isinstance(a, int) :
            return True

def findMaxColumnLength(list, versionColumn) -> int :
    temp = list[0][0]
    maxLength = 0
    counter = 0
    while(counter <= len(list) -1) :
        b = len(temp)
        c = len(list[counter][0])
        if( c > b) :
            maxLength = c
        temp = list[counter][0]
        counter +=1
    
    if(len(versionColumn) > maxLength) :
        maxLength = len(versionColumn)
    return maxLength

def checkDataListing(columnHeaders: list, checkData: list, comparedData : list) -> list :
    list = []
    
    counter = 0
    for x in columnHeaders:
        list.append([])
        list[counter].append([])
        list[counter].append([]) 
        list[counter].append([]) 
        for c in reversed(checkData[x]):
            comparedDataCounter = len(comparedData[x]) - 1
            
            while(c != comparedData[x][comparedDataCounter] and comparedDataCounter >= 0) :
                comparedDataCounter -= 1

            if c == comparedData[x][comparedDataCounter] :

                list[counter][0].append(c)
                list[counter][1].append(comparedData[x][comparedDataCounter])
                list[counter][2].append(True)
                comparedData[x].pop(comparedDataCounter)
            else :
            
                list[counter][0].append(c)
                list[counter][1].append('NULL') 
                list[counter][2].append(False)

        counter += 1

    return list

def populateFrame(df: pd.DataFrame, workHeaders: list, dfWorkList :list) -> None:
    counter = 0
    while counter <= len(workHeaders) -1 :
        
        df[workHeaders[counter] + "_Worksheet"] = pd.Series(reversed(dfWorkList[counter][0]))
        df[workHeaders[counter] + "_Datasheet"] = pd.Series(reversed(dfWorkList[counter][1]))
        df[workHeaders[counter] + "_Match"] = pd.Series(reversed(dfWorkList[counter][2]))
        counter += 1

def checkVersionOrder(columnVersionCheck) : # ERROR CHECK WHY FIRST ROW IS NOT SHOWN
    versionColumn = []
    for x in columnVersionCheck:
        if(isinstance(x, int) == False):
            versionColumn.append(x)

    
    v = [[],[]]
    v[1].append("N/A")
    counter = 0
    for x in versionColumn[0:len(versionColumn) -1]:
 
        v[0].append(x)
        if(parse(x) < parse(versionColumn[counter + 1])):            
            v[1].append(True)
        else:
            v[1].append(False)
        counter +=1      
    
    v[0].append(versionColumn[len(versionColumn) - 1])
    return v 

class Main :

    excelFile = pd.ExcelFile('example.xlsx')
    read = pd.read_excel(excelFile, excelFile.sheet_names[0])

    #1------Stores each COLUMN HEADER and for each COLUMN HEADER store its entire COLUMN in a dict from Work Sheet-----
    #Version Column is processed and stored
    workHeaders = [x for x in read.columns]
    workHeaders.pop(0)
    storedTempColumns = []
    for x in workHeaders:
        storedTempColumns.append(read[x])


    versionColumn = checkVersionOrder(storedTempColumns[0]) 

    
    workColumns = {}
    counter = 0
    while counter <= len(workHeaders) -1 :
        tempColumns = [] 
        for x in storedTempColumns[counter] :
            if isnumber(x): # note that the listing i/o are floats AND ints
                tempColumns.append(int(x))
                
        workColumns[workHeaders[counter]] = tempColumns
        counter += 1  
    #1-------------------------------------END-----------------------------------------------

    #3------seperate rows into columns for each workHeaders from datasheet and store them as a dict-----
    read = pd.read_excel(excelFile, excelFile.sheet_names[1])
    dataHeader = [x for x in read.columns]
    storedTempColumns = read[dataHeader[0]]

    
    dataColumns = {}
    counter = 0
    for x in workHeaders :
        tempColumns = []
        for c in storedTempColumns :
            if (re.search(workHeaders[counter], str(c))):
                
                tempRow = str(c).replace((workHeaders[counter]+'_'),'')
                tempSplit = tempRow.split('_')
                if(str.isdigit(tempSplit[0])) :
                    tempColumns.append(int(tempSplit[0]))
                
        dataColumns[workHeaders[counter]] = tempColumns 
        counter += 1
    
    #4-------------------------------------END----------------------------------------------
    
    #5-----Check if stored worksheet is found in stored datasheet ------------------------------------------------------------------------------
    dfWorkList = checkDataListing(workHeaders,workColumns, dataColumns)

    #5-------------------------------------END----------------------------------------------
    
    #--------------------------------Output to Excel---------------------------------------
    df = pd.DataFrame()
   
    df.index = range(1, findMaxColumnLength(dfWorkList, versionColumn[0]) + 1)


    counter = 0
    while counter <= len(workHeaders) -1 :
        df[workHeaders[counter] + "_Worksheet"] = pd.Series(reversed(dfWorkList[counter][0]))
        df[workHeaders[counter] + "_Datasheet"] = pd.Series(reversed(dfWorkList[counter][1]))
        df[workHeaders[counter] + "_Match"] = pd.Series(reversed(dfWorkList[counter][2]))
        counter += 1
        
    
    df['Version'] = pd.Series(versionColumn[0])
    df['Checked'] = pd.Series(versionColumn[1])
    df.to_excel('output2.xlsx', sheet_name = "Work")
    #-------------------------------------END----------------------------------------------