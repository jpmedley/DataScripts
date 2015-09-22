#!/usr/bin/python
# https://docs.python.org/2/library/httplib.html

import httplib, urllib
import itertools
import json
from StringIO import StringIO

SCRAPE_LOG = "scrape.log"
CITIES_FILE = "city-ids.json"

VIOLENT_CRIME_RATES = 2

logFile = open(SCRAPE_LOG, 'a')

def Cities():
  citiesFile = open(CITIES_FILE, 'r')
  cityData = citiesFile.read()
  citiesFile.close()
  cityDataDict = json.loads(cityData)
  for city in cityDataDict:
    yield city


def getResponse(year, stateId, crimeCrossId):

  params = urllib.urlencode({'StateId': stateId, 
                             'BJSPopulationGroupId': VIOLENT_CRIME_RATES, 
                             'CrimeCrossId': crimeCrossId, 
                             'DataType': 3,
                             'YearStart': year,
                             'NextPage': 'Get+Table'})

  headers = {"POST": "/Search/Crime/Local/RunCrimeOneYearofData.cfm HTTP/1.1",
             "Host": "www.ucrdatatool.gov",
             "Connection": "keep-alive",
             "Content-Length": "97",
             "Cache-Control": "max-age=0",
             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
             "Origin": "http://www.ucrdatatool.gov",
             "User-Agent": "Mozilla/5.0 (X11; CrOS armv7l 6812.88.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.153 Safari/537.36",
             "Content-Type": "application/x-www-form-urlencoded",
             "Referer": "http://www.ucrdatatool.gov/Search/Crime/Local/OneYearofDataStepTwo.cfm",
             "Accept-Encoding": "gzip, deflate",
             "Accept-Language": "en-US,en;q=0.8",
             "Cookie": "topItem=1c; CFID=106361124; CFTOKEN=a10fcd62b8337ef1-12AD05B5-EC17-3180-BF29864F30881E06; _ga=GA1.2.762111162.1442274583"}

  conn = httplib.HTTPConnection("www.ucrdatatool.gov")

  url = "/Search/Crime/Local/RunCrimeOneYearofData.cfm"
  conn.request("POST", url, params, headers)
  response = conn.getresponse()
  log_string = "%s: %s\n" % (response.status, response.reason)
  logFile.write(log_string)
  return response
  conn.close()
# End getResponse

cities = Cities()
for city in cities:
  year = 1985
  while (year < 2014):
    response = getResponse(str(year), city['State ID'], city['Crime Cross ID'])
    data = response.read()
    year += 1

    fileName = city['City'] + str(year) + ".html"
    dataFile = open(fileName, 'a')
    dataFile.write(data)
    dataFile.close()

logFile.close()

