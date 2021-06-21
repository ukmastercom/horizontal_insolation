#original project
#virtualenv env
#.\\env\Scripts\activate.ps1
#pip install flask flask-sqlalchemy
#pip install pandas
#python app.py
from flask import Flask, render_template, url_for, request, jsonify,send_file
import json
import csv
import pandas as pd
import solar
import fomatcsv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getlati',methods=["POST"])
def getlati():
    if request.method == 'POST':
        
        ##data = request.get_json(silent=True)
        ##print(data)
        ##with open("sample.json", "w") as outfile:
            ##outfile.write(data)
        ##return jsonify(data)
        #data = jsonify(data)
        value_lati = request.form.getlist('latikey[]')
        dfa = pd.DataFrame(value_lati,columns=["Latitudes"])
        dfa.to_csv('latitude.csv', index=False)
        return "ok"
        
@app.route('/getlongi',methods=["POST"])
def getlongi():
    if request.method == 'POST':
        value_longi = request.form.getlist('longikey[]')
        dfb = pd.DataFrame(value_longi,columns=["Longitudes"])
        dfb.to_csv('longitude.csv', index=False)
        solar.getvals()
        fomatcsv.convert()
        return "ok"
#def getinfo():
    # here we want to get the value of the key (i.e. ?key=value)
#    value = request.args.getlist('key[]')



#download csv on download_csv.html
#@app.route('/download')
#def download_file():
 #   p="final_save.csv"
  #  return send_file(p,as_attachment=True)


    

if __name__ == "__main__":
    app.run(debug=True)
