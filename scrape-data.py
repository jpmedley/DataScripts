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


def getResponse(year, stateId, crimeCrossId):

  # StateId=1& BJSPopulationGroupId=& CrimeCrossId=102& DataType=1& YearStart=2014& NextPage=Get+Table
  params = urllib.urlencode({'StateId': stateId, 
                             # 'BJSPopulationGroupId': VIOLENT_CRIME_RATES, 
                             'BJSPopulationGroupId': '',
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
             "Origin": "https://www.ucrdatatool.gov",
             "User-Agent": "Mozilla/5.0 (X11; CrOS armv7l 6812.88.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.153 Safari/537.36",
             "Content-Type": "application/x-www-form-urlencoded",
             "Referer": "https://www.ucrdatatool.gov/Search/Crime/Local/OneYearofDataStepTwo.cfm",
             "Accept-Encoding": "gzip, deflate, br",
             "Accept-Language": "en-US,en;q=0.8",
             "Cookie": "fsr.s=%7B%22v2%22%3A-2%2C%22v1%22%3A1%2C%22cp%22%3A%7B%22cxreplayaws%22%3A%22true%22%7D%2C%22rid%22%3A%22d464cf3-84849867-6167-1436-77641%22%2C%22to%22%3A4%2C%22c%22%3A%22http%3A%2F%2Fwww.ucrdatatool.gov%2FSearch%2FCrime%2FLocal%2FTrendsInOneVarStepTwo.cfm%22%2C%22pv%22%3A87%2C%22lc%22%3A%7B%22d0%22%3A%7B%22v%22%3A87%2C%22s%22%3Atrue%7D%7D%2C%22cd%22%3A0%2C%22sd%22%3A0%2C%22l%22%3A%22en%22%2C%22i%22%3A1%2C%22t%22%3A1%7D; BIGipServerbjs_http_pool=940669706.20480.0000; CFID=143409549; CFTOKEN=e8bb1aa183483088-7C40B983-AE8D-264B-134F49227B887381; topItem=1c; _gat_UA-49393820-1=1; _ga=GA1.2.947731664.1442451395; acs.t=%7B%22_ckX%22%3A1494467930367%2C%22rid%22%3A%22d464c27-83930372-b8e9-69ca-436fe%22%2C%22cp%22%3A%7B%22url%22%3A%22https%3A%2F%2Fwww.ucrdatatool.gov%2FSearch%2FCrime%2FLocal%2FRunCrimeOneYearofData.cfm%22%2C%22terms%22%3A%22%22%2C%22browser%22%3A%22Chrome%2056%22%2C%22os%22%3A%22Windows%22%2C%22flash%22%3A%2224.0%22%2C%22hosted%22%3A%22true%22%2C%22referrer%22%3A%22%22%2C%22site%22%3A%22bjs-gov%22%2C%22trigger_version%22%3A%2219.0.35%22%2C%22pv%22%3A%227%22%2C%22locale%22%3A%22en%22%2C%22cxreplayaws%22%3A%22true%22%2C%22dn%22%3A%22default%22%7D%2C%22pl%22%3A1%2C%22pv%22%3A7%2C%22def%22%3A0%2C%22browsepv%22%3A7%2C%22rc%22%3A%22true%22%2C%22grft%22%3A1486698161412%2C%22mid%22%3A%22d464c27-83640095-c961-f441-9708c%22%2C%22rt%22%3Afalse%2C%22cncl%22%3Afalse%2C%22rpid%22%3A%22d464c27-83640095-fede-b129-09e9d%22%2C%22dn%22%3A%22default%22%2C%22i%22%3A%22a%22%2C%22rw%22%3A1494472689911%7D"}

  conn = httplib.HTTPConnection("https://www.ucrdatatool.gov", timeout=5)
  url = "/Search/Crime/Local/RunCrimeOneYearofData.cfm"
  conn.request("POST", url, params, headers)
  try:
    response = conn.getresponse()
    headers = response.getheaders()
    for h in headers:
      print h
    print response.status
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
    while (year < end):
      try:
        response = getResponse(str(year), city['State ID'], city['Crime Cross ID'])
      except socket.timeout:
        log_string = "Can't find %s" % (city['City'] + ", " + str(year))
        logFile.write(log_string)
        print log_string
        year += 1
        continue
      except:
        continue
      data = response.read()
      fileName = OUT_PATH + city['City'] + str(year) + ".html" 
      dataFile = open(fileName, 'w')
      print data
      dataFile.write(data)
      dataFile.close()
      year += 1

  print ("%s cities processed." % str(cityCount))
  logFile.close()

getCityData(sys.argv[1], sys.argv[2])