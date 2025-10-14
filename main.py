# Import external libraries
import sqlite3
from tabulate import tabulate
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys

# Import internal libraries
from weather_data import WeatherData
from database import base, WeatherTable

# Ask user if they want to use the default parameters or their own parameters
check_default = input('Would you like to use default parameters? y/n: ')

# If default, create variables for New Orleans, Louisiana, for the past 5 Halloweens
if check_default == 'y':
    latitude, longitude = 29.9547, -90.0751
    month, day = 10, 31
    years = [2020, 2021, 2022, 2023, 2024]
    print('Creating table for weather data from the past 5 Halloweens from New Orleans, Louisiana.')

# If user decides to use their own parameters, ask for parameters. If no parameter is given, default to above parameter
elif check_default == 'n':
    print('You will be prompted to add your own location and date information. You can still use the default settings '
          'if you press Enter without typing anything for each statement. '
          'The default information is as follows:\n\n'
          'Latitude: 29.9547, Longitude: -90.0751; New Orleans, Louisiana\n'
          'Date: October 31; Halloween\n'
          'Years: Past 5 years from 2025; 2020, 2021, 2022, 2023, 2024.\n\n'
          'If you would like to use the default information, press Enter without making any input.')

    # Create variables for location (New Orleans, Louisiana) and dates (past 5 Halloweens)
    # Request input or use default values if no input is made.
    latitude = float(input('Type the desired Latitude or press Enter for default: ') or 29.9547)
    longitude = float(input('Type the desired Longitude or press Enter for default: ') or -90.0751)
    month = int(input('Type the desired Month as a number (ie. for October, type "10") or press Enter for default: ')
                or 10)
    day = int(input('Type the desired Day or press Enter for default: ') or 31)
    num_years = int(input('Type the number of years you want to see data for or Enter for default: ') or 5)
    last_year = int(input('Type the last year you want to see data for (ie. default is 2024): ') or 2024)
    years = []

    # Create the years list to access API data. If any date before January 1st, 1940 is added to the years list,
    # halt the program, as attempting to gather data from that date will result in an error, as the WeatherData class
    # has methods that aggregate data from each year, and type: None cannot be aggregated.
    for year in range(0, num_years):
        if last_year < 1940:
            sys.exit('The earliest year in the API database is 1940. Please ensure that any date before January 1st, '
                     '1940 is not included in the years you are checking.')
        years.append(last_year)
        last_year -= 1
    years.reverse()

# If user makes no input, use default parameters
else:
    latitude, longitude = 29.9547, -90.0751
    month, day = 10, 31
    years = [2020, 2021, 2022, 2023, 2024]
    print('No input was made. Using default parameters: New Orleans, Louisiana, for the past 5 Halloweens.')

print('\nProcessing...')

# Instance WeatherData class and call api
weather = WeatherData(latitude, longitude, month, day, years)
yearly_weather = weather.call_weather_api()

engine = create_engine('sqlite:///weather_data.db')

# CREATE OR REPLACE engine
base.metadata.drop_all(engine)
base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Populate WeatherTable table with API data
for year_data in yearly_weather:
    row = WeatherTable(
        Latitude=latitude,
        Longitude=longitude,
        Month=month,
        Day=day,
        Year=year_data['year'],

        temp=year_data['mean_temperature'],
        average_temperature=weather.get_temp('avg'),
        min_temperature=weather.get_temp('min'),
        max_temperature=weather.get_temp('max'),

        wind_speed=year_data['max_wind_speed'],
        average_wind_speed=weather.get_wind_speed('avg'),
        max_wind_speed=weather.get_wind_speed('max'),
        min_wind_speed=weather.get_wind_speed('min'),

        precipitation=year_data['sum_precipitation'],
        sum_precipitation=weather.get_precipitation('sum'),
        max_precipitation=weather.get_precipitation('max'),
        min_precipitation=weather.get_precipitation('min')
    )
    session.add(row)

print('Data has been added to the table.')
session.commit()
session.close()


def query_table(lat: float, long: float, mon: int, da: int):
    """
    Connects to sqlite database <weather_data.db> defined above. Creates table in terminal with headers using
    SQL SELECT statement
    :param lat: Location Latitude
    :param long: Location Longitude
    :param mon: Month
    :param da: Day, as 'day' was already in use
    :return: SELECT * FROM Weather_Table WHERE Latitude = lat AND Longitude = long AND Month = mon AND Day = da;
    """
    # Connect to database
    connection = sqlite3.connect('weather_data.db')
    cursor = connection.cursor()

    # Create SQL statement to form table from database
    query = (
        f'SELECT * FROM Weather_Table WHERE Latitude = ? AND Longitude = ? AND Month = ? AND Day = ?;')
    cursor.execute(query, (lat, long, mon, da))
    full_weather = cursor.fetchall()

    # If database is successfully queried, create table in console with headers
    if full_weather:
        headers = ['ID', 'Month', 'Day', 'Year',
                   'Daily_Temp (F)', 'Avg_Temp (F)', 'Max_Temp (F)', 'Min_Temp (F)',
                   'Daily_Wind_Speed (mph)', 'Avg_Wind_Speed (mph)', 'Max_Wind_Speed (mph)', 'Min_Wind_Speed (mph)',
                   'Daily_Precipitation (inches)', 'Sum_Precipitation (inches)',
                   'Max_Precipitation (inches)', 'Min_Precipitation (inches)']
        table_data = []

        for item in full_weather:
            table_data.append([
                item[0],  # ID
                item[3],  # Month
                item[4],  # Day
                item[5],  # Year

                item[6],  # Single Day's Temp
                item[7],  # Average Temp
                item[8],  # Maximum Temp
                item[9],  # Minimum Temp

                item[10],  # Single Day's Max Wind Speed
                item[11],  # Average Wind Speed
                item[12],  # Maximum Wind Speed
                item[13],  # Minimum Wind Speed

                item[14],  # Single Day's Precipitation
                item[15],  # Total Precipitation
                item[16],  # Maximum Precipitation
                item[17]  # Minimum Precipitation
            ])

        # Print table to console
        print(tabulate(table_data, headers=headers, tablefmt='grid'))

        cursor.close()
        connection.close()
    else:
        print('Error')


print()
# Print statement for table information showing location and date

if latitude == 29.9547 and longitude == -90.0751:
    if month == 10 and day == 31:
        print(f'Weather data for Halloween data in New Orleans for years: {years}')
    else:
        print(f'Weather data for date {month}, {day} in New Orleans for years: {years}')
elif month == 10 and day == 31 and not (latitude == 29.9547 and longitude == -90.0751):
    print(f'Weather data for Halloween data in location: {latitude}, {longitude} for years: {years}')
else:
    print(f'Weather data for date {month}, {day} in location: {latitude}, {longitude} for years: {years}')

# Finally, call query function
query_table(latitude, longitude, month, day)
