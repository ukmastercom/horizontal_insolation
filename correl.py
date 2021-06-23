#apply correlation
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import io
import os
import csv
from pandas import *

#%matplotlib inline


def cor():
    #read final_save
    df = pd.read_csv('final_save.csv')
    a=['v0','v1','v2','v3','v4','v5','v6','v7','v8','v9','v10','v11','v12','v13','v14','v15','v16','v17','v18']
    df_var=df[a]

    #applying correlation
    df_corr = df_var.corr()
    #df_corr.iloc[0]
    correlated_features = set()
    for i in range(len(df_corr .columns)):
        for j in range(1):
            if df_corr.iloc[i, j] > 0.81:
                colname = df_corr.columns[i]
                correlated_features.add(colname)

    #list correlation ans
    cf=list(correlated_features)

    #extract number from string and sort them
    stri=[]
    for x in range(0,len(cf)):
        d=cf[x]
        stri.append(d.split("v"))
    num = []
    for x in range(0,len(stri)):
        num.append(int(stri[x][1]))
    num.sort()
    #write csv corr_op.csv
    header=["date"]
    for x in num:
        k="v{x}".format(x=x)
        header.append(k)

    df_a = df[header]
    df_a.to_csv("corr_op.csv",header=header,index=False)
