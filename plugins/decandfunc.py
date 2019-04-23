from discord.ext import commands
import json
import requests
import random


def is_administrator():
    def predicate(context):
        user_permission = context.author.permissions_in(context.channel)
        return user_permission.administrator
    return commands.check(predicate)


def get_weather_broadcast(city):
    api_key = 'fc742b2e828d78d26b3aea0e896662e3'
    response = requests.get(
        "http://api.openweathermap.org/data/2.5/forecast?q=" + city +
        "&APPID=" + api_key)
    request = json.loads(response.text)
    if request['cod'] != '200':
        return request["message"]
    today_date = request['list'][0]
    result = ("Temperature: " "%.1f" % float(today_date['main']['temp'] - 273) + "\n"
              "Humidity: " + str(today_date['main']['humidity']) + " % \n"
              "Cloudiness: " + today_date['weather'][0]['description'] + " \n"
              "Wind: " + str(today_date['wind']['speed']))
    return result


def get_news(country):
    api_key = 'cd3e43d7f8a24e27bf10996605d66165'
    url = ('https://newsapi.org/v2/top-headlines?'
           'country=' + country + '&'
           'apiKey=' + api_key)
    response = requests.get(url)
    request = json.loads(response.text)
    if (not request['status'] == 'ok') or int(request['totalResults']) == 0:
        return 'Error'
    news = request['articles']
    r = random.randint(0, int(request['totalResults']) - 1)
    news = news[r]
    result = (news['title'] + "\n" +
              news['description'] + "\n" +
              "source: " + news['url'])
    return result


def get_helpme(*args):
    with open("helpmetext.json", "r") as f:
        request = json.load(f)
    which_text = ''
    if len(args) == 0:
        which_text = "MAIN"
    elif len(args) == 1:
        if args[0].upper() in request.keys():
            which_text = args[0].upper()
    else:
        return 'Error'
    result = ''
    for i in request[which_text]:
        result = result + i
    return result
