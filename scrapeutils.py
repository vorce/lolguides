import urllib2
import httplib
import math
import time
import json


class ScrapeUtils:
    def __init__(self):
        self.clgChamps = {
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
        'Ahri': 89,
        'Viktor': 90,
        'Sejuani': 91,
        'Ziggs' :92,
        'Nautilus': 93,
        'Fiora': 94,
        'Lulu': 95,
        'Hecarim': 96,
        'Varus': 97,
        'Darius': 98,
        'Draven': 99,
        'Jayce': 100,
        'Zyra': 101,
        'Diana': 102,
        'Rengar': 103,
        'Syndra': 104,
        'Kha\'Zix': 105,
        'Elise': 106,
        'Zed':107
        }
        self.elophant_key = 'Dy48E5sTZp2Kq5f4oqCR'
        self.elophant_champs = {}

    def getChampions(self):
        if len(self.elophant_champs) == 0:
            fp = urllib2.urlopen('http://elophant.com/api/v1/champions?key={0}'.format(self.elophant_key))
            self.elophant_champs = json.load(fp)
        return self.elophant_champs

    def csName(self, c):
        csn = c
        csn = csn.replace(' ', '-')
        csn = csn.replace("'", '')
        csn = csn.replace('.', '')
        return csn

    def cleanName(self, c):
        cleanName = c.lower()
        cleanName = cleanName.replace('.', '')
        cleanName = cleanName.replace("'", '')
        cleanName = cleanName.replace(' ', '')
        cleanName = cleanName.lower()
        return cleanName

    # slooow
    def filterTop(self, guides):
        topGuides = {}
        featuredGuides = {}
        maxTop = 2

        if len(guides) <= maxTop:
            return guides

        for g in guides:
            [name, rating, update, author, featured] = guides[g]
            if featured and update < 365:
                featuredGuides[g] = guides[g]

        guidesIncluded = 0
        while guidesIncluded < maxTop and len(guides) >= maxTop:
            highestRating = -99999
            topGuide = None

            for g in guides:
                [name, rating, update, author, featured] = guides[g]
                if rating > highestRating and g not in topGuides \
                   and g not in featuredGuides and update < 365:
                    highestRating = rating
                    topGuide = g

            if topGuide is not None:
                topGuides[topGuide] = guides[topGuide]
            guidesIncluded = guidesIncluded + 1

        return dict(topGuides.items() + featuredGuides.items())

    def filterNewest(self, guides):
        newGuides = {}
        maxNew = 1

        if len(guides) <= maxNew:
            return guides

        guidesIncluded = 0
        while guidesIncluded < maxNew and len(guides) >= maxNew:
            newest = 9999
            newGuide = None

            for g in guides:
                [name, rating, update, author, featured] = guides[g]
                if update < newest:
                    newest = update
                    newGuide = g

            newGuides[newGuide] = guides[newGuide]
            guidesIncluded = guidesIncluded + 1

        return newGuides

    def getPage(self, url):
        page = None
        retry = True
        skip = False

        while retry:
            try:
                page = urllib2.urlopen(url, timeout=60)
                retry = False
            except urllib2.HTTPError, e:
                if e.code == 404 or e.code == 403:
                    retry = False
                    skip = True
                else:
                    print("Exception: {0}".format(e))
                    print("Waiting 10 seconds, then retrying")
                    time.sleep(10)  # wait 10 seconds then try again
            except urllib2.URLError, e:
                print("Exception: {0}".format(e))
                print("Waiting 10 seconds, then retrying")
                time.sleep(10)  # wait 10 seconds then try again
            except httplib.HTTPException:
                print("HTTPException")
                print("Waiting 10 seconds, then retrying")
                time.sleep(10)  # wait 10 seconds then try again

        return (page, skip)

    # https://possiblywrong.wordpress.com/2011/06/05/reddits-comment-ranking-algorithm/
    # Thanks!
    def confidence_fixed(self, ups, downs):
        if ups == 0:
            return -downs
        n = ups + downs
        z = 1.64485  # 1.0 = 85%, 1.6 = 95%
        phat = float(ups) / n
        return int(((phat+z*z/(2*n)-z*math.sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n))*100)

