# 2011 - 2012 Joel Carlbark
#
import json
import time
import threading
import signal
import lolpro
import clg
import solomid
import lolking
import scrapeutils
import sys


class SourceScraper(threading.Thread):
    def __init__(self, scrape_util, source):
        threading.Thread.__init__(self, name='Guide scraper, source [{0}]'.format(source))
        self._finished = threading.Event()
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self._source = source
        self.scrape_util = scrape_util

        self._outjson = '{0}_data.json'.format(source)

    def shutdown(self, timeout=None):
        self._finished.set()

    def run(self):
        self.getGuideData()

    def getGuideData(self):
        guideMap = {}

        for i in self.scrape_util.getChampions():
            # Elophant "A champion with an id of "0" does not exist.
            # We use it to deal with exceptions."
            if i.get('id', 0) == 0:
                continue

            c = i.get('name')

            print("{0}: Getting guide data for {1}".format(self.getName(), c))
            cClean = self.scrape_util.cleanName(c)

            champURL = ''
            if self._source == 'solomid':
                champURL = 'http://www.solomid.net/guides.php?champ={0}'.format(cClean)
            elif self._source == 'clg':
                clgId = self.scrape_util.clgChamps[c]
                champURL = 'http://www.clgaming.net/guides/?champion={0}'.format(clgId)
            elif self._source == 'lolpro':
                champURL = 'http://www.lolpro.com/guides/{0}'.format(cClean)
            elif self._source == 'lolking':
                champURL = 'http://www.lolking.net/guides/list.php?champion={0}'.format(cClean)
            else:
                return guideMap

            page, skip = self.scrape_util.getPage(champURL)

            if self._source == 'solomid':
                solomidGuides = solomid.getGuides(page, skip, champURL,
                                                  self.scrape_util.confidence_fixed)
                solomidTopGuides = self.scrape_util.filterTop(solomidGuides)
                solomidNewGuides = self.scrape_util.filterNewest(solomidGuides)
                guideMap[c] = [solomidTopGuides, solomidNewGuides]
            elif self._source == 'clg':
                clgGuides = clg.getGuides(page, skip)
                clgTopGuides = self.scrape_util.filterTop(clgGuides)
                clgNewGuides = self.scrape_util.filterNewest(clgGuides)
                guideMap[c] = [clgTopGuides, clgNewGuides]
            elif self._source == 'lolpro':
                curseGuides = lolpro.getGuides(page, skip)
                curseTopGuides = self.scrape_util.filterTop(curseGuides)
                curseNewGuides = self.scrape_util.filterNewest(curseGuides)
                guideMap[c] = [curseTopGuides, curseNewGuides]
            elif self._source == 'lolking':
                kingGuides = lolking.getGuides(page, skip, champURL)
                kingTopGuides = self.scrape_util.filterTop(kingGuides)
                kingNewGuides = self.scrape_util.filterNewest(kingGuides)
                guideMap[c] = [kingTopGuides, kingNewGuides]

            time.sleep(0.01)

        self.dumpJSON(guideMap)
        print("{0}: Done, wrote {1}".format(self.getName(), self._outjson))

    def dumpJSON(self, dataz):
        with open(self._outjson, 'w') as fp:
            json_out = json.dumps(dataz, indent=2)
            fp.write(json_out)


def getGuideData(sources):
    scrape_util = scrapeutils.ScrapeUtils()
    scrape_util.getChampions()

    scrapers = []
    for s in sources:
       scrapers.append(SourceScraper(scrape_util, s)) 

    for s in scrapers:
        s.start()

    for s in scrapers:
        s.join()

# Ex: getguidedata.py solomid clg lolpro lolking
if __name__ == '__main__':
    getGuideData(sys.argv[1:])

