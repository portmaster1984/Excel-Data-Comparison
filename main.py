import pandas as pd
import re
from math import isnan
from tkinter.filedialog import askopenfilename
from portmaster_lib import Portmaster_Lib as test

def isnumber(a) -> int :
        if isinstance(a, float) == True and isnan(a) == False or isinstance(a, int) :
            return True





class Main :

    excelFile = pd.ExcelFile('example.xlsx')
    read = pd.read_excel(excelFile, excelFile.sheet_names[0])
    #1------Stores each COLUMN HEADER and for each COLUMN HEADER store its entire COLUMN in a dict from Work Sheet-----
    workHeaders = [x for x in read.columns]
    workHeaders.pop(0)
    storedColumns = []
    for x in workHeaders:
        storedColumns.append(read[x])

    workColumns = {}

    counter = 0
    while counter <= len(workHeaders) -1 :
        tempColumns = [] 
        for x in storedColumns[counter] :
            if isnumber(x): # note that the listing i/o are floats AND ints
                tempColumns.append(int(x))
                
        workColumns[workHeaders[counter]] = tempColumns
        counter += 1  
    #1-------------------------------------END-----------------------------------------------

    read = pd.read_excel(excelFile, excelFile.sheet_names[1])

    #3------seperate rows as columns for each workHeaders from datasheet and store it as a dict-----
    dataHeader = [x for x in read.columns]
    storedColumns = read[dataHeader[0]]
    

    dataColumns = {}
   
    counter = 0
    for x in workHeaders :
        tempColumns = []
        for c in storedColumns :
            if (re.search(workHeaders[counter], c)):
                
                tempRow = str(c).replace((workHeaders[counter]+'_'),'')
                tempSplit = tempRow.split('_')
                if(str.isdigit(tempSplit[0])) :
                    tempColumns.append(int(tempSplit[0]))
                
        dataColumns[workHeaders[counter]] = tempColumns 
        counter += 1
    
    #4-------------------------------------END----------------------------------------------
    
    #5-----Check if stored worksheet is found in stored datasheet ------------------------------------------------------------------------------
    dfList = []
    
    counter = 0
    for x in workHeaders:
        dfList.append([])
        dfList[counter].append([])
        dfList[counter].append([]) 
        dfList[counter].append([]) 
        for c in reversed(workColumns[x]):
            dataCounter = len(dataColumns[x]) - 1
            
            while(c != dataColumns[x][dataCounter] and dataCounter >= 0) :
                dataCounter -= 1

            if c == dataColumns[x][dataCounter] :

                dfList[counter][0].append(c)
                dfList[counter][1].append(dataColumns[x][dataCounter])
                dfList[counter][2].append(True)
                dataColumns[x].pop(dataCounter)
            else :
            
                dfList[counter][0].append(c)
                dfList[counter][1].append('') 
                dfList[counter][2].append(False)

        counter += 1
    #5-------------------------------------END----------------------------------------------

    #6--------------------------------Output to Excel---------------------------------------
    df = pd.DataFrame()

    counter = 0
    while counter <= len(workHeaders) -1 :
        
        df[workHeaders[counter] + "_Worksheet"] = dfList[counter][0]
        df[workHeaders[counter] + "_Datasheet"] = dfList[counter][1]
        df[workHeaders[counter] + "_Match"] = dfList[counter][2]
        counter += 1
        
    df.to_excel('output.xlsx')
    #6-------------------------------------END----------------------------------------------