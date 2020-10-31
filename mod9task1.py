import requests
import csv
from flask import Flask, render_template, request, redirect


response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")


data = response.json()

app = Flask(__name__)

def create_csv():
    with open("xe.csv", mode="w") as f:
        fieldnames = ['currency', 'code', 'bid', 'ask']
        writer = csv.DictWriter(f, delimiter=';', fieldnames=fieldnames)
        for currency in data[0]['rates']:
            writer.writerow(currency)


@app.route("/xe/", methods=['GET', 'POST'])
def currency_exchange():
    if request.method == "GET":
        tab = 'Dane'
        select_data = [x['code'] for x in data[0]['rates']]
        return render_template('xe.html', currency_list=select_data, tab=tab)
    if request.method == 'POST':
        try:
            qty = float(request.form['qty'])
            select = request.form.get('currency')
            for currency in data[0]['rates']:
                if currency['code'] == select:
                    return f"Należność w PLN: {qty*currency['ask']}"
        except:
            return "Incorrect value"
    return redirect("/xe")




def main():
    create_csv()

if __name__ == "__main__":
    main()
    app.run(debug=True)
