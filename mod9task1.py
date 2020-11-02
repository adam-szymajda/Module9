import requests
import csv
import pickle
import os
import time
from time import sleep
from flask import Flask, render_template, request, redirect



app = Flask(__name__)

# def create_csv():
#     with open("xe.csv", mode="w") as f:
#         fieldnames = ['currency', 'code', 'bid', 'ask']
#         writer = csv.DictWriter(f, delimiter=';', fieldnames=fieldnames)
#         for currency in data[0]['rates']:
#             writer.writerow(currency)

def create_pickle_cache(data, filename):
    with open(filename, mode="wb") as f:
        pickle.dump(data, f)

def read_pickle_cache(path):
    with open(path, mode="rb") as f:
        content = pickle.load(f)
    return content

def clear_cache(filename, folder):
    path = os.path.join(folder, filename)
    # if path and (time.time() - os.path.getatime(path) > limit * 60):
    #     print("Clearing cache")
    #     os.remove(path)
    print("Clearing cache")
    os.remove(path)

def load_data(filename, folder):
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        print("No cache, fetching from API")
        response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
        api_output = response.json()
        create_pickle_cache(api_output, path)
        return api_output
    else:
        print("Fetching cached data")
        return read_pickle_cache(path)




# data = load_data("xe.pickle", "cache")



@app.route("/xe/", methods=['GET', 'POST'])
def currency_exchange():
    errors = []
    select_data = [x['code'] for x in data[0]['rates']]
    if request.method == "GET":
        tab = 'Dane'
        return render_template('xe.html', currency_list=select_data, tab=tab)
    if request.method == 'POST':
        try:
            qty = float(request.form['qty'])
            select = request.form.get('currency')
            for currency in data[0]['rates']:
                if currency['code'] == select:
                    # return f"Należność w PLN: {qty*currency['ask']}"
                    return render_template('xe.html', currency_list=select_data, errors=errors, tab='Do zapłaty', to_pay=qty*currency['ask'])
        except:
            errors.append("Incorrect value")
            return render_template('xe.html', currency_list=select_data, errors=errors, tab='Error')
            # return "Incorrect value"
    return redirect("/xe")



if __name__ == "__main__":
    app.run(debug=True)
