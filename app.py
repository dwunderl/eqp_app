from flask import Flask, render_template, request, make_response
from eqp import serveEqPuzzle

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


# called from flask ui
# result = serveEqPuzzle(n1, n2, n3, n4, goal)

@app.route("/submit", methods=["POST"])
def process():
    n1 = request.form["n1"]
    n2 = request.form["n2"]
    n3 = request.form["n3"]
    n4 = request.form["n4"]
    goal = request.form["goal"]
    #print("before serveEqPuzzle: n1=",n1, ", goal=",goal)

    familiesOfExpressions = serveEqPuzzle(n1, n2, n3, n4, goal)
    #print("after serveEqPuzzle: n1=",n1, ", goal=",goal,", result=",result)

    retExps = []
    for familyName, solutions in familiesOfExpressions.items():
        retExps.append("FamilyName: " + familyName)
        for sol in solutions:
            retExps.append(sol.expression)
        retExps.append("")
        
    # concatenate the list items with line breaks
    retExpsString = "\n".join(retExps)


    return render_template("index.html", n1=n1, n2=n2, n3=n3, n4=n4, goal=goal, expressions=retExpsString)

#---------------------------------
if __name__ == "__main__":
    app.run()

