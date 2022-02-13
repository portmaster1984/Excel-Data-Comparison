#reading excel requires openpyxl
from dataclasses import dataclass
from tabnanny import check
import pandas as pd
import re
from math import isnan
from tkinter.filedialog import askopenfilename

from portmaster_lib import Portmaster_Lib as test
from work_column_data import Work_Column_Data

class Main :
 


    excelFile = pd.ExcelFile(askopenfilename())
    read = pd.read_excel(excelFile, excelFile.sheet_names[0])
    

    #1------Stores each COLUMN HEADER and for each COLUMN HEADER store its entire data in a dict-----
    workHeaders = [x for x in read.columns]
    
    tempColumns = []
    for x in workHeaders[1: ] :
        tempColumns.append(read[x])
    #1-------------------------------------END----------------------------------------------

    #2----Removes all NaN and non numeric values--------------------------------------------
    # note that the listing i/o are floats AND ints
    workColumns = [{}]

    counter = 0
    while counter < len(workHeaders) -1 :
        for x in tempColumns[counter] :
            if (isinstance(x, float) == True and isnan(x) == False) or isinstance(x, int):
                workColumns[counter][int(x)] = workHeaders[counter + 1]
        
        counter += 1
        workColumns.append({})

    workColumns.pop(len(workColumns) - 1)
    #2-------------------------------------END-----------------------------------------------


    read = pd.read_excel(excelFile, excelFile.sheet_names[1])

     #3------Stores single COLUMN HEADER from "datasheet" and its entire data in an array-----
    dataHeader = [x for x in read.columns]
    tempColumns = read[dataHeader[0]]
    

     #3-------------------------------------END-----------------------------------------------
    
    #4----Stores targeted COLUMN HEADERS in each array-----------------------------------

    dataColumns = [{}]
   
    counter = 0
    for x in workHeaders[1: ] :
        for n in tempColumns :
            if(re.search(workHeaders[counter +1], n)):
                dataColumns[counter][n] = workHeaders[counter +1]
        counter += 1
        dataColumns.append({})
    dataColumns.pop(len(dataColumns) -1)



    print(dataColumns)