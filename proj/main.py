from flask import Flask, request, redirect, render_template, url_for

app = Flask(__name__)

result1 = 'hi'

@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        gre_verbal = request.form['gre_verbal']
        gre_quantitative = request.form['gre_quantitative']
        gre_writing = request.form['gre_writing']
        gpa = request.form['gpa']
        cost = request.form['cost']
        pub_or_priv = request.form['pub_or_priv']
        size = request.form['size']
        location = request.form['location']

        return render_template('results.html', gre_verbal=gre_verbal, 
        gre_quantitative=gre_quantitative, gre_writing=gre_writing, gpa=gpa, 
        cost=cost, pub_or_priv=pub_or_priv, size=size, location=location)
    else:   
        return render_template('home.html')

@app.route("/results", methods=['POST'])

def results():
    result = 'nothing submitted'
    return render_template("results.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)