from flask import render_template, flash, redirect, request
from app import app
from app.forms import Form

from app import augurAccuracyFunctions as augurAccuracyFunctions

@app.route('/')
@app.route('/index',methods=['GET', 'POST'])
def index():
    form = Form()
    if form.validate_on_submit():
        result = request.form
        marketSet = augurAccuracyFunctions.binaryMarkets
        secondsAhead = int(result['secondsAhead'])
        kernelFunction = eval('augurAccuracyFunctions.' + result['kernelFunction'])
        kernelWidth = int(result['kernelWidth'])
        scoreFunction = eval('augurAccuracyFunctions.' + result['scoreFunction'])
        score = augurAccuracyFunctions.scoreMarketsBinary(marketSet, secondsAhead, kernelFunction, kernelWidth, scoreFunction)
        return render_template('index.html', title='AugurScore', form=form, score=str(score))
    else:
        print(form.errors)
        return render_template('index.html', title='AugurScore', form=form)

