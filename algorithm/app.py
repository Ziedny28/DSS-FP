import numpy as np
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from forms import *
from functions import *

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret_key'

CORS(app)  # Enable CORS for all routes
csrf = CSRFProtect(app)


#region routes
@app.route('/', methods=['GET'])
def home():
    # csrf_token = csrf.generate_csrf_token(app)
    form = Form()
    return render_template('index.html', form=form)
    

@app.route('/ahp', methods=['POST'])
def ahp():

    data = request.get_json()
    # get data
    all_criterias = data['all_criterias']
    criteria_length = data['criteria_length']
    alternatifs_point_per_criterias = data['alternatifs_point_per_criterias']
    alternatifs_point_per_criterias_values = list(alternatifs_point_per_criterias.values())
    alternatifs_point_per_criterias_keys = list(alternatifs_point_per_criterias.keys()) 
    alternatif_count = len(alternatifs_point_per_criterias)

    if len(all_criterias) != criteria_length:
        return jsonify({'error': 'An error occurred', 'message': f'all_criterias count is not {criteria_length}'}), 400

    #(pw criteria 1, pw criteria 2, pw criteria 3,...pw  criteria n)
    main_pw = priority_weight(criteria_length,all_criterias)

# correct way
#  (criteria 1:alt 1,alt 2,alt 3... alt n)
    pw_per_criteria = np.zeros((criteria_length, alternatif_count))
    for i in range(criteria_length):
        temp = np.zeros(alternatif_count)
        for j in range(alternatif_count):
            temp[j] = alternatifs_point_per_criterias_values[j][i]
        pw_per_criteria[i] = priority_weight(alternatif_count, temp)

    final_decision = get_final_decision(criteria_length,main_pw,pw_per_criteria,alternatifs_point_per_criterias_keys)

    #NOTE:kalau mau return json harus tolist()
    return jsonify({
        'pw': main_pw.tolist(),
        'pw_alt_per_criteria': pw_per_criteria.tolist(),
        # 'test_pw' : test_pw.tolist(),
        'final_decision': final_decision
    })

@app.route('/test', methods=['POST'])
def test():
    try:

        data = request.json

        # Process the JSON data as needed
        # For example, you can access individual fields like this:
        bobot_pengalaman_kerja = data['bobot_kriteria']['pengalaman_kerja']
        bobot_skill = data['bobot_kriteria']['bobot_skill']
        
        # ... process other fields ...

        # You can then return a response, for example:
        response_data = {'message': 'Data received successfully'}
        return jsonify(response_data)
    
    except Exception as e:
        # Handle any exceptions that might occur during processing
        error_message = str(e)
        print(error_message)
        return jsonify({'error': error_message}), 400  # You can customize the error response code


#endregion

if __name__ == '__main__':
    app.run(debug=True)