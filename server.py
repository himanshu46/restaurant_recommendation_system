import pandas as pd
from flask import Flask, render_template, request
from mongo_query import recommend_rest

# create a flask application
app = Flask(__name__)


# route: http method and path
@app.route("/", methods=["GET"])
def root():
    # return "<h1>Welcome to Flask</h1>"
    return render_template("index.html")


# this function will be executed when user enter
# experience and hits the submit button
@app.route("/view", methods=["POST"])
def recommend_restaurant():
    # get the experience entered by user
    loc = request.form.get("loc")
    min = int(request.form.get("min"))
    max = int(request.form.get("max"))
    dist = int(request.form.get("dist"))
    ls = recommend_rest(loc,min,max, dist)
    if ls == 0:
        return render_template("view.html", tables=0)
    else:
        rest = pd.DataFrame(ls)
        return render_template("view.html", tables=[rest.to_html(index=False)])


# start the flask web server
app.run(host="0.0.0.0", port=3000, debug=True)
