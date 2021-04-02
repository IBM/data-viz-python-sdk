# -*- coding: utf-8 -*-
"""
Created: 2021-02-11
Updated:
Python: 3.7
@author: EddPineda
Version: 1.0
"""
#dataPreprocessing
dpca = {'casePara' : {'text' : {'dta': []},
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
          'category' : {'dta': []},
          'indcategory' : {'dta' : []},
          'nestcategory' : {'dta' : []},
          'subcategory' : {'dta' : []},
          'adjcategory' : {'dta' : []}
          }
        }