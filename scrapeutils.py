import urllib2
import httplib
import math
import time
import json


class ScrapeUtils:
    def __init__(self):
        self.clgChamps = [
            {'name': 'Evelynn', 'id': 22},
            {'name': 'Nunu', 'id': 9},
            {'name': 'Swain', 'id': 61},
            {'name': 'Taric', 'id': 31},
            {'name': 'Miss Fortune', 'id': 59},
            {'name': 'Cho\'Gath', 'id': 25},
            {'name': 'Graves', 'id': 85},
            {'name': 'Jax', 'id': 5},
            {'name': 'Dr. Mundo', 'id': 32},
            {'name': 'Shaco', 'id': 40},
            {'name': 'Morgana', 'id': 8},
            {'name': 'Nidalee', 'id': 42},
            {'name': 'Kassadin', 'id': 29},
            {'name': 'Sona', 'id': 60},
            {'name': 'Cassiopeia', 'id': 66},
            {'name': 'Skarner', 'id': 81},
            {'name': 'Malzahar', 'id': 52},
            {'name': 'Amumu', 'id': 24},
            {'name': 'Olaf', 'id': 53},
            {'name': 'Vladimir', 'id': 56},
            {'name': 'Riven', 'id': 83},
            {'name': 'Gangplank', 'id': 30},
            {'name': 'Poppy', 'id': 43},
            {'name': 'Volibear', 'id': 88},
            {'name': 'Kennen', 'id': 49},
            {'name': 'Ryze', 'id': 10},
            {'name': 'Gragas', 'id': 45},
            {'name': 'Garen', 'id': 50},
            {'name': 'Shen', 'id': 48},
            {'name': 'Karthus', 'id': 23},
            {'name': 'Sion', 'id': 11},
            {'name': 'Alistar', 'id': 1},
            {'name': 'LeBlanc', 'id': 63},
            {'name': 'Ezreal', 'id': 47},
            {'name': 'Fiddlesticks', 'id': 4},
            {'name': 'Kog\'Maw', 'id': 54},
            {'name': 'Lux', 'id': 62},
            {'name': 'Lee Sin', 'id': 73},
            {'name': 'Anivia', 'id': 26},
            {'name': 'Tryndamere', 'id': 20},
            {'name': 'Nasus', 'id': 38},
            {'name': 'Heimerdinger', 'id': 39},
            {'name': 'Nocturne', 'id': 72},
            {'name': 'Ashe', 'id': 3},
            {'name': 'Xin Zhao', 'id': 55},
            {'name': 'Malphite', 'id': 33},
            {'name': 'Irelia', 'id': 64},
            {'name': 'Annie', 'id': 2},
            {'name': 'Twitch', 'id': 21},
            {'name': 'Kayle', 'id': 6},
            {'name': 'Janna', 'id': 34},
            {'name': 'Blitzcrank', 'id': 35},
            {'name': 'Talon', 'id': 82},
            {'name': 'Vayne', 'id': 76},
            {'name': 'Katarina', 'id': 36},
            {'name': 'Twisted Fate', 'id': 16},
            {'name': 'Warwick', 'id': 17},
            {'name': 'Fizz', 'id': 87},
            {'name': 'Renekton', 'id': 68},
            {'name': 'Brand', 'id': 74},
            {'name': 'Corki', 'id': 37},
            {'name': 'Maokai', 'id': 70},
            {'name': 'Yorick', 'id': 78},
            {'name': 'Urgot', 'id': 58},
            {'name': 'Tristana', 'id': 15},
            {'name': 'Galio', 'id': 57},
            {'name': 'Sivir', 'id': 12},
            {'name': 'Orianna', 'id': 77},
            {'name': 'Jarvan IV', 'id': 71},
            {'name': 'Soraka', 'id': 13},
            {'name': 'Caitlyn', 'id': 67},
            {'name': 'Veigar', 'id': 28},
            {'name': 'Pantheon', 'id': 44},
            {'name': 'Trundle', 'id': 65},
            {'name': 'Shyvana', 'id': 86},
            {'name': 'Udyr', 'id': 41},
            {'name': 'Master Yi', 'id': 7},
            {'name': 'Mordekaiser', 'id': 46},
            {'name': 'Zilean', 'id': 18},
            {'name': 'Rammus', 'id': 27},
            {'name': 'Rumble', 'id': 75},
            {'name': 'Wukong', 'id': 80},
            {'name': 'Xerath', 'id': 84},
            {'name': 'Singed', 'id': 19},
            {'name': 'Karma', 'id': 69},
            {'name': 'Akali', 'id': 51},
            {'name': 'Leona', 'id': 79},
            {'name': 'Teemo', 'id': 14},
            {'name': 'Ahri', 'id': 89},
            {'name': 'Viktor', 'id': 90},
            {'name': 'Sejuani', 'id': 91},
            {'name': 'Ziggs', 'id': 92},
            {'name': 'Nautilus', 'id': 93},
            {'name': 'Fiora', 'id': 94},
            {'name': 'Lulu', 'id': 95},
            {'name': 'Hecarim', 'id': 96},
            {'name': 'Varus', 'id': 97},
            {'name': 'Darius', 'id': 98},
            {'name': 'Draven', 'id': 99},
            {'name': 'Jayce', 'id': 100},
            {'name': 'Zyra', 'id': 101},
            {'name': 'Diana', 'id': 102},
            {'name': 'Rengar', 'id': 103},
            {'name': 'Syndra', 'id': 104},
            {'name': 'Kha\'Zix', 'id': 105},
            {'name': 'Elise', 'id': 106},
            {'name': 'Zed', 'id': 107},
            {'name': 'Nami', 'id': 108}
        ]
        self.elophant_key = 'Dy48E5sTZp2Kq5f4oqCR'
        self.elophant_champs = {}

    def getChampions(self):
        if len(self.elophant_champs) == 0:
            try:
                fp = urllib2.urlopen('http://elophant.com/api/v1/champions?key={0}'.format(self.elophant_key))
                self.elophant_champs = json.load(fp)
            except urllib2.HTTPError:
                self.elophant_champs = self.clgChamps

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

