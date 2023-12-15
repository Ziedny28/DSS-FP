import numpy as np
from markupsafe import Markup


def get_final_decision(criteria_length, main_pw, pw_per_criteria, alternatif_names):
    final_decision = {}

    for i, alternatif_name in enumerate(alternatif_names):
        total = 0
        for j in range(criteria_length):
            total += (pw_per_criteria[j][i] * main_pw[j])
        final_decision[alternatif_name] = total
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


# def unpack(field, name, id):
#     if isinstance(field, str):
#         # Handle string case (e.g., return empty Markup)
#         return Markup("")
#     else:
#         return Markup(field.name, field.id)
