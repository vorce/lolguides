# 2011 - 2012 Joel Carlbark
#

from BeautifulSoup import BeautifulSoup
import urllib2
import re
import json
import time
import httplib
import threading, signal
import lolpro, clg, solomid

from scrapeutils import *

champion_url = 'http://na.leagueoflegends.com/champions'

# {url:[name, rating, updateDate]}
# Akali : [dict1, dict2]

class SourceScraper(threading.Thread):
    def __init__(self, champs, source):
        threading.Thread.__init__(self, name='Lolguides scraper, source {0}'.format(source))
        self._finished = threading.Event()
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self._champs = champs
        self._source = source

        if source == 0:
            self._outjson = 'solomid_data.json'
        elif source == 1:
            self._outjson = 'clg_data.json'
        elif source == 2:
            self._outjson = 'lolpro_data.json'

    def shutdown(self, timeout=None):
        self._finished.set()

    def run(self):
        self.getGuideData()

    def getGuideData(self):
        guideMap = {}

        for c in self._champs:
            print("{0}: Getting guide data for {1}".format(self.getName(), c))
            cClean = cleanName(c)

            if self._source == 0:
                # solomidUrl = 'http://www.solomid.net/guide/champion.php?name={0}'.format(cClean)
                solomidUrl = 'http://www.solomid.net/guides.php?champ={0}'.format(cClean)
                solomidGuides = solomid.getGuides(solomidUrl)
                solomidTopGuides = filterTop(solomidGuides)
                #print solomidTopGuides

                #print('----------------------')
                solomidNewGuide = filterNewest(solomidGuides)
                guideMap[c] = [solomidTopGuides, solomidNewGuide]

            elif self._source == 1:
                clgUrl = 'http://www.clgaming.net/guides/?champion={0}'.format(self._champs[c])
                clgGuides = clg.getGuides(clgUrl)
                clgTopGuides = filterTop(clgGuides)
                clgNewGuide = filterNewest(clgGuides)
                guideMap[c] = [clgTopGuides, clgNewGuide]
            
            elif self._source == 2:
                (ltop, lnew) = lolpro.getGuideData(c)
                guideMap[c] = [ltop, lnew]

            time.sleep(0.01)

        self.dumpJSON(guideMap)
        print("{0}: Done, wrote {1}".format(self.getName(), self._outjson))

    def dumpJSON(self, dataz):
        fp = open(self._outjson, 'w')
        json_out = json.dumps(dataz, indent=2)
        fp.write(json_out)
        fp.close()

        
def getGuideData(champs):
    tsmscraper = SourceScraper(champs, 0)
    clgscraper = SourceScraper(champs, 1)
    lolproscraper = SourceScraper(champs, 2)

    tsmscraper.start()
    clgscraper.start()
    lolproscraper.start()

    tsmscraper.join()
    clgscraper.join()
    lolproscraper.join()

if __name__ == '__main__':
    getGuideData(clgChamps)

