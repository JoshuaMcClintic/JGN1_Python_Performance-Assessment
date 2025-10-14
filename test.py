import unittest
from weather_data import WeatherData

# Latitude and longitude are set to New Orleans, Louisiana
latitude, longitude = 29.9547, -90.0751
# Date is set to Halloween
month, day = 10, 31
# Years are last 5 years, from 2025
years = [2020, 2021, 2022, 2023, 2024]


class TestWeatherData(unittest.TestCase):
    """
    setUpClass to instance WeatherData class as an object;

    test_1: Ensure that weather_info variable from WeatherClass instance is not none;
            Ensure that there are 5 items in WeatherClass instance for the 5 years;

    test_2: Ensure that create_weather_list method from WeatherData contains 5 items for the 5 years for each of the
            following: mean_temperature, sum_precipitation, max_wind_speed

    test_3: Ensure that the data added to instance by calling API does not contain impossible values: 0 for
            precipitation and wind speed, -460 (absolute 0) for temperature
    """
    @classmethod
    def setUpClass(cls):
        cls.weather_data = WeatherData(latitude=latitude, longitude=longitude, month=month, day=day, years=years)
        cls.weather_data.call_weather_api()
        print('Setup completed\n')

    # Check if weather_info list is populated. Should have 5 items, and should not be None
    def test_1(self):
        print('Starting first test...')
        self.assertIsNotNone(self.weather_data.weather_info, 'Failed: weather_info found to be type: None')
        self.assertEqual(len(self.weather_data.weather_info), 5, 'Failed: weather_info should have len: 5')
        print('First test passed!\n')

    def test_2(self):
        print('Starting second test...')
        self.assertEqual(len(WeatherData.create_weather_list(self.weather_data, 'mean_temperature')), 5,
                         'Failed: temperature list should contain 5 items')
        self.assertEqual(len(WeatherData.create_weather_list(self.weather_data, 'sum_precipitation')), 5,
                         'Failed: precipitation list should contain 5 items')
        self.assertEqual(len(WeatherData.create_weather_list(self.weather_data, 'max_wind_speed')), 5,
                         'Failed: wind speed list should contain 5 items')
        print('Second test passed!\n')

    # Ensure that weather items gathered in list from create_weather_list do not have impossible values
    def test_3(self):
        print('Starting third test...')
        temp_list = self.weather_data.create_weather_list('mean_temperature')
        precip_list = self.weather_data.create_weather_list('sum_precipitation')
        wind_list = self.weather_data.create_weather_list('max_wind_speed')
        for precip in precip_list:
            self.assertGreaterEqual(precip, 0, 'Failed: precipitation cannot be less than 0 inches')
        for speed in wind_list:
            self.assertGreaterEqual(speed, 0, 'Failed: wind speed cannot be less than 0 mph')
        for temp in temp_list:
            self.assertGreaterEqual(temp, -460, 'Failed: temperature cannot be less than -460F, or absolute 0')
        print('Third test passed!\n')


if __name__ == '__main__':
    unittest.main()
