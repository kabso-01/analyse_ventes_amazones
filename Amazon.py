# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 14:39:38 2026

@author: EL RAY KABSO
"""

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
#import de la dataset
df = pd.read_csv("amazon.csv")

#print(f'Shape : {df.shape}')           
#print(df.dtypes)
#print(df.isnull().sum())
#nettoyage des données 
#df = df.drop_duplicates()
print(df.columns)
#df = df.dropna(subset=['price', 'quantity'])
