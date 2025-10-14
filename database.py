from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import declarative_base

base = declarative_base()


class WeatherTable(base):
    __tablename__ = 'Weather_Table'

    # auto-incrementing integer as primary key
    ID = Column(Integer, primary_key=True, autoincrement=True)

    # Location and Date
    Longitude = Column(Float)
    Latitude = Column(Float)
    Month = Column(Integer)
    Day = Column(Integer)
    Year = Column(Integer)

    # Temp and aggregate temp columns
    temp = Column(Float)
    average_temperature = Column(Float)
    max_temperature = Column(Float)
    min_temperature = Column(Float)

    # Wind Speed and aggregate Wind Speed columns
    wind_speed = Column(Float)
    average_wind_speed = Column(Float)
    max_wind_speed = Column(Float)
    min_wind_speed = Column(Float)

    # Precipitation and aggregate Precipitation columns
    precipitation = Column(Float)
    sum_precipitation = Column(Float)
    max_precipitation = Column(Float)
    min_precipitation = Column(Float)
