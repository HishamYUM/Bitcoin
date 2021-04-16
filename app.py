import os

from flask import Flask, render_template, request

import candlestick
import conversion
import trade
from coins import show
from conversion import convert_currencies
from plot_of_altcoins import allcoins

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# @app.route('/trade')
# def trade():
#     return render_template('trade.html')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/Evolution/')
def Evolution():
    if os.path.isfile("templates/bitcoin_candlestick.html"):
        os.remove("templates/bitcoin_candlestick.html")
        candlestick.plot_graph()
    else:
        candlestick.plot_graph()
    return render_template('evolution.html')


@app.route('/Historical-data/<curr>/')
def currency(curr):
    return show(curr)


@app.route('/Historical-data/')
def gallery():
    return render_template('gallery.html')


@app.route('/Evolution/Comparison/')
def plot_allcoins():
    allcoins()
    return render_template('comparison.html')


@app.route('/trade', methods=['GET', 'POST'])
def trading():
    trade.buy_sell()
    conversion.plot_evolution_garph()
    select = request.args.get('select_currencies')
    to_curr = request.args.get('to_currency')
    if request.args.get('amount') == None:
        amount = 0
    else:
        amount = int(request.args.get('amount'))
    # print(amount)  # just to see what select is
    result = convert_currencies(select, to_curr, amount)
    # return render_template('trade.html', select=select, amount=amount, to_curr=to_curr)
    return render_template('trade.html', result=result)


if __name__ == "__main__":
    app.run(debug=True)
