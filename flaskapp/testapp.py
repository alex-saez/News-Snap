#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This file is part of the flask+d3 Hello World project.
"""
import json
from flask import Flask, request, render_template
import numpy as np
from main import findTopics



app = Flask(__name__)



@app.route("/")
@app.route('/<int:mux>')
def gindex():
    """
    When you request the gaus path, you'll get the gaus.html template.

    """
    
    #pull date from input field
    #mux = int(request.args.get('mux'))

    mux = request.args.get('mux',6190)
    return render_template("pagelayout4.html",mux=mux)


@app.route('/gdata')
@app.route('/gdata/<int:mux>')
def gdata(mux=None):
    
    mux = int(request.args.get('mux'))

    
    # find topics
    topics = findTopics(mux)
    
    ntopics = len(topics['titles'])
    A = [len(i) for i in topics['titles']]
    x = np.arange(ntopics)
    y = [0]*ntopics


    col = ["#156b87", "#876315", "#543510", "#872815"]*2
          
         
#    t = [[w+' ' for w in topics['summaries'][i]] for i in range(ntopics)]
    kw = ['\n'.join(t) for t in topics['summaries']]
    
    summ = topics['titles']

#    summs_titles = []
#    for i,s in enumerate(topics['summaries']):
#        summs_titles.append(dict(summary = ' | '.join(s), titles = ''))
#        for t in topics['titles'][i]:
#             summs_titles.append(dict(summary = '', titles = t.decode('utf8').encode('ascii', 'ignore')))
#    
#    return render_template('output.html',topics=summs_titles)



    return json.dumps([{"_id": i, 
                        "x": x[i], 
                        "y": y[i], 
                        "area": A[i], 
                        "color": col[i], 
                        "keywords": kw[i],
                        "summary": summ[i]} 
                      for i in range(ntopics)])
    

if __name__ == "__main__":
    import os

    port = 8000

    # Open a web browser pointing at the app.
    os.system("open http://localhost:{0}/".format(port))

    # Set up the development server on port 8000.
    app.debug = True
    app.run(port=port)