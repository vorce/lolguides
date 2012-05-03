import urllib2
import math

def csName(c):
    csn = c
    csn = csn.replace(' ', '-')
    csn = csn.replace("'", '')
    csn = csn.replace('.', '')
    return csn

def cleanName(c):
    cleanName = c.lower()
    cleanName = cleanName.replace('.', '')
    cleanName = cleanName.replace("'", '')
    cleanName = cleanName.replace(' ', '')
    cleanName = cleanName.lower()
    return cleanName

# slooow
def filterTop(guides):
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
        highestRating = -99999
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

def filterNewest(guides):
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

def getPage(url):
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
                time.sleep(10) # wait 10 seconds then try again
        except urllib2.URLError, e:
            print("Exception: {0}".format(e))
            print("Waiting 10 seconds, then retrying")
            time.sleep(10) # wait 10 seconds then try again

    return (page, skip)

# https://possiblywrong.wordpress.com/2011/06/05/reddits-comment-ranking-algorithm/
# Thanks!
def confidence_fixed(ups, downs):
    if ups == 0:
        return -downs
    n = ups + downs
    z = 1.64485 #1.0 = 85%, 1.6 = 95%
    phat = float(ups) / n
    return int(((phat+z*z/(2*n)-z*math.sqrt((phat*(1-phat)+z*z/(4*n))/n))/(1+z*z/n))*100)

