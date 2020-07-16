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
    return (
        f"<p>Hawaii weather!</p>"
        f"/api/v1.0/precipitation<br/>Returns a JSON list of percipitation data from Measurement<br/><br/>"
        f"/api/v1.0/stations<br/>Returns a JSON list of the weather stations<br/><br/>"
        f"/api/v1.0/tobs<br/>Returns a JSON list of the Temperature Observations (tobs) for each station for the dates between 8/23/16 and 8/23/17<br/><br/>"
    )

# 4. Define what to do when a user hits the index route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Precipitation' page.")
    session = Session(engine)
    # Return the list of stations with the precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Create a dictionary from the row data and append to a list
    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        prcp_list.append(prcp_dict)
    return jsonify(prcp_list)

# 5. Define what to do when a user hits the /about route
@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'About' page...")
    #return "Welcome to my 'Stations' page!"
    session = Session(engine)

    # Return the list of stations with the stations data
    results = session.query(Station.id, Station.name).all() 
    session.close()

    sta_list = []
    for id, station in results:
        sta_dict = {}
        sta_dict["ID"] = id
        sta_dict["Station"] = station
        sta_list.append(sta_dict)
    return jsonify(sta_list)
    # print(results)

@app.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Contact' page...")
    session = Session(engine)

    # Save latest date into a variable and in string type
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    # return latest_date
    
    # Find the latest year
    date_time_obj = dt.datetime.strptime(latest_date, '%Y-%m-%d') 

    # Last year from latest date's year
    one_year_back = date_time_obj.year - 1
    # return str(one_year_back)

    # Reconstruct the date 12 months back from the latest available date
    latest_twelve_months_date = dt.date(one_year_back, date_time_obj.month, date_time_obj.day)
    # return str(latest_twelve_months_date)

    # Save the counts of the observations 
    results = session.query(Measurement.station, func.count(Measurement.tobs)).group_by(Measurement.station).all()
    
    max_count = 0
    for i in range(len(results)):
        print(results[i][1])
        if results[i][1] > max_count:
            max_count = results[i][1]
    return str(max_count)

    # # Create second query for the latest 12 months
    # results_12 = session.query(Measurement.date, Measurement.station, Measurement.tobs).\
    #     order_by(Measurement.date.desc()).\
    #     filter(Measurement.date <= latest_date).\
    #     filter(Measurement.date > latest_twelve_months_date).\
    #     filter(Measurement.tobs != 'None').\
    #     all()

    session.close()

    # # Loop through the query results_12 to get the precipitation data
    # tobs_count_list = []
    # max_count = 0
    # for count in range(len(results_12)):
    #     tobs_count_dict = {}
    #     tobs_count_dict["Counts on observations"] = count
    #     tobs_count_list.append(tobs_count_dict)
    #     if int(results[count][0]) > max_count:
    #         max_count = results_12[count][1]
    # return jsonify(max_count)

    # # Loop through the query results to get the precipitation data
    # tobs_count_list = []
    # max_count = 0
    # for count in range(len(results)):
    #     tobs_count_dict = {}
    #     tobs_count_dict["Counts on observations"] = count
    #     tobs_count_list.append(tobs_count_dict)
    #     if results[count][1] > max_count:
    #         max_count = results[count][1]
    # return jsonify(max_count)

    # max_count = 0
    # for i in range(len(results)):
    #     print(results[i][1])
    #     if results[i][1] > max_count:
    #         max_count = results[i][1]
    # return max_count

if __name__ == "__main__":
    app.run(debug=True)

