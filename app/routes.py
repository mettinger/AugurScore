from flask import render_template, flash, redirect, request
from app import app
from app.forms import Form

from app import augurAccuracyFunctions as aaf

@app.route('/')
@app.route('/index',methods=['GET', 'POST'])
def index():
    form = Form()
    if form.validate_on_submit():
        result = request.form
        marketSet = aaf.binaryMarkets
        secondsAhead = float(result['daysAhead']) * 60. * 60. * 24.
        kernelFunction = eval('aaf.' + result['kernelFunction'])
        kernelWidthInSeconds = float(result['kernelWidth']) * 60. * 60. * 24.
        
        scores = {}
        scores['logScore'], weightedVolume, allTrades = aaf.scoreMarketsBinary(marketSet, secondsAhead, kernelFunction, kernelWidthInSeconds, aaf.logScore)
        scores['brierScore'], weightedVolume, allTrades = aaf.scoreMarketsBinary(marketSet, secondsAhead, kernelFunction, kernelWidthInSeconds, aaf.brierScore)
        scores['sphericalScore'], weightedVolume, allTrades = aaf.scoreMarketsBinary(marketSet, secondsAhead, kernelFunction, kernelWidthInSeconds, aaf.sphericalScore)
        print(allTrades)
        imagePath = aaf.confusionMatrixMake(allTrades)
        return render_template('index.html', 
                               title='AugurScore', 
                               form=form, 
                               scores=scores,
                               weightedVolume=weightedVolume,
                               imagePath=imagePath)
    else:
        print(form.errors)
        return render_template('index.html', title='AugurScore', form=form)
    
# probabilstic confusion matrix
# select subset of wagers
# more kernels
# make it pretty