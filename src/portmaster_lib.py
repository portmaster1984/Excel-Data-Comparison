from math import isnan

from pandas import array

class Portmaster_Lib:
  
    def printarray(a) -> array :
        
        for x in a :
            print(x)    
      

    def isClassNumber(a) -> int :
        if isinstance(a, float) == True and isnan(a) == False or isinstance(a, int) :
            return True


