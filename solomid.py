from BeautifulSoup import BeautifulSoup
import urllib2
import httplib
import time

from scrapeutils import *

def getGuides(url):
    retry = True
    page, skip = getPage(url)

    if skip:
        return {}

    soup = BeautifulSoup(page)
    guideList = soup.findAll(name="div", attrs={"class":["title", "rating",
                                                         "author", "image"]})
    urls = []
    names = []
    ratings = []
    updates = []
    authors = []
    featureds = [] # It's a word.

    for g in guideList:
        infoType = getattr(g, 'attrs', None)

        # Do not include guides of another champion...
        if infoType[0][0] == 'image':
            chmp = getGuideChamp(g)
            if not url.endswith(chmp):
                continue

        if infoType[0][1] == 'title':
            (url, name, update, featured) = getUrlNameUpdate(g)
            urls.append(url)
            names.append(name)
            featureds.append(featured)
            updates.append(update)
        elif infoType[0][1] == 'rating':
            rating = getRating(g)
            ratings.append(rating)
        elif infoType[0][1] == 'author':
            author = getAuthor(g)
            authors.append(author)
        else:
            pass # something terrible has happened!!
    
    namesRatingsUpdates = zip(names, ratings, updates, authors, featureds)
    return dict(zip(urls, namesRatingsUpdates))

def getGuideChamp(div):
    i = div.find("img")
    attr = getattr(i, 'attrs', None)
    return attr[1][1]

def getUrlNameUpdate(guide):
    urlAndName = guide.find("a")
    url = 'http://solomid.net/{0}'.format(getattr(urlAndName, 'attrs', None)[0][1])
    name = getattr(urlAndName, 'attrs', None)[1][1]
    update = int(getattr(guide, 'text', None).split(' ')[-3])
    featured = (guide.span.text == 'FEATURED')

    return (url, name, update, featured)

def getAuthor(guide):
    authorA = guide.find("a")
    author = authorA.text
    return author

def getRating(guide):
    rating = guide.findAll("span", attrs={"class":["green", "red"]})
    likes = int(rating[0].text)
    dislikes = int(rating[1].text)

    return confidence_fixed(likes, dislikes)

