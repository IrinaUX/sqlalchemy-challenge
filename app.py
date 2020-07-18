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
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/end<br/>"
    )

# 4. Define what to do when a user hits the index route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """ Returns the precipitation data
    """
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
    """ Returns the list of stations
    """
    session = Session(engine)

    # Return the list of stations with the stations data
    results2 = session.query(Station.name).all() 
    session.close()
    return jsonify(results2)
   
    
@app.route("/api/v1.0/tobs")
def tobs():
    """ Returns the dates and the temperatures 
        observed in the latest 12 months
    """
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
    
    # Query stations in descending order
    station = session.query(Measurement.station, func.count(Measurement.tobs)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).all()
    
    # Save the station name with maximum observations into a variable
    maxtobs_station = station[0][0]
    
    # Query the dates and observations for the identified station 
    maxtobsstation_query = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == maxtobs_station).\
        filter(Measurement.date >= latest_twelve_months_date).\
        all()
    
    # Create a list of dates and temperatures for the identified station
    dates_tobs_list = []
    for date, tobs in maxtobsstation_query:
        dates_tobs_dict = {}
        dates_tobs_dict["Date"] = date
        dates_tobs_dict["Observed Temperature, DegF"] = tobs
        dates_tobs_list.append(dates_tobs_dict)
    return jsonify(dates_tobs_list)
 

@app.route("/api/v1.0/<start>")
def temperatures_start(start):
    """ Given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than 
        and equal to the start date. 
    """
    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
    
    # Convert list of tuples into normal list
    temperatures_start = list(np.ravel(results))

    return jsonify(temperatures_start)

    session.close()


@app.route("/api/v1.0/<start>/<end>")
def temperatures_start_end(start, end):
    """ When given the start and the end date, 
        calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.
    """

    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    
    # Convert list of tuples into normal list
    temperatures_start_end = list(np.ravel(results))

    return jsonify(temperatures_start_end)

    session.close()


if __name__ == "__main__":
    app.run(debug=True)

