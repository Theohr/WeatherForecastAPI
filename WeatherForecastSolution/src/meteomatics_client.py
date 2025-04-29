import requests
from datetime import datetime

class MeteomaticsClient:
    def __init__(self, username, password):
        self.base_url = 'https://api.meteomatics.com'
        self.auth = (username, password)

    def get_forecast(self, lat, lon, start_date, end_date, interval, parameters):
        url = f"{self.base_url}/{start_date}--{end_date}:{interval}/{','.join(parameters)}/{lat},{lon}/json"
        response = requests.get(url, auth=self.auth)
        response.raise_for_status()
        data = response.json()
        
        forecasts = []
        for date_data in data['data']:
            parameter = date_data['parameter']
            for coord_data in date_data['coordinates']:
                for date_value in coord_data['dates']:
                    forecast = {
                        'valid_date': date_value['date'],
                        parameter: date_value['value']
                    }
                    forecasts.append(forecast)
        
        # Group by date
        result = {}
        for forecast in forecasts:
            date = forecast['valid_date']
            if date not in result:
                result[date] = {'valid_date': date}
            # Update the result with the parameter value
            for key, value in forecast.items():
                if key != 'valid_date':
                    result[date][key] = value
        
        return list(result.values())