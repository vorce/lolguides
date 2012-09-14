from BeautifulSoup import BeautifulSoup
import urllib2
import httplib
import time

from scrapeutils import *

base_url = 'http://www.lolpro.com/guides/' #veigar

def getGuideData(c):
    #print("Getting guide data for: {0}".format(c))
    cClean = cleanName(c)
    guide_url = base_url + '{0}'.format(cClean)
    
    guides = getGuides(guide_url)
    
    top = filterTop(guides)

    new = filterNewest(guides)

    return (top, new)

def getGuides(url):
    page, skip = getPage(url)

    lolpro_ul_class = 'b-list b-list-a p-carousel-wrapper champ-guide-list'
    guideItems = []

    if not skip:
        soup = BeautifulSoup(page)
        guideList = soup.findAll(name="ul", attrs={"class":lolpro_ul_class})
        if len(guideList) > 0:
            guideItems = guideList[0].findAll(name='li')

    urls = []
    names = []
    ratings = []
    updates = []
    authors = []
    featureds = [] # It's a word.

    for g in guideItems:
        url = getUrl(g)
        urls.append(url)

        name = getName(g)
        names.append(name)

        featureds.append(True) # All the guides are sort of featured I guess?

        updates.append(-1) # No dates .. use -1 as specialcase = unknown

        rating = int(g.findAll('span')[3].text.split(' ')[0])
        ratings.append(rating)

        author = g.findAll('span')[1].text.split('by ')[1]
        authors.append(author)

    namesRatingsUpdates = zip(names, ratings, updates, authors, featureds)
    return dict(zip(urls, namesRatingsUpdates))

def getUrl(guideItem):
    return getattr(guideItem.find('a'), 'attrs')[0][1]

def getName(guideItem):
    return guideItem.find('span').text
