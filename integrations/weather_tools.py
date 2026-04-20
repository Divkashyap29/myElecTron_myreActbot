import requests
from agent.tools import Tool


class WeatherTool(Tool):
    def __init__(self):
        super().__init__(
            name='get_weather',
            description='Get current weather for a city using wttr.in (no API key needed).',
            parameters={
                'city': {'type': 'string', 'description': 'City name'},
            }
        )

    def execute(self, city='', **kwargs) -> str:
        try:
            url = f"https://wttr.in/{city}?format=j1"
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            current = data['current_condition'][0]
            desc = current['weatherDesc'][0]['value']
            temp_c = current['temp_C']
            temp_f = current['temp_F']
            feels_c = current['FeelsLikeC']
            humidity = current['humidity']
            wind_kmph = current['windspeedKmph']
            wind_dir = current['winddir16Point']
            return (
                f"Weather in {city}:\n"
                f"- Condition: {desc}\n"
                f"- Temperature: {temp_c}°C ({temp_f}°F), feels like {feels_c}°C\n"
                f"- Humidity: {humidity}%\n"
                f"- Wind: {wind_kmph} km/h {wind_dir}"
            )
        except Exception as e:
            return f"Error getting weather: {e}"
