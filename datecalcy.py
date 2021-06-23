import pandas as pd
from datetime import date



def diff():
    df=pd.read_csv("dates.csv")
    data=df['dates'].tolist()
    sdate=data[0]
    edate=data[1]
    sdate=sdate.split('-')
    edate=edate.split('-')
    s_y=int(sdate[0])
    s_m=int(sdate[1])
    s_d=int(sdate[2])
    e_y=int(edate[0])
    e_m=int(edate[1])
    e_d=int(edate[2])
    d0 = date(s_y,s_m,s_d)
    d1 = date(e_y,e_m,e_d)
    delta = d1 - d0
    return delta