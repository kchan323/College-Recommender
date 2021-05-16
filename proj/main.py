from flask import Flask, request, redirect, render_template, url_for

app = Flask(__name__)

result1 = 'hi'

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        gre = request.form['gre']
        gre_verbal = request.form['gre_verbal']

        return render_template('results.html',
                               result=gre, gre_verbal=gre_verbal)
    else:   
        return render_template('home.html')

@app.route("/results", methods=['POST'])

def results():
    result = 'nothing submitted'
    return render_template("results.html", result = result)

if __name__ == "__main__":
    app.run(debug=True)
