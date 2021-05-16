from flask import Flask, request, redirect, render_template, url_for
import pandas as pd
import numpy as np
import sys
import logging
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cosine.html
from scipy.spatial.distance import cosine
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.jaccard.html
from scipy.spatial.distance import jaccard
import logging

app = Flask(__name__)

logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger
handler = logging.FileHandler('test.log') # creates handler for the log file
logger.addHandler(handler) # adds handler to the werkzeug WSGI logger


result1 = 'hi'

@app.route("/", methods=['GET','POST'])
def home():
    logger.info("Here's some info")
    if request.method == 'POST':
        gre_verbal = request.form['gre_verbal']

        schoolArray = get_sim_score(0, 0, 0, 0)

        # print('This is error output', file=sys.stderr)
        # print('This is standard output', file=sys.stdout)

        print('This is standard output', file=sys.stdout)


        return render_template('results.html',
                               results=schoolArray, gre_verbal=gre_verbal)
    else:   
        return render_template('home.html')
    
def get_sim_score(input_cost, input_puborpriv, input_size, input_location):
    user_inputs = [input_cost, input_puborpriv, input_size, input_location]
    finalData = pd.read_csv('finalData.csv')
    weights = [40, 30, 20, 10]
    cosine_similarity_scores = []
    jaccard_similarity_scores = []
    for index, row in finalData.iterrows():
        name = finalData.loc[index,'Name']
        cost = finalData.loc[index,'Cost']
        pubOrPriv = finalData.loc[index,'pubOrPrivNum']
        size = finalData.loc[index,'SizeNum']
        state = finalData.loc[index,'LocationNum']
        school_info = [cost, pubOrPriv, size, state]
        cosine_score = 1 - cosine(user_inputs, school_info, weights)
        cosine_similarity_scores.append(cosine_score)
        jaccard_score = 1 - jaccard(user_inputs, school_info, weights)
        jaccard_similarity_scores.append(jaccard_score)

    cosine_ranked_schools_scores = np.sort(-1*np.array(cosine_similarity_scores))
    cosine_ranked_schools_index = np.argsort(-1*np.array(cosine_similarity_scores))
    cosine_ranked_schools_names = []

    jaccard_ranked_schools_scores = np.sort(-1*np.array(jaccard_similarity_scores))
    jaccard_ranked_schools_index = np.argsort(-1*np.array(jaccard_similarity_scores))
    jaccard_ranked_schools_names = []

    for index in cosine_ranked_schools_index:
        cosine_ranked_schools_names.append(finalData.loc[index,'Name'])

    for index in jaccard_ranked_schools_index:
        jaccard_ranked_schools_names.append(finalData.loc[index,'Name'])
    
    # app.logger.warning('testing warning log')
    # app.logger.error('testing error log')
    # app.logger.info('testing info log')
    # print(cosine_ranked_schools_names, file=sys.stdout)

    return cosine_ranked_schools_names

@app.route("/results", methods=['POST'])

def results():
    result = 'nothing submitted'
    return render_template("results.html", result = result)

if __name__ == "__main__":
    app.run(debug=True)
