import requests
import csv
import pickle
import os
import time
from time import sleep
from flask import Flask, render_template, request, redirect



app = Flask(__name__)

CACHE_FOLDER = "cache"
CACHE_FILE = "xe.pickle"
ENDPOINT = "http://api.nbp.pl/api/exchangerates/tables/C?format=json"

# def create_csv():
#     with open("xe.csv", mode="w") as f:
#         fieldnames = ['currency', 'code', 'bid', 'ask']
#         writer = csv.DictWriter(f, delimiter=';', fieldnames=fieldnames)
#         for currency in data[0]['rates']:
#             writer.writerow(currency)



# data = load_data("xe.pickle", "cache")

def cache_data(f):
    def wrapper(*args, **kwargs):
        path = os.path.join(CACHE_FOLDER, CACHE_FILE)
        try:
            print("trying......")
            with open(path, 'rb') as cache:
                rates, timestamp = pickle.load(cache)
                print(rates.keys(), timestamp, time.time() - timestamp)
            if time.time() - timestamp > 30:
                raise IOError()
        except IOError:
            rates = f()
            print("Fetching from API")
            with open(path, 'wb') as cache:
                pickle.dump((rates, time.time()), cache)
        return rates
    return wrapper

@cache_data
def rate():
    rates = {
        rate['code']: float(rate['ask']) for rate in requests.get(ENDPOINT).json()[0]['rates']
    }
    return rates

@app.route("/xe/", methods=['GET', 'POST'])
def currency_exchange():
    errors = []
    select_data = rate().keys()
    print(select_data)
    if request.method == "GET":
        tab = 'Dane'
        return render_template('xe.html', currency_list=select_data, tab=tab)
    if request.method == 'POST':
        try:
            qty = float(request.form['qty'])
            select = request.form.get('currency')
            # for currency in data[0]['rates']:
            #     if currency['code'] == select:
                    # return f"Należność w PLN: {qty*currency['ask']}"
            return render_template('xe.html', currency_list=select_data, errors=errors, tab='Do zapłaty', to_pay=qty*rate()[select])
        except:
            errors.append("Incorrect value")
            return render_template('xe.html', currency_list=select_data, errors=errors, tab='Error')
            # return "Incorrect value"
    return redirect("/xe")



if __name__ == "__main__":
    app.run(debug=True)
