import numpy as np
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    msg = {'msg': 'welcome to AHP application, send data in post request to /ahp'}
    return jsonify(msg)

@app.route('/ahp', methods=['POST'])
def ahp():
    data = request.get_json()

    # count criteria start
    all_criterias = data['all_criterias']

    if len(all_criterias) != 6:
        return jsonify({'error': 'An error occurred', 'message': 'all_criterias count is not 6'}), 400

    criteria_length = 6
    table_criteria = np.zeros((criteria_length, criteria_length))
    for i in range(criteria_length):
        for j in range(criteria_length):
            table_criteria[i][j] = all_criterias[i] / all_criterias[j] 

    jumlah = np.zeros(criteria_length)
    for i in range(criteria_length):
        for j in range(criteria_length):
            jumlah[i] +=  table_criteria[j][i]
    
    normalisasi = np.zeros((criteria_length, criteria_length))
    for i in range(criteria_length):
        for j in range(criteria_length):
            normalisasi[i][j] = table_criteria[i][j] / jumlah[i]

    pw = np.zeros(criteria_length)
    for i in range(criteria_length):
        pw[i] = np.sum(normalisasi[i]) / criteria_length
    

    #NOTE:kalau mau return json harus tolist()
    return jsonify({
        'all_criterias': all_criterias,
        'table_criteria': table_criteria.tolist(),
        'jumlah': jumlah.tolist(),
        'normalisasi': normalisasi.tolist(),
        'pw': pw.tolist()
    })

if __name__ == '__main__':
    app.run(debug=True)