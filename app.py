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
    n1 = request.form["input1"]
    n2 = request.form["input2"]
    n3 = request.form["input3"]
    n4 = request.form["input4"]
    goal = request.form["input5"]
    print("before serveEqPuzzle: n1=",n1, ", goal=",goal)

    result = serveEqPuzzle(n1, n2, n3, n4, goal)
    print("after serveEqPuzzle: n1=",n1, ", goal=",goal,", result=",result)

    return render_template("index.html", input1=n1, input2=n2, input3=n3, input4=n4, input5=goal, output_area=result)


if __name__ == "__main__":
    app.run()

