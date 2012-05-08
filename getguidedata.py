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

'''
riotChamps = {
'evelynn': 28,
'nunu': 20,
'swain': 50,
'taric': 44,
'missfortune': 21,
'chogath': 31,
'graves': 104,
'jax': 24,
'drmundo': 36,
'shaco': 35,
'morgana': 25,
'nidalee': 76,
'kassadin': 38,
'sona': 37,
'cassiopeia': 69,
'skarner': 72,
'malzahar': 90,
'amumu': 32,
'olaf': 2,
'vladimir': 8,
'riven': 92,
'gangplank': 41,
'poppy': 78,
'volibear': 106,
'kennen': 85,
'ryze': 13,
'gragas': 79,
'garen': 86,
'shen': 98,
'karthus': 30,
'sion': 14,
'alistar': 12,
'leblanc': 7,
'ezreal': 81,
'fiddlesticks': 9,
'kogmaw': 96,
'lux': 99,
'leesin': 64,
'anivia': 34,
'tryndamere': 23,
'nasus': 75,
'heimerdinger': 74,
'nocturne': 56,
'ashe': 22,
'xinzhao': 5,
'malphite': 54,
'irelia': 39,
'annie': 1,
'twitch': 29,
'kayle': 10,
'janna': 40,
'blitzcrank': 53,
'talon': 91,
'vayne': 67,
'katarina': 55,
'twistedfate': 4,
'warwick': 19,
'fizz': 105,
'renekton': 58,
'brand': 63,
'corki': 42,
'maokai': 57,
'yorick': 83,
'urgot': 6,
'tristana': 18,
'galio': 3,
'sivir': 15,
'orianna': 61,
'jarvaniv': 59,
'soraka': 16,
'caitlyn': 51,
'veigar': 45,
'pantheon': 80,
'trundle': 48,
'shyvana': 102,
'udyr': 77,
'masteryi': 11,
'mordekaiser': 82,
'zilean': 26,
'rammus': 33,
'rumble': 68,
'wukong': 62,
'xerath': 101,
'singed': 27,
'karma': 43,
'akali': 84,
'leona': 89,
'teemo': 17,
'ahri':103
# viktor
# sejuani
# ziggs
# nautilus
# fiora
}

clgChampsClean = {
'evelynn': 22,
'nunu': 9,
'swain': 61,
'taric': 31,
'missfortune': 59,
'chogath': 25,
'graves': 85,
'jax': 5,
'drmundo': 32,
'shaco': 40,
'morgana': 8,
'nidalee': 42,
'kassadin': 29,
'sona': 60,
'cassiopeia': 66,
'skarner': 81,
'malzahar': 52,
'amumu': 24,
'olaf': 53,
'vladimir': 56,
'riven': 83,
'gangplank': 30,
'poppy': 43,
'volibear': 88,
'kennen': 49,
'ryze': 10,
'gragas': 45,
'garen': 50,
'shen': 48,
'karthus': 23,
'sion': 11,
'alistar': 1,
'leblanc': 63,
'ezreal': 47,
'fiddlesticks': 4,
'kogmaw': 54,
'lux': 62,
'leesin': 73,
'anivia': 26,
'tryndamere': 20,
'nasus': 38,
'heimerdinger': 39,
'nocturne': 72,
'ashe': 3,
'xinzhao': 55,
'malphite': 33,
'irelia': 64,
'annie': 2,
'twitch': 21,
'kayle': 6,
'janna': 34,
'blitzcrank': 35,
'talon': 82,
'vayne': 76,
'katarina': 36,
'twistedfate': 16,
'warwick': 17,
'fizz': 87,
'renekton': 68,
'brand': 74,
'corki': 37,
'maokai': 70,
'yorick': 78,
'urgot': 58,
'tristana': 15,
'galio': 57,
'sivir': 12,
'orianna': 77,
'jarvaniv': 71,
'soraka': 13,
'caitlyn': 67,
'veigar': 28,
'pantheon': 44,
'trundle': 65,
'shyvana': 86,
'udyr': 41,
'masteryi': 7,
'mordekaiser': 46,
'zilean': 18,
'rammus': 27,
'rumble': 75,
'wukong': 80,
'xerath': 84,
'singed': 19,
'karma': 69,
'akali': 51,
'leona': 79,
'teemo': 14,
'ahri':89,
'viktor':90,
'sejuani':91,
'ziggs':92
}
'''

clgChamps = {
'Evelynn': 22,
'Nunu': 9,
'Swain': 61,
'Taric': 31,
'Miss Fortune': 59,
'Cho\'Gath': 25,
'Graves': 85,
'Jax': 5,
'Dr. Mundo': 32,
'Shaco': 40,
'Morgana': 8,
'Nidalee': 42,
'Kassadin': 29,
'Sona': 60,
'Cassiopeia': 66,
'Skarner': 81,
'Malzahar': 52,
'Amumu': 24,
'Olaf': 53,
'Vladimir': 56,
'Riven': 83,
'Gangplank': 30,
'Poppy': 43,
'Volibear': 88,
'Kennen': 49,
'Ryze': 10,
'Gragas': 45,
'Garen': 50,
'Shen': 48,
'Karthus': 23,
'Sion': 11,
'Alistar': 1,
'LeBlanc': 63,
'Ezreal': 47,
'Fiddlesticks': 4,
'Kog\'Maw': 54,
'Lux': 62,
'Lee Sin': 73,
'Anivia': 26,
'Tryndamere': 20,
'Nasus': 38,
'Heimerdinger': 39,
'Nocturne': 72,
'Ashe': 3,
'Xin Zhao': 55,
'Malphite': 33,
'Irelia': 64,
'Annie': 2,
'Twitch': 21,
'Kayle': 6,
'Janna': 34,
'Blitzcrank': 35,
'Talon': 82,
'Vayne': 76,
'Katarina': 36,
'Twisted Fate': 16,
'Warwick': 17,
'Fizz': 87,
'Renekton': 68,
'Brand': 74,
'Corki': 37,
'Maokai': 70,
'Yorick': 78,
'Urgot': 58,
'Tristana': 15,
'Galio': 57,
'Sivir': 12,
'Orianna': 77,
'Jarvan IV': 71,
'Soraka': 13,
'Caitlyn': 67,
'Veigar': 28,
'Pantheon': 44,
'Trundle': 65,
'Shyvana': 86,
'Udyr': 41,
'Master Yi': 7,
'Mordekaiser': 46,
'Zilean': 18,
'Rammus': 27,
'Rumble': 75,
'Wukong': 80,
'Xerath': 84,
'Singed': 19,
'Karma': 69,
'Akali': 51,
'Leona': 79,
'Teemo': 14,
'Ahri':89,
'Viktor':90,
'Sejuani':91,
'Ziggs':92,
'Nautilus':93,
'Fiora':94,
'Lulu':95,
'Hecarim':96,
'Varus':97
}

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
                solomidUrl = 'http://solomid.net/guides.php?champ={0}'.format(cClean)
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

