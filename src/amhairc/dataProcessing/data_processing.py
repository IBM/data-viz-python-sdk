# -*- coding: utf-8 -*-
"""
Created: 2020-11-02
Updated: 2021-02-11
Python: 3.7
@author: EddPineda
Version 1.0.3

The attributes and their purpose for the class are:
    casePara - the parameters dictionary for the "select case/switch" method - needs to
               stay in alignment case
    case     - the different data types dictionary and the method to use to process the data
    kc       - the indexes of the dataframe columns to be used as a list
    kct      - the column data type for the used data frame columns as a list
    featStrt - the column in the dataframe where the features start
    spell    - the spell checker

The methods for the class are:
    na              - do nothing with the data (needed for case/switch logic and takes the following parameters:
                      dta    - dataframe column data as a list or series
    removeColumns   - removes the unused columns in the dataframe and takes the following parameters:
                      df     - the dataframe
    cleanColumns    - cleans the column names (strips white space & changes to title format) and takes the following parameters:
                      df     - the dataframe
                      s      - optional (required if r != '') - the search string to search for a specific character/s to replace
                      r      - optional - the replacement for s
    cleanData       - strips the white space from the dataframe data and takes the following parameters:
                      df     - the dataframe
    dateChecker     - the "parent" method for dateFinder that handles date and time data it takes the following parameters:
                      dta    - dataframe column data as a list or series
                      f      - the format for the given date/time data ex: '%Y-%m-%d %H:%M:%S.%f'
    dateFinder      - converts given date time value to the desired format and takes the following parameters:
                      s      - date/time value as a string
                      f      - format for the date/time
    currencyCleaner - converts to a float regardless if US or International and takes the following parameters:
                      dta    - dataframe column data as a list or series
    spellChecker    - spell checks and updates text data and takes the following parameters:
                      dta    - dataframe column data as a list or series
    numberChecker   - the parent method for floatChecker and intChecker and takes the following parameters:
                      dta    - dataframe column data as a list or series
    floatChecker    - checks the given value presented as a string to see if it's a float and takes the following parameters:
                      s      - value as string
    intChecker      - checks the given value presented as a string to see if it's an integer and takes the following parameters:
                      s      - value as string
    dfDataClean     - the select case/switch method directs data to the correct data cleaner it takes the following parameters:
                      fun    - the name of the method to be used as string
                      para   - the parameters to be used for the given method
    cleanDFcols     - assesses the dataframe columns and validates the data - it takes the following parameters:
                      df     - the dataframe
    dataProcess     - performs the task to prep the dataframe data for visualization and takes the following parameters:
                      df     - the dataframe
"""
import numpy as np
#from autocorrect import Speller
from spellchecker import SpellChecker
from dateutil.parser import parse
from money_parser import price_str
import logging
import pandas as pd

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

class DataProcess:
    def __init__(self,dataframe):
        self.dataframe = dataframe
        self.cleaned_dataframe = self.clean_normalise_data()
        self.data_types = self.get_datatypes_dict()
        self.data_types_strings = self.get_datatypes_strings()


    def clean_normalise_data(self):
        logging.info("clean and normalise data")
        cleaned_dataframe = self.dataframe
        return cleaned_dataframe


    def get_datatypes_dict(self):
        logging.info("get data types dict")
        dataTypes = dict(self.dataframe.dtypes)
        return dataTypes


    def get_datatypes_strings(self):
        logging.info("get data types string")

        data_types = []
        for col in self.dataframe.columns:
            data_type = self.dataframe.dtypes[col]
            data_types.append(data_type)

        return data_types


class DataDefinition:
    def __init__(self,data_location,selected_rows):
        self.data_location = data_location
        self.selected_rows = selected_rows


    def get_pandas_dataframe(self):
        logging.info("get pandas dataframe")
        dataframe = pd.read_csv(self.data_location)#,usecols=self.selected_rows)
        return dataframe


class DataPreProcessing:
    def __init__(self, cv):
        self.__dict__.update(**cv)
        self.__dict__.update(**dpca)
        self.case = {'text' : self.spellChecker,
                     'currency' : self.currencyCleaner,
                     'date' : self.dateChecker,
                     'time' : self.dateChecker,
                     'datetime' : self.dateChecker,
                     'datetimestamp' : self.dateChecker,
                     'name' : self.na,
                     'float' : self.numberChecker,
                     'intlfloat' : self.numberChecker,
                     'int' : self.numberChecker,
                     'intlint' : self.numberChecker,
                     'category' : self.na,
                     'indcategory' : self.na,
                     'nestcategory' : self.na,
                     'subcategory' : self.na,
                     'adjcategory' : self.na
                     }
        #self.spell = Speller(lang='en')
        self.spell = SpellChecker()
        print('data preprocessing class initiated')

    def __del__(self):
        print('data preprocessing class destroyed')

    def na(self, dta):
        return dta

    def removeColumns(self, df):
        df.drop(df.columns[[i for i in list(range(0, len(df.columns))) if i not in self.kc]], axis = 1, inplace = True)
        return df

    def cleanColumns(self, df, s = '', r = ''):
        if (r == ''):
            df.columns = [''.join(e for e in c.title() if e.isalnum()) for c in df.columns]
        else:
            df.columns = [c.title().replace(s, r) for c in df.columns.str.strip()]

        return df

    def cleanData(self, df):
        return df.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)

    def dateChecker(self, dta, f):
        return [self.dateFinder(s, f) for s in dta]

    def dateFinder(self, s, f):
        try:
            return parse(s, fuzzy_with_tokens = False).strftime(f)
        except:
            return None

    def currencyCleaner(self, dta):
        return [price_str(e, default=None) for e in dta]

    def spellChecker(self, dta):
        return [self.spell.correction(e) if e != None else None for e in dta]

    def numberChecker(self, dta, f, typ):
        return [self.floatChecker(s) for s in dta.str.replace(f, '')] if typ == 'float' else [self.intChecker(s) for s in dta.str.replace(f, '')]

    def floatChecker(self, s):
        try:
            return float(s) if (~np.isnan(float(s)) and ~np.isinf(float(s))) else None
        except:
            return None

    def intChecker(self, s):
        try:
            return int(float(s))
        except:
            return None

    def dfDataClean(self, fun, para):
        func = self.case.get(fun, lambda: 'Invalid Type')

        return func(**para)

    def cleanDFcols(self, df):
        for i, c in enumerate(df.columns):
            td = self.casePara[self.kct[i]].copy()
            td['dta'] = df[c].astype('str')
            df[c] = self.dfDataClean(self.kct[i], td)

        return df

    def dataProcess(self, df):
        return self.cleanDFcols(self.cleanData(self.cleanColumns(self.removeColumns(df) if self.kc != list(range(0, len(df.columns))) else df)))
