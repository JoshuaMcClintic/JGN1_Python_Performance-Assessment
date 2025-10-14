import requests


# url = "https://archive-api.open-meteo.com/v1/archive"
# params = {
# 	"latitude": 29.9547,
# 	"longitude": -90.0751,
# 	"start_date": "2020-10-31",
# 	"end_date": "2024-10-31"
# }


# Create object with location, date, 5-year weather data:
class WeatherData:
    """
    Attributes:
        lat: Location Latitude
        long: Location Longitude
        mon: Month
        day: Day
        years: List of years to gather from API

        temp: List of Average Temperatures for location on date, for each year
        wind_speed: List of Maximum Wind Speeds for location on date, for each year
        precip: List of Total Precipitation for location on date, for each year

        min/max_temp/wind/precip: Minimum and Maximum Temperature, Wind Speed, and Precipitation for location on date
        avg_temp/wind: Average Temperature and Wind Speed for location on date
        sum_precip: Sum of Precipitation for location on date

        weather_info: List to contain weather data gathered from API

    Methods:
        call_weather_api(self):
            Calls weather API to return list of dictionaries containing year, temp, wind_speed, precip for each date
            returns <weather_info> list

        create_weather_list(self, item):
            accepts item: weather param from call_weather_api:
                'mean_temperature'; 'max_wind_speed'; 'sum_precipitation'
            creates list for use in other functions
            returns <weather_list> list

        get_<weather_param>(self, function):
            three parameters for <weather_param>: temp, precipitation, wind_speed
            accepts functions: 'min'; 'max'; 'avg'; 'sum'
            returns aggregate number <function(weather_list[item])>
    """

    def __init__(self, latitude: float, longitude: float, month: int, day: int, years: list):
        """
        arguments:
            (Latitude, Longitude, Month, Day): as numerics
            years: as list
                create attributes for arguments;
                create list attributes to be gathered from api
                create attributes to be aggregated from list attributes
                create list to pass api data into
        """
        self.lat = latitude
        self.long = longitude
        self.mon = month
        self.day = day
        self.years = years

        self.temp = []
        self.wind_speed = []
        self.precip = []

        self.min_temp = None
        self.max_temp = None
        self.avg_temp = None

        self.min_wind = None
        self.max_wind = None
        self.avg_wind = None

        self.min_precip = None
        self.max_precip = None
        self.sum_precip = None

        self.weather_info = []

    def call_weather_api(self):
        """
        Method for WeatherData class
        Loops over <self.years> list:
            Calls archive-api.open-meteo.com/v1/archive API:
                Opens API with params:
                    latitude, longitude, precipitation_sum, wind_speed_10m_max, temperature_2m_mean,
                    with start date and end date being equal to year-self.mon-self.day,
                    timezone: America-Chicago; CDT; GMT-5,
                    units are Fahrenheit, miles-per-hour(mph), inch
            Add data for day into weather_info list

        :return: List of dictionaries containing data gathered from API with keys:
        year; mean_temperature; max_wind_speed; sum_precipitation
        """
        for year in self.years:
            url = (
                f"https://archive-api.open-meteo.com/v1/archive?"
                f"latitude={self.lat}&longitude={self.long}&"
                f"daily=precipitation_sum,wind_speed_10m_max,temperature_2m_mean&"
                f"start_date={year}-{self.mon:02d}-{self.day:02d}&end_date={year}-{self.mon:02d}-{self.day:02d}&"
                f"timezone=America%2FChicago&"
                f"temperature_unit=fahrenheit&wind_speed_unit=mph&precipitation_unit=inch"
            )
            response = requests.get(url=url)

            # Attempt to add data from API into weather_info
            try:

                data = response.json()

                single_day_data = {
                    "year": year,
                    "mean_temperature": data.get('daily').get('temperature_2m_mean')[0],
                    "max_wind_speed": data.get('daily').get('wind_speed_10m_max')[0],
                    "sum_precipitation": data.get('daily').get('precipitation_sum')[0]
                }

                self.weather_info.append(single_day_data)

            except Exception as e:
                print(f'Error: {e}')
                print(f'Failed to retrieve data; {year}: {response.status_code}')

        print('Data successfully gathered from weather API.')
        return self.weather_info

    #   Add methods:

    def create_weather_list(self, item: str):
        """
        Creates list of numerics to be aggregated in later functions
        :param item: Key from <single_day_data> dictionary from <call_weather_api> function;
        Items are: 'mean_temperature', 'sum_precipitation', 'max_wind_speed'
        :return: List of values from dictionary <single_day_data> with key <item>
        """
        weather_list = []
        for day in self.weather_info:
            weather_list.append(day[item])
        return weather_list

    #   AVG(temp{Fahrenheit}); MAX(wind_speed{Miles-Per-Hour}); SUM(precipitation{Inches})

    def get_temp(self, function: str):
        """
        Aggregates numeric data from the list <weather_list> using key 'mean_temperature' for dictionary in list
        <weather_info>
        :param function: Aggregate function: 'min'; 'max'; 'avg'; 'sum'
        :return: Minimum, Maximum, Average, or Sum of items within <weather_list> from <create_weather_list>
        """
        weather = self.create_weather_list(item='mean_temperature')

        if function.lower() == 'min':
            return min(weather)
        elif function.lower() == 'max':
            return max(weather)
        elif function.lower() == 'avg':
            return sum(weather) / len(weather)
        elif function.lower() == 'sum':
            return sum(weather)
        else:
            print(f'{function} not defined')

    def get_precipitation(self, function: str):
        """
        Aggregates numeric data from the list <weather_list> using key 'sum_precipitation' for dictionary in list
        <weather_info>
        :param function: Aggregate function: 'min'; 'max'; 'avg'; 'sum'
        :return: Minimum, Maximum, Average, or Sum of items within <weather_list> from <create_weather_list>
        """
        weather = self.create_weather_list(item='sum_precipitation')

        if function.lower() == 'min':
            return min(weather)
        elif function.lower() == 'max':
            return max(weather)
        elif function.lower() == 'avg':
            return sum(weather) / len(weather)
        elif function.lower() == 'sum':
            return sum(weather)
        else:
            print(f'{function} not defined')

    def get_wind_speed(self, function: str):
        """
        Aggregates numeric data from the list <weather_list> using key 'max_wind_speed' for dictionary in list
        <weather_info>
        :param function: Aggregate function: 'min'; 'max'; 'avg'; 'sum'
        :return: Minimum, Maximum, Average, or Sum of items within <weather_list> from <create_weather_list>
        """
        weather = self.create_weather_list(item='max_wind_speed')

        if function.lower() == 'min':
            return min(weather)
        elif function.lower() == 'max':
            return max(weather)
        elif function.lower() == 'avg':
            return sum(weather) / len(weather)
        elif function.lower() == 'sum':
            return sum(weather)
        else:
            print(f'{function} not defined')
