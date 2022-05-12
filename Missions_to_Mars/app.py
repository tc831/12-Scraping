# Dependencies
import scrape_mars
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri = "mongodb://localhost:27017/mission_to_mars_db")

# Create route that renders index.html
@app.route("/")
def home(): 

    # Find data from Mongo DB
    mars_facts = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", mars = mars_facts)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Call to run the scrape function
    mars_data = scrape_mars.scrape()

    # Update the Mongo DB each time when new scrape happen
    mongo.db.mars_data.update({}, mars_data, upsert = True)

    # Back to the home page
    return redirect("/", code = 302)

if __name__ == "__main__":
    app.run(debug = True)