from flask import render_template, flash, redirect, request
from app import app
from app.forms import Form

from app import augurAccuracyFunctions as aaf
import os

@app.route('/')
@app.route('/index',methods=['GET', 'POST'])
def index():
    
    thisDir = './app/static/'
    files = os.listdir(thisDir)
    for file in files:
        if file.endswith(".jpg"):
            os.remove(thisDir + file)
       
    form = Form()
    if form.validate_on_submit():
        result = request.form
        marketSet = aaf.binaryMarkets
        secondsAhead = float(result['daysAhead']) * 60. * 60. * 24.
        kernelFunction = eval('aaf.' + result['kernelFunction'])
        kernelWidthInSeconds = float(result['kernelWidth']) * 60. * 60. * 24.
        
        kernelFunctionCalibrated = eval('aaf.' + result['kernelFunctionCalibrated'])
        print(result['kernelWidthCalibrated'])
        kernelWidthCalibrated = float(result['kernelWidthCalibrated'])
        
        scores = {}
        scores['logScore'], weightedVolume, allTrades = aaf.scoreMarketsBinary(marketSet, secondsAhead, kernelFunction, kernelWidthInSeconds, aaf.logScore)
        scores['brierScore'], weightedVolume, allTrades = aaf.scoreMarketsBinary(marketSet, secondsAhead, kernelFunction, kernelWidthInSeconds, aaf.brierScore)
        scores['sphericalScore'], weightedVolume, allTrades = aaf.scoreMarketsBinary(marketSet, secondsAhead, kernelFunction, kernelWidthInSeconds, aaf.sphericalScore)
        
        print(kernelFunctionCalibrated)
        print(kernelWidthCalibrated)
        
        filePath = aaf.calibrationPlot(marketSet,
                            kernelFunctionCalibrated, 
                            kernelWidthCalibrated)
        
        return render_template('index.html', 
                               title='AugurScore', 
                               form=form, 
                               scores=scores,
                               weightedVolume=weightedVolume,
                               filePath=filePath)
    else:
        print(form.errors)
        return render_template('index.html', title='AugurScore', form=form)
    