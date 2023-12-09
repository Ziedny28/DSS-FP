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
    # get data
    all_criterias = data['all_criterias']
    criteria_length = data['criteria_length']
    alternatifs_point_per_criterias = data['alternatifs_point_per_criterias']
    alternatif_count = len(alternatifs_point_per_criterias)

    if len(all_criterias) != criteria_length:
        return jsonify({'error': 'An error occurred', 'message': f'all_criterias count is not {criteria_length}'}), 400

    main_pw = priority_weight(criteria_length,all_criterias)
    
    # index = 0
    # pw_per_criteria = np.zeros((alternatif_count, criteria_length))
    # for point_per_criteria in alternatifs_point_per_criterias:
    #     if len(point_per_criteria) != criteria_length:
    #         return jsonify({'error': 'An error occurred', 'message': f'alternatifs_point_per_criterias count is not {criteria_length}'}), 400
    #     pw_per_criteria[index] = priority_weight(criteria_length, point_per_criteria)
    #     index +=1

# correct way
    # index = 0
    # pw_per_criteria = np.zeros((criteria_length,alternatif_count))
    # for point_per_criteria in alternatifs_point_per_criterias:
    #     if len(point_per_criteria) != criteria_length:
    #         return jsonify({'error': 'An error occurred', 'message': f'alternatifs_point_per_criterias count is not {criteria_length}'}), 400
    #     pw_per_criteria[index] = priority_weight(alternatif_count, point_per_criteria)
    #     index +=1

    test_pw = priority_weight(5,[6,6,6,6,6])

# correct way
    pw_per_criteria = np.zeros((criteria_length, alternatif_count))
    for i in range(criteria_length):
        temp = np.zeros(alternatif_count)
        for j in range(alternatif_count):
            temp[j] = alternatifs_point_per_criterias[j][i]
        pw_per_criteria[i] = priority_weight(alternatif_count, temp)

    # TODO: cek apakah ini benar?
    final_decision = get_final_decision(alternatif_count,criteria_length,main_pw,pw_per_criteria)


    #TODO: implement pengambilan keputusan 
    # TODO: cek mana yang bener? 

    #TODO: (optional)implement consistency_ratio
    """
consistency_ratio = np.zeros(criteria_length)
for i in range(criteria_length):
    for j in range(criteria_length):
        consistency_ratio[i] += (table_criteria[i][j] * pw[j])

# langkah ini opsional
cr_per_pw = np.zeros(criteria_length)
for i in range(criteria_length):
    cr_per_pw[i] = consistency_ratio[i] / pw[i]

lambda_max = sum(cr_per_pw)/criteria_length
    """
    #NOTE:kalau mau return json harus tolist()
    return jsonify({
        'pw': main_pw.tolist(),
        'pw_per_criteria': pw_per_criteria.tolist(),
        'test_pw' : test_pw.tolist(),
        'final_decision': final_decision.tolist()
    })


def get_final_decision(alternatif_count,criteria_length,main_pw,pw_per_criteria):
    final_decision = np.zeros(alternatif_count)
    for i in range(alternatif_count):
        for j in range(criteria_length):
            final_decision[i] += (main_pw[j] * pw_per_criteria[j][i])  
    
    return final_decision


def priority_weight(criteria_length,initial_value):

    """
    this function will return priority weight as list,
    param: (criteria length, value in one dimention array)
    """

    # ini menyamping
    table = np.zeros((criteria_length, criteria_length))
    for i in range(criteria_length):
        for j in range(criteria_length):
            table[i][j] = initial_value[i] / initial_value[j] 
    
    jumlah = np.zeros(criteria_length)
    for i in range(criteria_length):
        for j in range(criteria_length):
            jumlah[i] +=  table[j][i]
    
    # ini kebawah 
    normalisasi = np.zeros((criteria_length, criteria_length))
    for i in range(criteria_length):
        for j in range(criteria_length):
            normalisasi[i][j] = table[j][i] / jumlah[i]

    pw = np.zeros(criteria_length)
    for i in range(criteria_length):
        tot = 0
        for j in range(criteria_length):
            tot += normalisasi[j][i]
        
        tot /= criteria_length
        pw[i] = tot
    
    return pw

def evaluation_weight(criteria_length,main_pw,pw_per_criteria):
    result = np.zeros(len(pw_per_criteria[0]))
    for i in range(criteria_length):
        for j in range(len(pw_per_criteria[0])):
            result[i] += pw_per_criteria[j][i] * main_pw[j]
    
    return result

if __name__ == '__main__':
    app.run(debug=True)