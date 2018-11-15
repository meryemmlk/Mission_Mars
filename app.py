from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/marsdb"
mongo = PyMongo(app)

@app.route("/")
def index():
    
	
	scraped_facts = mongo.db.collection.find_one()

    # render an index.html template and pass it the data you retrieved from the database
	return render_template("index.html", scraped_facts=scraped_facts)

@app.route("/scrape")
def scraper():
    # run scrape function
    new_facts = scrape_mars.scrape()

    # empty out the collection
    mongo.db.collection.drop()

    # Insert new record into the collection
    mongo.db.collection.insert_one(new_facts)

    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)