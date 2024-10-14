import json
import os

import pyfiglet
import requests
from bs4 import BeautifulSoup

url_countries = "https://world-weather.info/forecast/"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Cookie": f"celsius=0",
}
Countries = []
Cities = []
weather_Cities = []


def clear_console():
    # Clear the console based on the operating system
    os.system("cls" if os.name == "nt" else "clear")


def getSoupValue(url):
    response = requests.get(url=url, headers=HEADERS)
    response.raise_for_status()
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return None


def fahrenheit_to_celsius(fahrenheit):
    # Convert Fahrenheit to Celsius using the formula
    celsius = (int(fahrenheit) - 32) * 5 / 9
    return round(celsius, 1)


def choose_country(url):
    soup = getSoupValue(url)
    country_names = soup.find_all("li", class_="country-block")
    global Countries
    Countries = [name.find("a").get_text() for name in country_names]
    for index, name in enumerate(Countries):
        print(f"Number : {index+1} - Country name {name}")


def choose_City(countryIndex):
    countryName = Countries[countryIndex - 1]
    soup = getSoupValue(f"https://world-weather.info/forecast/{countryName}/")
    city_names_values = soup.find_all("li", class_="city-block")
    global Cities
    Cities = [
        {
            "Index": index + 1,
            "CityName": city.find("a").get_text(),
            "CityValue": fahrenheit_to_celsius(
                city.find("span").get_text().replace("+", "")
            ),
        }
        for index, city in enumerate(city_names_values)
    ]
    for city in Cities:
        print(
            f"Number: {city['Index']} - City name: {city['CityName']} - City value: {city['CityValue']}"
        )


def exportJson(index_City, index_Country):
    save = int(input("do you want to save the cities into json file yes:1 , no:0 : "))
    if save == 1:
        with open(f"cities_{Cities[index_City]['CityName']}.json", "w") as json_file:
            name = Countries[index_Country - 1]
            json.dump(
                {"Country": name, "Cities": Cities},
                json_file,
                indent=4,
                ensure_ascii=False,
            )


def big_Text(value):
    big_text = pyfiglet.figlet_format(value)
    print(big_text)


if __name__ == "__main__":
    while 1:
        big_Text("Welcome To Weather Spring")
        choose_country(url_countries)
        index_Country = int(input("What is your country Number : "))
        clear_console()
        big_Text("Welcome To Weather Spring")
        choose_City(index_Country)
        index_City = int(input("What is your City Number : "))
        clear_console()
        big_Text("Welcome To Weather Spring")
        big_Text(f"your weather is {Cities[index_City-1]['CityValue']}")
        exportJson(index_City, index_Country)
