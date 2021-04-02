# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 11:11:08 2020

@author: EddPineda
"""

from classes.dataPreprocessing import dataSet

# data fed in
import pandas as pd

dfIn = pd.read_csv('../dataset.csv') # this is fed in
kc = [0, 1, 2, 3, 4, 5] # this is fed in
kct = ['name', 'currency', 'date', 'int', 'float', 'time'] # this is fed in
# end data fed in

# casePara is left out of the class to allow changes to the datetime formats as/if needed
# the dataframe is left out of the class (for now) to ease add'l testing/debugging
cv = {'casePara' : {'text' : {'dta': []}, 
          'currency' : {'dta': []}, 
          'date' : {'dta': [], 'f': '%Y-%m-%d'},  
          'time' : {'dta': [], 'f': '%H:%M:%S'}, 
          'datetime' : {'dta': [], 'f': '%Y-%m-%d %H:%M:%S'}, 
          'datetimestamp' : {'dta': [], 'f': '%Y-%m-%d %H:%M:%S.%f'}, 
          'name' : {'dta': []}, 
          'float' : {'dta': [], 'f': ',', 'typ': 'float'}, 
          'intlfloat' : {'dta': [], 'f': '.', 'typ': 'float'}, 
          'int' : {'dta': [], 'f': ',', 'typ': 'int'}, 
          'intlint' : {'dta': [], 'f': '.', 'typ': 'int'}, 
          'category' : {'dta': []}
          }, 
      'kc' : kc, 
      'kct' : kct}

ds = dataSet(cv)

#dfOut = ds.cleanDFcols(ds.cleanData(ds.cleanColumns(ds.removeColumns(df, [i for i in list(range(0, len(df.columns))) 
#                            if i not in ds.kc]) if ds.kc != list(range(0, len(df.columns))) else df)))
dfOut = ds.dataProcess(dfIn)

del(ds)
