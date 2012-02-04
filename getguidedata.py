#
# MONSTER NOMNONOMONOMONOMOMOMONOM!!!
# I AM NOT SCARED [][][][]
#

from BeautifulSoup import BeautifulSoup
import urllib2
import re
import json
import time
import httplib
import threading, signal

champion_url = 'http://na.leagueoflegends.com/champions'

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
'Leblanc': 63,
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
'Xinzhao': 55,
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
'Masteryi': 7,
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
'Ziggs':92
}

def dumpJSON(dataz):
    fp = open('guide_data.json', 'w')
    json_out = json.dumps(dataz, indent=2)
    fp.write(json_out)
    fp.close()

def makeChampMap(champs):
    champIds = []
    champNames = []

    for c in champs:
        infoType = getattr(c, 'name', None)

        if infoType == 'a':
            champIds.append(getChampId(c))
        elif infoType == 'div':
            champName = getChampName(c)
            champNames.append(champName)
        else:
            pass #something's terribly wrong

    return dict(zip(champNames, champIds))


def getChampId(info):
    while getattr(info, 'name', None) != 'img':
        info = info.next

    champId = getattr(info, 'attrs', None)[0][1].split('/')[-1].split('.jpg')[0]
    return champId

def cleanName(c):
    cleanName = c.lower()
    cleanName = cleanName.replace('.', '')
    cleanName = cleanName.replace("'", '')
    cleanName = cleanName.replace(' ', '')
    return cleanName

def getChampName(info):
    champName = info.text.lower()
    champName = champName.replace('.', '')
    champName = champName.replace("'", '')
    champName = champName.replace(' ', '')
    return champName

# {url:[name, rating, updateDate]}
# Akali : [dict1, dict2]

def solomid_getGuides(url):
    retry = True
    while retry:
        try:
            page = urllib2.urlopen(url)
            retry = False
        except httplib.BadStatusLine, e:
            print("Exception: {0}".format(e))
            print("Line: {0}".format(e.line))
            print("Waiting 10 seconds, then retrying")
            time.sleep(10) # wait 10 seconds then try again

    soup = BeautifulSoup(page)
    guideList = soup.findAll(name="div", attrs={"class":["title", "rating", "author"]})
    urls = []
    names = []
    ratings = []
    updates = []
    authors = []
    featureds = [] # It's a word.

    for g in guideList:
        infoType = getattr(g, 'attrs', None)
        
        if infoType[0][1] == 'title':
            (url, name, update, featured) = solomid_getUrlNameUpdate(g)
            urls.append(url)
            names.append(name)
            featureds.append(featured)
            updates.append(update)
        elif infoType[0][1] == 'rating':
            rating = solomid_getRating(g)
            ratings.append(rating)
        elif infoType[0][1] == 'author':
            author = solomid_getAuthor(g)
            authors.append(author)
        else:
            pass # something terrible has happened!!
    
    namesRatingsUpdates = zip(names, ratings, updates, authors, featureds)
    return dict(zip(urls, namesRatingsUpdates))

# slooow
def solomid_filterTop(guides):
    topGuides = {}
    featuredGuides = {}
    maxTop = 2

    if len(guides) <= maxTop:
        return guides

    for g in guides:
        [name, rating, update, author, featured] = guides[g]
        if featured:
            featuredGuides[g] = guides[g]

    guidesIncluded = 0
    while guidesIncluded < maxTop and len(guides) >= maxTop:
        highestRating = -1
        topGuide = None

        for g in guides:
            [name, rating, update, author, featured] = guides[g]
            if rating > highestRating and not topGuides.has_key(g) \
               and not featuredGuides.has_key(g):
                highestRating = rating
                topGuide = g

        if topGuide != None:
            topGuides[topGuide] = guides[topGuide]
        guidesIncluded = guidesIncluded + 1

    return dict(topGuides.items() + featuredGuides.items())

def solomid_filterNewest(guides):
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

def solomid_getUrlNameUpdate(guide):
    urlAndName = guide.find("a")
    url = 'http://solomid.net/{0}'.format(getattr(urlAndName, 'attrs', None)[0][1])
    name = getattr(urlAndName, 'attrs', None)[1][1]
    update = int(getattr(guide, 'text', None).split(' ')[-3])
    featured = (guide.span.text == 'FEATURED')

    return (url, name, update, featured)

def solomid_getAuthor(guide):
    authorA = guide.find("a")
    author = authorA.text
    return author

def solomid_getRating(guide):
    rating = guide.findAll("span", attrs={"class":["green", "red"]})
    likes = int(rating[0].text)
    dislikes = int(rating[1].text)

    return (likes-dislikes)

class SourceScraper(threading.Thread):
    def __init__(self, champs, source):
        threading.Thread.__init__(self, name='Lolguides.net source scraper')
        self._finished = threading.Event()
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        self._champs = champs
        self._source = source

        if source == 0:
            self._outjson = 'solomid_data.json'
        elif source == 1:
            self._outjson = 'clg_data.json'

    def shutdown(self, timeout=None):
        self._finished.set()

    def run(self):
        self.getGuideData()

    def getGuideData(self):
        guideMap = {}

        for c in self._champs:
            if self._source == 0:
                solomidUrl = 'http://solomid.net/guides.php?champ={0}'.format(c)
                solomidGuides = solomid_getGuides(solomidUrl)
                solomidTopGuides = solomid_filterTop(solomidGuides)
                #print solomidTopGuides

                #print('----------------------')
                solomidNewGuide = solomid_filterNewest(solomidGuides)
            elif self._source == 1:
                clgUrl = 'http://www.clgaming.net/guides/?championID={0}'.format(champs[c])
                clgGuides = clg_getGuides(clgUrl)
                clgTopGuides = solomid_filterTop(clgGuides)
                clgNewGuide = solomid_filterNewest(clgGuides)

    def dumpJSON(dataz):
        fp = open(self._outjson, 'w')
        json_out = json.dumps(dataz, indent=2)
        fp.write(json_out)
        fp.close()

        

def getGuidesForAllChamps(champs):
    #tsmscraper = SourceScraper(champs, 0)
    #clgscraper = SourceScraper(champs, 1)

    # 1. get guides from solomid
    # 2. get guides from clgaming

    guideMap = {} # ChampName : [{url:[name, rating, updated, author], url2:[n, r, u, a]}, {url:[n, r, u, a]}] first dict in list is top, second contains newest

    for c in champs:
        print("Getting guide data for: {0}".format(c))
        cClean = cleanName(c)

        #print('----------------------')
        solomidUrl = 'http://solomid.net/guides.php?champ={0}'.format(c)
        solomidGuides = solomid_getGuides(solomidUrl)
        #print(solomidGuides)

        #print('----------------------')
        solomidTopGuides = solomid_filterTop(solomidGuides)
        #print solomidTopGuides

        #print('----------------------')
        solomidNewGuide = solomid_filterNewest(solomidGuides)


        clgUrl = 'http://www.clgaming.net/guides/?championID={0}'.format(champs[c])
        clgGuides = clg_getGuides(clgUrl)

        clgTopGuides = solomid_filterTop(clgGuides)
        #print(clgTopGuides)

        #print('----------------------')
        clgNewGuide = solomid_filterNewest(clgGuides)
        #print(clgNewGuide)

        guideMap[c] = [dict(solomidTopGuides.items() + clgTopGuides.items()), dict(solomidNewGuide.items() + clgNewGuide.items())]
        time.sleep(0.01) # no need to DoS their servers ffs.

    return guideMap

# SO SLOW LOLZ - Y U CREATE AND COMPILE DA SAME REGEXP ALL TIEM?
def clg_getUpdateDays(exp, update):
    update = update.replace(',', '')

    m = exp.match(update)
    #print(reg)
    #print("in: " + update)

    days = 0

    if m != None:
        mg = m.groups()

        if mg[1].startswith('day'):
            days = int(mg[0])
        elif mg[1].startswith('week'):
            days = int(mg[0])*7
        elif mg[1].startswith('month'):
            days = int(mg[0])*30
        elif mg[1].startswith('year'):
            days = int(mg[0])*365
    else:
        pass # something awful in da dataz

    #print("days: " + str(days))
    return days

def clg_getGuides(url):
    retry = True
    page = None

    #while retry:
    #    try:
    #        page = urllib2.urlopen(url)
    #        retry = False
    #    except httplib.HTTPError, e:
    #        print("Exception: {0}".format(e))
    #        print("Line: {0}".format(e.line))
    #        print("Waiting 10 seconds, then retrying")
    #        time.sleep(10) # wait 10 seconds then try again

    #page = urllib2.urlopen(url)
    try:
        page = urllib2.urlopen(url)
    except urllib2.HTTPError, e:
        print e.code
    except urllib2.URLError, e:
        print e.args
    
    soup = BeautifulSoup(page)
    tableData = soup("td")

    periods = '(years|year|months|month|weeks|week|days|day|hours|hour|minutes|minute|seconds|second)'

    reg = '^updated (\\d+) ' + periods + ' (\\d+) ' + periods + ' ago'
    exp = re.compile(reg)

    urls = []
    names = []
    ratings = []
    updates = []
    authors = []
    featureds = []

    i = 0
    # print(tableData[1:-12])
    while i < len(tableData[1:-12])-1:
        td = tableData[1:-12][i]
        td2 = tableData[1:-12][i+1]

        urlEnd = getattr(td.a, 'attrs', None)[1][1]
        url = 'http://clgaming.net{0}'.format(urlEnd)
        urls.append(url)

        name = td.a.text
        names.append(name)

        rating = td.span.text
        if rating.lower() == 'featured':
            featureds.append(True)
            rating = td.findAll("span")[1].text
        else:
            featureds.append(False)

        rating = int(rating)

        ratings.append(rating)

        author = td.findAll("a")[1].text
        authors.append(author)

        update = td2.findAll("div")[1].text
        updateDays = clg_getUpdateDays(exp, update)
        updates.append(updateDays)

        i = i + 3; # voodoo

    guideInfo = zip(names, ratings, updates, authors, featureds)
    return dict(zip(urls, guideInfo))

if __name__ == '__main__':
    # 1. Create champ:id map from leagueoflegends.com/champions
    #page = urllib2.urlopen(champion_url)
    #soup = BeautifulSoup(page)
    #champData = soup.findAll(name=["div", "a"],
    #                  attrs={"class" : ["lol_champion", "champion_name"]})
    #champions = makeChampMap(champData)

    dataz = getGuidesForAllChamps(clgChamps)
    dumpJSON(dataz) 

