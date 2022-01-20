from flask import Flask,render_template,request
import requests

app = Flask(__name__)
API_KEY = 'RQM7GIDWT0ZU2WLU'

@app.route('/',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        try:
            amount = request.form['amount']
            amount = float(amount)
            from_c = request.form['from_c']
            to_c = request.form['to_c']
            url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={}&to_currency={}&apikey={}'.format(from_c,to_c,API_KEY)
            response = requests.get(url=url).json()
            rate = response['Realtime Currency Exchange Rate']['5. Exchange Rate']
            rate = float(rate)
            result = rate * amount
            from_c_code = response['Realtime Currency Exchange Rate']['1. From_Currency Code']
            from_c_name = response['Realtime Currency Exchange Rate']['2. From_Currency Name']
            to_c_code = response['Realtime Currency Exchange Rate']['3. To_Currency Code']
            to_c_name = response['Realtime Currency Exchange Rate']['4. To_Currency Name']
            time = response['Realtime Currency Exchange Rate']['6. Last Refreshed']
            return render_template('home.html', result=round(result,2), amount=amount,
                                    from_c_code=from_c_code, from_c_name=from_c_name,
                                    to_c_code=to_c_code, to_c_name=to_c_name, time=time)
        except Exception as e:
            return '<h1>Bad Request : {}</h1>'.format(e)

    else:
        return render_template('home.html')



if __name__ == "__main__":
    app.run(debug= False)