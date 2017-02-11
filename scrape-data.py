#!/usr/bin/python

from datetime import date

import httplib, urllib
import json
import socket
import sys

SCRAPE_LOG = "scrape" + str(date.today()) + ".log"
CITIES_FILE = "city-ids.json"
OUT_PATH = "out/"

VIOLENT_CRIME_RATES = 2

logFile = open(SCRAPE_LOG, 'a')

def Cities():
  citiesFile = open(CITIES_FILE, 'r')
  cityData = citiesFile.read()
  citiesFile.close()
  cityDataDict = json.loads(cityData)
  for city in cityDataDict:
    yield city
    
def logger(message, err=''):


def getResponse(year, stateId, crimeCrossId):

  # StateId=1& BJSPopulationGroupId=& CrimeCrossId=102& DataType=1& YearStart=2014& NextPage=Get+Table
  params = urllib.urlencode({'StateId': stateId, 
                             # 'BJSPopulationGroupId': VIOLENT_CRIME_RATES, 
                             'BJSPopulationGroupId': '',
                             'CrimeCrossId': crimeCrossId, 
                             'DataType': 3,
                             'YearStart': year,
                             'NextPage': 'Get+Table'})
  
  headers = {
       "Content-Type": "application/x-www-form-urlencoded",
       "Origin": "https://www.ucrdatatool.gov",
       "Upgrade-Insecure-Requests": "1",
       "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36"
    }

  try:
    conn = httplib.HTTPSConnection("www.ucrdatatool.gov", timeout=5)
    url = "/Search/Crime/Local/RunCrimeOneYearofData.cfm"
    conn.request("POST", url, params, headers)
  except:
    print("Unexpected error:", sys.exc_info()[0])
  
  try:
    response = conn.getresponse()
  except:
    raise
  return response
# End getResponse

def getCityData(startYear, endYear):
  cities = Cities()
  cityCount = 0
  for city in cities:
    cityCount += 1
    print ("now retrieving data for " + city['City'])
    year = int(startYear)
    end = int(endYear)
    while (year <= end):
      try:
        response = getResponse(str(year), city['State ID'], city['Crime Cross ID'])
        data = response.read()
      except socket.timeout:
        log_string = "Can't find %s" % (city['City'] + ", " + str(year))
        logFile.write(log_string)
        print log_string
        year += 1
        continue
      except:
        continue
      fileName = OUT_PATH + city['City'] + str(year) + ".html" 
      dataFile = open(fileName, 'w')
      dataFile.write(data)
      dataFile.close()
      year += 1

  print ("%s cities processed." % str(cityCount))
  logFile.close()

getCityData(sys.argv[1], sys.argv[2])