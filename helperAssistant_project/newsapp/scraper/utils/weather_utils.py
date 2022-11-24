from bs4 import BeautifulSoup
import requests
import json

HEADERS = {
    "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36"
}


def get_forecast(code):
    forecast = {}
    response = requests.get(f"https://meteo.ua/ua/{code}", headers=HEADERS).text
    soup = BeautifulSoup(response, 'lxml')
    try:
        title = soup.find('div', class_="weather-detail__main-title js-weather-detail-value").text.strip().replace('\n', '')
        temperature = soup.find('div', class_='weather-detail__main-temp js-weather-detail-value').text.strip()
        state = soup.find('div', class_="weather-detail__main-specification js-weather-detail-value").text.strip().title()
        items = soup.find_all('div', class_="weather-detail__extra-item")
        fallout = items[0].text.replace('\n', ' ').strip()
        pressure = items[1].text.replace('\n', ' ').strip()
        wind = items[2].text.replace('\n', ' ').strip()
        humidity = items[3].text.replace('\n', ' ').strip()
        forecast['title'] = title
        forecast['temperature'] = temperature
        forecast['state'] = state
        forecast['fallout'] = fallout
        forecast['pressure'] = pressure
        forecast['wind'] = wind
        forecast['humidity'] = humidity
    except Exception as err:
        print(f'[ERROR]{err}')
    return forecast


if __name__ == '__main__':
    get_forecast('164/dnepr-dnepropetrovsk')
