from flask import Flask, request, render_template, jsonify

from statsmodels.tsa.statespace.sarimax import SARIMAXResults

app = Flask(__name__)

models = []

def forecast(model, year, month):
    predict_steps = (year - 2021) * 12 + month
    pred_uc = model.get_forecast(steps=predict_steps)
    return pred_uc.predicted_mean[-1]

def prediction(year, months):
    value = 0
    for model in models:
        value += forecast(model, year, months)
    return int(value)


@app.before_first_request
def load_model():
    global models
    Alkoholunfälle_model = SARIMAXResults.load('./models/model_Alkoholunfälle.pkg')
    Fluchtunfälle_model = SARIMAXResults.load('./models/model_Fluchtunfälle.pkg')
    Verkehrsunfälle_model = SARIMAXResults.load('./models/model_Verkehrsunfälle.pkg')
    models = [Alkoholunfälle_model, Fluchtunfälle_model, Verkehrsunfälle_model]

@app.route('/')
def show_page():
    return(render_template('index.html'))

@app.route('/api/predict', methods=['POST'])
def get_predictions_api():
    data_dict = request.get_json()
    year = int(data_dict['year'])
    month = int(data_dict['month'])

    if not (year and month):
        return {"Error": "year or month is missing"}, 400
    elif year < 2021:
        return {"Error": "Year should be greater than 2021"}, 400
    elif month < 1 or month > 12:
        return {"Error": "Month should be between 1 and 12"}, 400
    else:
        result = prediction(year, month)
        return {"prediction": result}, 200
@app.route('/predict', methods=['POST'])
def get_predictions_form():
    input = request.form['date'].split("-")
    year = int(input[0])
    month = int(input[1])
    result = prediction(year, month)
    date = input[0] + '/' + input[1]
    return (render_template('index.html', date=date, result=result))
if __name__ == "__main__":
    app.run("0.0.0.0", 5000)