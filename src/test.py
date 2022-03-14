from cgitb import text
import re
from portmaster_lib import Portmaster_Lib as te

from packaging.version import Version, parse


v1 = parse("B.1")
v2 = parse("A.1.1")

print(v2<v1)



# filename = askopenfilename()USE THIS WHEN READY

#  #-----Removes all NaN and non numeric values--------------------------------------------
#     # note that list ONE is read as INT and list TWO is read as float
#     workColumns = [[]]

#     counter = 0
#     while counter < len(workHeaders) -1 :
#         for x in tempColumns[counter] :
#             if (isinstance(x, float) == True and isnan(x) == False) or isinstance(x, int):
#                 workColumns[counter].append(int(x))
        
#         counter += 1
#         workColumns.append([])

#     workColumns.pop(len(workColumns) - 1)
#     #--------------------------------------END----------------------------------------------







# #reading excel requires openpyxl
# import pandas as pd
# import re
# from math import isnan
# from tkinter.filedialog import askopenfilename
# from portmaster_lib import Portmaster_Lib as test

# def isnumber(a) -> int :
#         if isinstance(a, float) == True and isnan(a) == False or isinstance(a, int) :
#             return True

# class Main :

#     excelFile = pd.ExcelFile('example.xlsx')
#     read = pd.read_excel(excelFile, excelFile.sheet_names[0])
    

#     #1------Stores each COLUMN HEADER and for each COLUMN HEADER store its entire data in a dict-----
#     workHeaders = [x for x in read.columns]
    
#     storedColumns = []
#     for x in workHeaders[1: ] :
#         storedColumns.append(read[x])
        
#     #1-------------------------------------END----------------------------------------------

#     #2----Removes all NaN and non numeric values--------------------------------------------
#     # note that the listing i/o are floats AND ints
#     workColumns = {}

#     counter = 0
#     while counter < len(workHeaders) -1 :
#         tempColumns = []
#         for x in storedColumns[counter] :
#             if isnumber(x):
#                 tempColumns.append(int(x))
                
                
#         workColumns[workHeaders[counter + 1]] = tempColumns
#         counter += 1
        
    
    
#     #2-------------------------------------END-----------------------------------------------


#     read = pd.read_excel(excelFile, excelFile.sheet_names[1])

#      #3------Stores single COLUMN HEADER from "datasheet" and its entire data in an array-----
#     dataHeader = [x for x in read.columns]
#     storedColumns = read[dataHeader[0]]
    

#     #3-------------------------------------END-----------------------------------------------
    
#     #4----Stores targeted COLUMN HEADERS in each array-----------------------------------

#     dataColumns = {}
   
#     counter = 0
#     for x in workHeaders[1: ] :
#         tempColumns = []
#         for c in storedColumns :
#             if (re.search(workHeaders[counter +1], c)):
                
#                 tempRow = str(c).replace((workHeaders[counter + 1]+'_'),'')
#                 tempSplit = tempRow.split('_')
#                 if(str.isdigit(tempSplit[0])) :
#                     tempColumns.append(int(tempSplit[0]))
                
#         dataColumns[workHeaders[counter +1]] = tempColumns 
#         counter += 1
        

    
    
#     #4-------------------------------------END----------------------------------------------
    

    # #5-----Check if worksheet value is found in datasheet value------------------------------------------------------------------------------
 
    # dfList = []

    # counter = 0
    # for x in workHeaders[1: ]:
    #     dfList.append([])
    #     dfList[counter].append([])
    #     dfList[counter].append([]) 
    #     dfList[counter].append([]) 
    #     for c in reversed(workColumns[x]):
    #         dataCounter = len(dataColumns[x]) - 1
            
    #         while(c != dataColumns[x][dataCounter] and dataCounter >= 0) :
    #             dataCounter -= 1

    #         if c == dataColumns[x][dataCounter] :

    #             dfList[counter][0].append(c)
    #             dfList[counter][1].append(dataColumns[x][dataCounter])
    #             dfList[counter][2].append(True)
    #             dataColumns[x].pop(dataCounter)
    #         else :
            
    #             dfList[counter][0].append(c)
    #             dfList[counter][1].append('') 
    #             dfList[counter][2].append(False)

      
    #     counter += 1

    # df = pd.DataFrame(dfList)

    # df.to_excel('output.xlsx')

    # #5-------------------------------------END----------------------------------------------







def findMaxColumnLength(list) :
    temp = list
    maxLength = 0
    for x in list :

        if(len(temp[0]) > len(x[0])) :
            maxLength = max(temp[0], x[1])
        temp = x[1]
    
    return maxLength

  