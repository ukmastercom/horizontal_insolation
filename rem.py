import os

def unwanted():
    for x in range(0,19):
        f_name = "request_data_{x}.csv".format(x=x)
        os.remove(f_name)
        #f_n = "save_data_{x}.csv".format(x=x)
        #os.remove(f_n)
    os.remove("final_save.csv")
    #os.remove("latitude.csv")
    #os.remove("longitude.csv")
