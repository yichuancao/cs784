#!/usr/bin/env python
# encoding=utf8
from bs4 import BeautifulSoup
import urllib2
import time
import sys  
import re

reload(sys)  
sys.setdefaultencoding('utf8')

# grab all beer data
style_url = 'http://www.beeradvocate.com/beer/style/'
opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
response = opener.open(style_url)
html = response.read()
soup = BeautifulSoup(html)
beerStylePageAllLinks = soup.find_all("a")
with open('beerAdvocateData.txt', 'a') as f:
    for i in range(0, len(beerStylePageAllLinks)):
        try:
            if beerStylePageAllLinks[i]['href'][0:12] == "/beer/style/":
                if beerStylePageAllLinks[i]['href'] == "/beer/style/" or beerStylePageAllLinks[i]['href'] == "/beer/style/#navigation":
                    continue
                else:
                    beerStyleLink = beerStylePageAllLinks[i]['href']
                    beerStyleName = beerStylePageAllLinks[i].text
                    j = 0
                    threshold = 50000
                    while j <= threshold:
                        response = opener.open('http://www.beeradvocate.com' + beerStyleLink + '?sort=revsD&start=' + str(j))
                        html = response.read()
                        soup = BeautifulSoup(html)
                        data = soup.find_all("div", id="ba-content")
                        matchObj = re.findall(r'[0-9]+', data[0].find_all("b")[2].text)
                        if matchObj:
                            threshold = 50 * int(int(matchObj[2]) / 50)
                        info = data[0].find_all("a")
                        for k in range(0, len(info)):
                            if info[k].find("b") is not None and info[k].find("b").text != "-" and info[k].find("b").text.isdigit() == False:
                                beerName = info[k].find("b").text
                                f.write(beerName)
                                f.write(",")
                                brewery = info[k + 1].text
                                f.write(brewery)
                                f.write(",")
                                f.write(beerStyleName)
                                f.write("\n")
                        j += 50
                        time.sleep(5)
        except UnicodeEncodeError:
            print "error"
            time.sleep(5)
        except KeyError:
            continue
        time.sleep(5)