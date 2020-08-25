from django.shortcuts import render
import requests
from django.http import HttpResponse
# from urllib import request
# Create your views here.
################################
# import csv
# from .models import Data
# def export(self):
#     response = HttpResponse(content_type='text/csv')
#
#     writer = csv.writer(response)
#     writer.writerow(['temp','city'])
#
#     for data in Data.objects.all().values_list('temp','city'):
#         writer.writerow(data)
#
#     response['Content-Disposition'] = "attachment; filename='Data.csv'"
#
#     return response


################################
def get_html_content(request):

    city = request.GET.get('city')
    city = city.replace(" ", "+")
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.google.com/search?q=weather+{city}').text
    return html_content

def home(request):
    result = None
    if 'city' in request.GET:
        # fetch the weather from Google.
        html_content = get_html_content(request)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        result = {}
        # extract region
        result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
        # extract temperature now
        result['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
        result['temp_now_f'] = soup.find("span", attrs={"id": "wob_ttm"}).text
        # get the day and hour now
        result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
        # get the actual weather
        result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
        # get the actual ppt
        result['ppt'] = soup.find("span",attrs = {'id':'wob_pp'}).text
        # get the actual Humidity
        result['hm'] = soup.find("span",attrs = {'id':'wob_hm'}).text
        # get the actual wind
        result['ws'] = soup.find("span",attrs = {'id':'wob_ws'}).text



    return render(request, 'core/home.html', {'result': result})
