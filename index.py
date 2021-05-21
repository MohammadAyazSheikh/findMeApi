import flask
from flask import request, jsonify
import aiModel
import excelPython
import json


app = flask.Flask(__name__)
# app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '''<h1>FindME AI API</h1>
<p>Created By Ayaz and Uzair.</p>'''

# --------------------------------------------------------------------------------------------
@app.route('/postSchedule', methods=['POST'])
def postSchedule():

    data = request.get_json()

    # print(data)
    
    try:
        excelPython.addValues(data['uId'], data['city'], data['hour'])
        return jsonify({'succes': True})
    except:
        return jsonify({'succes':False})
# ------------------------------------------------------------------------------------------------

@app.route('/postInitialData', methods=['POST'])
def postInitialData():

    data = request.get_json()

    # print(data)
    
    try:
        excelPython.addInitialData(data['uId'], data['initialData'])
        return jsonify({'succes': True})
    except:
        return jsonify({'succes':False})

# ----------------------------------------------------------------------------------------------

@app.route('/getSchedule', methods=['GET'])
def getSchedule():

    if 'hour' in request.args and 'uId' in request.args and 'num' in request.args :
        hr = int(request.args['hour'])
        uId = str(request.args['uId'])
        num = int(request.args['num'])
        print("\nUser id is "+str(uId))
    else:
        return "Error: No hour field provided. Please specify an hour."

    data  = {}
    try:
        filename = 'user '+str(uId) + ' file.xlsx'
        results = aiModel.getRecommendations(Hour=hr, Num=num, FileName=filename)
        
        data = {
            'result':results,
            'succes':True
        }

    except:
        print("An exception occurred")
        data = {
            'succes':False
        }

    
    return jsonify(data)

# --------------------------------------------------------------------------------------------------------
@app.route('/getScheduleAll', methods=['GET'])
def getScheduleAll():

    if 'uId' in request.args and 'num' in request.args :
        uId = str(request.args['uId'])
        num = int(request.args['num'])
        print("\nUser id is "+str(uId))
    else:
        return "Error: No hour field provided. Please specify an hour."  

    data  = {}
    allData = []
    try:
        for x in range(0,24):
           
            filename = 'user '+str(uId) + ' file.xlsx'
            results = [] 
            try:
                results = aiModel.getRecommendations(Hour=x, Num=num, FileName=filename)
            except:
                results = ["no enough data "]
            var = {
                "place":results[0],
                "time":x
                }
            allData.append(var)
        data = {
            'result':allData,
            'succes':True
        }

    except:
        print("An exception occurred")
        data = {
            'succes':False
        }

    
    return jsonify(data)

# app.run()
# app.run(host= '0.0.0.0') 
# app.run(host= '192.168.0.2')
if __name__ == "__main__":
    app.run()#(debug=False,host='0.0.0.0')