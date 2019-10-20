from flask import Flask, render_template, request, jsonify, url_for
from testFunctions import rList
import pandas as pd
import json
from pandas.io.json import json_normalize

from Program_Functions import main, save_user_choice



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/parse_data", methods=["GET", "POST"])
def parse_data():
    if request.method == "POST":
        data = request.json

        budget = data['budget']
        zipCode = data['zipCode']

        rlist = main(budget, zipCode)
        print(rlist)
        rstring = json.dumps(rlist)
        print(type(rstring))
        #rstring = json_normalize(rlist['list'])
        return rstring
    else:
        return render_template('index.html')

@app.route("/chosenData", methods=["GET", "POST"])
def chosenData():
    if request.method == "POST":

        
        data = request.json
        rstring = data["restList"]
        save_user_choice(rstring)

        #print(rstring)
        #rstring = json_normalize(rlist['list'])
        return ""
    else:
        return render_template('index.html')



if __name__== '__main__':
    app.run


if __name__ == '__main__':
    app.run(debug=True)

