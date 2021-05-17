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

@app.route("/", methods=['GET','POST'])
def home():
    logger.info("Here's some info")
    if request.method == 'POST':
        gre_verbal = request.form['gre_verbal']
        gre_quantitative = request.form['gre_quantitative']
        gre_writing = request.form['gre_writing']
        gpa = request.form['gpa']
        cost = request.form['cost']
        pub_or_priv = request.form['pub_or_priv']
        size = request.form['size']
        location = request.form['location']
        most_important = request.form['most_important']
        very_important = request.form['very_important']
        less_important = request.form['less_important']
        least_important = request.form['least_important']

        weights = get_weights(most_important, very_important, less_important, least_important)
        # print(weights, file=sys.stdout)

        # schools based on preference
        school_array = get_sim_score(float(cost), float(pub_or_priv), float(size), float(location), weights)
        school_array = school_array[0:7]
        
        top_school_info = []
        for idx, name in enumerate(school_array):
            if idx < 7:
                top_school_info.append(get_school_info(name))

        # print('This is standard output', file=sys.stdout)

        # schools based on scores using knn
        school_knn = get_school_knns(float(gre_verbal), float(gre_quantitative), float(gre_writing), float(gpa))
        top_school_knn_info = []

        for school in school_knn:
            school_name = school[0]
            top_school_knn_info.append(get_school_info(school_name))

        return render_template('results.html', gre_verbal=gre_verbal, 
        gre_quantitative=gre_quantitative, gre_writing=gre_writing, gpa=gpa, 
        cost=cost, pub_or_priv=pub_or_priv, size=size, location=location, 
        most_important=most_important, very_important=very_important, 
        less_important=less_important, least_important=least_important,
        results=school_array, top_school_info=top_school_info, school_knn=school_knn, top_school_knn_info=top_school_knn_info)
    else:   
        return render_template('home.html')    
    
def get_weights(most_important, very_important, less_important, least_important):
    weights = [0, 0, 0, 0]
    if most_important == "cost":
        weights[0] = 50
    elif most_important == "pub_or_priv":
        weights[1] = 50
    elif most_important == "size":
        weights[2] = 50
    elif most_important == "location":
        weights[3] = 50

    if very_important == "cost":
        weights[0] = 40
    elif very_important == "pub_or_priv":
        weights[1] = 40
    elif very_important == "size":
        weights[2] = 40
    elif very_important == "location":
        weights[3] = 40

    if less_important == "cost":
        weights[0] = 7
    elif less_important == "pub_or_priv":
        weights[1] = 7
    elif less_important == "size":
        weights[2] = 7
    elif less_important == "location":
        weights[3] = 7
    
    if least_important == "cost":
        weights[0] = 3
    elif least_important == "pub_or_priv":
        weights[1] = 3
    elif least_important == "size":
        weights[2] = 3
    elif least_important == "location":
        weights[3] = 3
    
    return weights

def get_sim_score(input_cost, input_puborpriv, input_size, input_location, weights):
    user_inputs = [input_cost, input_puborpriv, input_size, input_location]
    final_data = pd.read_csv('finalData.csv')
    cosine_similarity_scores = []
    jaccard_similarity_scores = []
    for index, row in final_data.iterrows():
        cost = final_data.loc[index,'Cost'] + 1
        puborpriv = final_data.loc[index,'pubOrPrivNum'] + 1
        size = final_data.loc[index,'SizeNum'] + 1
        location = final_data.loc[index,'LocationNum'] + 1
        school_info = [cost, puborpriv, size, location]
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
        cosine_ranked_schools_names.append(final_data.loc[index,'Name'])

    for index in jaccard_ranked_schools_index:
        jaccard_ranked_schools_names.append(final_data.loc[index,'Name'])

    return cosine_ranked_schools_names

def get_school_info(school_name):
    final_data = pd.read_csv('finalData.csv')
    data = ['Name', 'Rank', 'City', 'State', 'PubOrPriv', 'StudentPop', 'Size', 'Location', 'Website']
    final_data_cols = final_data[data]
    school = final_data_cols.loc[final_data_cols['Name'] == school_name]
    school_info = []
    for i in data:
        school_info.append(list(school[i])[0])    
    return school_info
    
def get_school_knns(greV, greQ, greA, cgpa):
    gradData = pd.read_csv('cleanedGradData.csv')
    testSet = [[greV, greQ, greA, cgpa]]
    test = pd.DataFrame(testSet)
    k = 7
    result, neigh= knn(gradData, test, k)
    return result

def eucDistance(data1, data2, length):
    distance = 0
    for x in range(length):
        distance += np.square(data1[x] - data2[x])
    return np.sqrt(distance)

def knn(trainingSet, testInstance, k):
    distances = {}
    length = testInstance.shape[1]
    for x in range(len(trainingSet)):
        dist = eucDistance(testInstance, trainingSet.iloc[x], length)
        distances[x] = dist[0]
    sorted_d = sorted(distances.items(), key=lambda x: x[1])
    neighbors = []
    for x in range(k):
        neighbors.append(sorted_d[x][0])
    classVotes = {}
    for x in range(len(neighbors)):
        response = trainingSet.iloc[neighbors[x]][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.items(), key=lambda x: x[1], reverse=True)
    return(sortedVotes, neighbors)

@app.route("/results", methods=['POST'])

def results():
    result = 'nothing submitted'
    return render_template("results.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)