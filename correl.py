#apply correlation
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
import io
import os
import csv
from pandas import *
import seaborn as sns
import scipy.stats as stats
from numpy import loadtxt
from xgboost import XGBRegressor
from matplotlib import pyplot
#%matplotlib inline

def cor(mthd):
    #read final_save
    df = pd.read_csv('final_save_dates.csv')
    a=['v0','v1','v2','v3','v4','v5','v6','v7','v8','v9','v10','v11','v12','v13','v14','v15','v16','v17','v18']
    df_var=df[a]

    #applying correlation
    #df_corr = df_var.corr(method=mthod)
    #df_corr.iloc[0]
    if(mthd==1):
        df_corr = df_var.corr(method="pearson")
    elif(mthd==2):
        df_corr = df_var.corr(method="kendall")
    elif(mthd==3):
        df_corr = df_var.corr(method="spearman")
        #i think there is problem in the else code provided to me..... please take care...
    else:
        x3=df_var
        x3=np.array(x3)
        X = x3[:,0:18]
        y = x3[:,[18]]
        model = XGBRegressor()
        model.fit(X, y)
        df_corr=model.feature_importances_

    correlated_features = set()

    if(mthd!=4):
        for i in range(len(df_corr.columns)):
            for j in range(1):
                if df_corr.iloc[i, j] > 0.81:
                    colname = df_corr.columns[i]
                    correlated_features.add(colname)
    else:
        correlated_features.add("v0")
        for i in range(len(df_corr)):
            if df_corr[i] > 0.1:
                colname = "v{nm}".format(nm=(i+1))
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
    header=["year",'month','date']
    for x in num:
        k="v{x}".format(x=x)
        header.append(k)

    df_a = df[header]
    df_a.to_csv("corr_op.csv",header=header,index=False)
