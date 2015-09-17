#!/usr/bin/python
# https://docs.python.org/2/library/httplib.html

import httplib, urllib

SCRAPE_LOG = "scrape.log"
SCRAPE_DATA = "scrape.data"

logFile = open(SCRAPE_LOG, 'a')
dataFile = open(SCRAPE_DATA, 'a')
  

def getResponse():

  params = urllib.urlencode({'StateId': 33, 
                             'BJSPopulationGroupId': 2, 
                             'CrimeCrossId': 13794, 
                             'DataType': 3,
                             'YearStart': 1985,
                             'NextPage': 'Get+Table'})

  headers = {"Content-type": "application/x-www-form-urlencoded",
             "Accept": "text/plain"}

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

response = getResponse()

data = response.read()

dataFile.write(data)
dataFile.write("")

logFile.close()
dataFile.close()
