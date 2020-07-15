# 1. import Flask
from flask import Flask, jsonify
# %matplotlib inline 
# Import necessary modules
from matplotlib import style
# style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
import numpy as np
import pandas as pd
import datetime as dt

database_path = "Resources/hawaii.sqlite"
engine = sqlalchemy.create_engine(f"sqlite:///{database_path}")

""" Reflect Tables into SQLAlchemy ORM """
Base = automap_base()
Base.prepare(engine, reflect=True)

# Map Measurement and Station tables
Measurement = Base.classes.measurement
Station = Base.classes.station


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!. This is Irina"


# 4. Define what to do when a user hits the index route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page...")
    # Convert the query results to a dictionary using 'Date' as the key and 'prcp' as the value 
    # return "Welcome to my 'Precipitation' page!. This is Irina"
    session = Session(engine)
    """ Return the list of stations with the precipitation data""" 
    results = session.query(Measurement.station, Measurement.prcp).all()
    print(len(results))
    session.close()

    # # Convert list of tuples into normal list
    # prcp_data_list = list(np.ravel(results))
    # return jsonify(prcp_data_list)

    # Create a dictionary from the row data and append to a list
    prcp_list = []
    for station, prcp in results:
        prcp_dict = {}
        prcp_dict["station"] = station
        prcp_dict["precipitation"] = prcp
        prcp_list.append(prcp_dict)
    return jsonify(prcp_list)

# 5. Define what to do when a user hits the /about route
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'About' page...")
    return "Welcome to my 'Stations' page!"

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Contact' page...")
    return "Welcome to my 'TOBS' page!"


if __name__ == "__main__":
    app.run(debug=True)

