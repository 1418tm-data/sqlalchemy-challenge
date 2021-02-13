import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measure = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all passengers
    prp_result = session.query(Measure.date, Measure.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    prp_result_all = {date:prcp for date, prcp in prp_result}

    return jsonify(prp_result_all)

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all passengers
    prp_result = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list    

    return jsonify(prp_result)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all passengers
    ldate = session.query(Measure.date).order_by((Measure.date).desc()).first()
    ldate = ldate[0].split("-")
    ldate_year = dt.date(int(ldate[0]),int(ldate[1]),int(ldate[2])) - dt.timedelta(days=365)

    prp_result = session.query(Measure.date, Measure.tobs).filter(Measure.station == "USC00519281").filter(Measure.date >= ldate_year).all()

    session.close()

    # Convert list of tuples into normal list    

    return jsonify(prp_result)

@app.route("/api/v1.0/<start>")
def precp(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all passengers
    
    prp_result = session.query(func.max(Measure.tobs), func.min(Measure.tobs), func.avg(Measure.tobs)).filter(Measure.date >= start).all()

    session.close()

    # Convert list of tuples into normal list    

    return jsonify(prp_result)

@app.route("/api/v1.0/<start>/<end>")
def prp_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all passengers
    
    prp_result = session.query(func.max(Measure.tobs), func.min(Measure.tobs), func.avg(Measure.tobs)).filter(Measure.date >= start).filter(Measure.date <= end).all()

    session.close()

    # Convert list of tuples into normal list    

    return jsonify(prp_result)


if __name__ == '__main__':
    app.run(debug=True)
