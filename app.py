# 1. import Flask
from flask import Flask

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)


# 3. Define what to do when a user hits the index route
@app.route("/")
def precipitation():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!. This is Irina"


# 3. Define what to do when a user hits the index route
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Precipitation' page!. This is Irina"


# 4. Define what to do when a user hits the /about route
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

