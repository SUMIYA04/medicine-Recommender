from flask import Flask, request, render_template
import pickle
import pandas as pd
import bz2file as bz2

app = Flask(__name__)


def compressed_pickle(title, data):
    with bz2.BZ2File(title + '.pbz2', 'w') as f:
        pickle.dump(data, f)

def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = pickle.load(data)
    return data

medicines_dict = pickle.load(open('medicine_dict.pkl', 'rb'))
medicines = pd.DataFrame(medicines_dict)


similarity = decompress_pickle('similarity.pbz2')

def recommend(medicine):
    medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
    distances = similarity[medicine_index]
    medicines_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_medicines = []
    for i in medicines_list:
        recommended_medicines.append(medicines.iloc[i[0]].Drug_Name)
    return recommended_medicines

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    selected_medicine_name = None
    if request.method == 'POST':
        selected_medicine_name = request.form['medicine']
        recommendations = recommend(selected_medicine_name)
    return render_template('index.html', medicines=medicines['Drug_Name'].values, recommendations=recommendations, selected_medicine_name=selected_medicine_name)

if __name__ == '__main__':
    app.run(debug=True)
