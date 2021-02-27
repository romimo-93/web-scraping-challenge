from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    compiled_dict = mongo.db.mars.find_one()
    # Return template and data
    return render_template("index.html", mars=compiled_dict)


@app.route("/scrape")
def scrape():
    mars_db = mongo.db.mars
    compiled_dict_data = scrape_mars.scrape_info()
    # Update the Mongo database using update and upsert=True
    mars_db.update({}, compiled_dict_data, upsert=True)
    return redirect("/",code=302)

if __name__ == "__main__":
    app.run(debug=True)
