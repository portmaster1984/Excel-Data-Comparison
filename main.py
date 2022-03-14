import pandas as pd
import re
from math import isnan
from tkinter.filedialog import askopenfilename
from packaging.version import parse
import openpyxl as pxl
from tkinter import Tk, filedialog
import tkinter.messagebox as mes

def isnumber(a) -> int :
        if isinstance(a, float) == True and isnan(a) == False or isinstance(a, int) :
            return True

def findMaxColumnLength(list, args = None) -> int :
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
    
    if args is not None :
        if(len(args) > maxLength) :
            maxLength = len(args)
    
    return maxLength

def checkDataListing(columnHeaders: list, dataToBeCompared: list, againstThisData : list) -> list :
   
    
    list = []
    
    counter = 0
    for x in columnHeaders:
        list.append([])
        list[counter].append([])
        list[counter].append([]) 
        list[counter].append([]) 
        for c in reversed(dataToBeCompared[x]):
            comparedDataCounter = len(againstThisData[x]) - 1
            
            while(c != againstThisData[x][comparedDataCounter] and comparedDataCounter >= 0) :
                comparedDataCounter -= 1
   
                
                
            if c == againstThisData[x][comparedDataCounter] :

                list[counter][0].append(c)
                list[counter][1].append(againstThisData[x][comparedDataCounter])
                list[counter][2].append(True)
                againstThisData[x].pop(comparedDataCounter)
            else :
            
                list[counter][0].append(c)
                list[counter][1].append('NULL') 
                list[counter][2].append(False)

        list[counter][0].append('ERROR IF SHOWN REPORT')
        list[counter][1].append('ERROR IF SHOWN REPORT')
        list[counter][2].append('ERROR IF SHOWN REPORT')
        counter += 1

    

    return list

def checkEmptyListing(workList, dataList): #IGNORE THIS

    emptyList = False
    for x in workList:
        if len(x) == 0:
            emptyList = True
    
    for x in dataList:
        if len(x) == 0:
            emptyList = True
    if emptyList:
        mes.showerror('error', 'ONE OF YOUR COLUMNS WERE NOT FOUND IN EITHER SHEET. Check your listing! ')
        raise ValueError('ERROR: ONE OF YOUR COLUMNS WERE NOT FOUND IN EITHER SHEET. Check your listing')
    

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

    
    versionList = [[],[]]
    versionList[0].append("N/A")
    versionList[1].append("N/A")
    versionList[1].append("N/A")
    counter = 0
    for x in versionColumn[0:len(versionColumn) -1]:
 
        versionList[0].append(x)
        if(parse(x) < parse(versionColumn[counter + 1])):            
            versionList[1].append(True)
        else:
            versionList[1].append(False)
        counter +=1      
    
    versionList[0].append(versionColumn[len(versionColumn) - 1])
    return versionList 

def populateDataList(workHeaders, storedTempColumns):
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
    
    return dataColumns

class Main :
    filename = askopenfilename()
    excelFile = pd.ExcelFile(filename)
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


    dataColumns = populateDataList(workHeaders, storedTempColumns)
    dataColumns2 = populateDataList(workHeaders, storedTempColumns)
  
    #3-------------------------------------END----------------------------------------------
    
    #5-----Check validation ------------------------------------------------------------------------------
    dfWorkList = checkDataListing(workHeaders, workColumns, dataColumns)
    dfDataList = checkDataListing(workHeaders, dataColumns2, workColumns)
    #5-------------------------------------END----------------------------------------------
    
    #6--------------------------------Output to Excel---------------------------------------
    dfWorkSheet = pd.DataFrame()
    dfWorkSheet.index = range(1, findMaxColumnLength(dfWorkList, args = versionColumn[0]) + 1)

    #creates worksheet dataframe
    counter = 0
    while counter <= len(workHeaders) -1 :
        dfWorkSheet[workHeaders[counter] + "_Worksheet"] = pd.Series(reversed(dfWorkList[counter][0]))
        dfWorkSheet[workHeaders[counter] + "_Datasheet"] = pd.Series(reversed(dfWorkList[counter][1]))
        dfWorkSheet[workHeaders[counter] + "_Match"] = pd.Series(reversed(dfWorkList[counter][2]))
        counter += 1
        
    dfWorkSheet['Version'] = pd.Series(versionColumn[0])
    dfWorkSheet['Checked'] = pd.Series(versionColumn[1])
    

    #creates datasheet dataframe
    dfDataSheet = pd.DataFrame()
    dfDataSheet.index = range(1, findMaxColumnLength(dfDataList) + 1)

    counter = 0
    while counter <= len(workHeaders) -1 :
        dfDataSheet[workHeaders[counter] + "_Datasheet"] = pd.Series(reversed(dfDataList[counter][0]))
        dfDataSheet[workHeaders[counter] + "_WorkSheet"] = pd.Series(reversed(dfDataList[counter][1]))
        dfDataSheet[workHeaders[counter] + "_Match"] = pd.Series(reversed(dfDataList[counter][2]))
        counter += 1
        

    #create excel and append sheet
    root = Tk() 
    root.withdraw() 
    root.attributes('-topmost', True) 
    open_file = filedialog.askdirectory() + r"/"

    fileOutput = 'output.xlsx'
    dfWorkSheet.to_excel(open_file + fileOutput, sheet_name = "Work_form")
    
    ExcelWorkbook = pxl.load_workbook(open_file + fileOutput)
    options = {}
    options['strings_to_formulas'] = False
    options['strings_to_urls'] = False
    writer = pd.ExcelWriter(open_file + fileOutput, engine = 'openpyxl')
    writer.book = ExcelWorkbook
    dfDataSheet.to_excel(writer, sheet_name = "Data_form")

    writer.close()

    excel_book = pxl.load_workbook(open_file + fileOutput)

    
    
    #6-------------------------------------END----------------------------------------------