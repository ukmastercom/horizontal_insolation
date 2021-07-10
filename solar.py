#import nasa info
import pandas as pd
import numpy as np
import sys,os
from IPython.display import display
import requests
import csv
import json
from pandas import *
from datetime import date
import numpy as np

i=0
value=[]
value_int_a=[]
value_int_b=[]
j=0

#this import lat and long and save in csv the requested
def getvals():
    i=0
    j=0
    def req_data(s_d,e_d):
        global i
        if i>18:
            i=0
        data = read_csv("latitude.csv")
        lt = data['Latitudes'].tolist()
        data = read_csv("longitude.csv")
        lng = data['Longitudes'].tolist()
        for x in range(0,19):
            lat = lt[x]
            long = lng[x]
            #GET https://power.larc.nasa.gov/cgi-bin/v1/DataAccess.py?&request=execute&identifier=SinglePoint&parameters=ALLSKY_SFC_SW_DWN&startDate=20150101&endDate=20150305&userCommunity=SSE&tempAverage=DAILY&outputList=CSV&lat=23.5000&lon=78.0000
            url = 'https://power.larc.nasa.gov/cgi-bin/v1/DataAccess.py?&request=execute&identifier=SinglePoint&parameters=ALLSKY_SFC_SW_DWN&startDate={s_d}&endDate={e_d}&userCommunity=SSE&tempAverage=DAILY&outputList=CSV&lat={lat}&lon={long}'.format(s_d=s_d,e_d=e_d,lat=lat,long=long)
            r = requests.get(url = url)
            #set filename
            f_name="request_data_{i}.csv".format(i=i)
            i=i+1
            #save in csv
            a = r.content
            csv_file = open(f_name, 'wb')
            csv_file.write(a)
            csv_file.close()

    #save date and their value in csv
    def writetocsv():
        header = ['date','value']
        global j
        if j>18:
            j=0
        file_name="save_data_{j}.csv".format(j=j)
        
        with open(file_name, 'w',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(zip(value_int_a, value_int_b))
        #this will clear lists
        j=j+1
        value.clear()
        value_int_a.clear()
        value_int_b.clear()
        

    #request data from csv store into a string
    def read_send_csv(delta):
        for x in range(0,19):
            file_name="request_data_{x}.csv".format(x=x)
            with open(file_name, newline='') as f:
                reader = csv.reader(f)
                data = list(reader)
                #data_list = data[14:7319]
                for a in range(14,delta+15):
                    s = str(data[a])
                    s=s.translate({ord(' '): None,ord('['): None,ord(']'): None,ord('"'): None,ord(','): None,ord("'"): None})
                    s=s.split(':')
                    value.append(s)
            #for b in range(0,7304):
            #    dte = int(value[b][0])
            #   val = float(value[b][1])
            #  value_int_a.append(dte)
            # value_int_b.append(val)
                #f.close()
            #writetocsv()
            for b in range(0,(delta+1)):
                dte = value[b][0]
                dte=int(dte)
                value_int_a.append(dte)
                val = value[b][1]
                val=float(val)
                value_int_b.append(val)
            writetocsv()
            f.close()
                #tobeadd1.append(int(tobeadd[a][0]))
                #tobeadd2.append(float(tobeadd[0][a]))
    df=pd.read_csv("dates.csv")
    data=df['dates'].tolist()
    sdate=data[0]
    edate=data[1]
    sdate=sdate.split('-')
    edate=edate.split('-')
    st_y=sdate[0]
    st_m=sdate[1]
    st_d=sdate[2]
    ed_y=edate[0]
    ed_m=edate[1]
    ed_d=edate[2]
    s_d=st_y+st_m+st_d
    e_d=ed_y+ed_m+ed_d
    st_y=int(sdate[0])
    st_m=int(sdate[1])
    st_d=int(sdate[2])
    ed_y=int(edate[0])
    ed_m=int(edate[1])
    ed_d=int(edate[2])

    d0 = date(st_y,st_m,st_d)
    d1 = date(ed_y,ed_m,ed_d)
    delta = d1 - d0
    delta=delta.days
    req_data(s_d,e_d)            
    read_send_csv(delta)
