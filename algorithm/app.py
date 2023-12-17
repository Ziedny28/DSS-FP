import os

import numpy as np
import pymongo
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from forms import *
from functions import *
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)

# Disable CSRF protection
app.config['WTF_CSRF_ENABLED'] = False


mongodb_url = os.getenv("MONGODB_URL")
cluster = MongoClient(mongodb_url)
db = cluster["dss-ahp"]
collection = db["history"]

#region routes
@app.route('/', methods=['GET'])
def home():
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
        data = request.get_json()

        alternatif = data['alternatif']
        bobot_kriteria = data['bobot_kriteria']

        alternatifs_point_per_criterias = []
        for alt in alternatif:
            for key, value in alt.items():
                # jika uncheck maka bernilai 1
                # jika checked bernilai 3
                if value == None:
                    value = 1
                if value == 'on':
                    value = 3
                alt[key] = value

            per_alt = {alt["nama"]:[alt["pengalaman_kerja"], alt["nilai"], alt["lokasi_kerja"], alt["pengalaman_organisasi"], alt["umur"], alt["ipk"]]}
            alternatifs_point_per_criterias.append(per_alt)

        all_criterias = list(bobot_kriteria.values())# all criterias
        print(all_criterias)
        all_criterias = [int(x) for x in all_criterias[0::1]] #make list data type integer
        print(all_criterias)
        
        # persiapan data
        criteria_length = len(all_criterias)

        alternatifs_point_per_criterias_values = []
        alternatifs_point_per_criterias_keys = []

        for alt in alternatifs_point_per_criterias:
            for key, value in alt.items():
                alternatifs_point_per_criterias_values.append(value)
                alternatifs_point_per_criterias_keys.append(key)

        alternatif_count = len(alternatifs_point_per_criterias)

        alternatifs_point_per_criterias_values = [int(x) if isinstance(x, str) else x for x in alternatifs_point_per_criterias_values] #if its string then convert to int

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

        final_decision = [(key, value) for key, value in final_decision.items()] # make a list of (key, value)

        # masukin data ke db
        history_data = {
            "final_decision":final_decision,
            "alternatifs_point_per_criterias": alternatifs_point_per_criterias,
            "title": data['judul']
        }

        collection.insert_one(history_data)


        #NOTE:kalau mau return json harus tolist()
        return jsonify({
            'pw': main_pw.tolist(),
            'pw_alt_per_criteria': pw_per_criteria.tolist(),
            # 'test_pw' : test_pw.tolist(),
            'final_decision': final_decision
        })
    
    except Exception as e:
        error_message = str(e)
        print(error_message)
        return jsonify({'error': error_message}), 400  # You can customize the error response code

# TODO: Implement history, setelah melakukan perhitungan masukkan ke database dan simpan history dari value input ke hasil akhir
@app.route('/history', methods=['GET'])
def history():
    histories = collection.find({}) #get data
    return render_template('history.html', histories=histories)

# TODO: implement delete history
@app.route('/delete-history', methods=['POST'])
def delete_history():
    data =  request.get_json()
    title = data["title"]
    collection.delete_one({'title':title})
    return jsonify({'message': 'deleted successfully'}), 200

#endregion

if __name__ == '__main__':
    app.run(debug=True)