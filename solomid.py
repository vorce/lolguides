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
    guideList = soup.findAll(name="li", attrs={"class":
                            ["grey-border p10 bg pos-rel"]})
    #name="div", attrs={"class":["title", "rating", "author"]})

    urls = []
    names = []
    ratings = []
    updates = []
    authors = []
    featureds = [] # It's a word.

    for g in guideList:
        '''infoType = getattr(g, 'attrs', None)
        
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
        '''
        url = getUrl(g)
        urls.append(url)

        name = getName(g)
        names.append(name)

        update = getUpdate(g)
        updates.append(update)

        f = getFeatured(g)
        featureds.append(f)

        r = getRating(g)
        ratings.append(r)

        author = getAuthor(g)
        authors.append(author)
    
    namesRatingsUpdates = zip(names, ratings, updates, authors, featureds)
    return dict(zip(urls, namesRatingsUpdates))


def getUrl(guide):
    return getattr(guide.a, 'attrs', None)[1][1]

def getName(guide):
    return guide.find(name="td", attrs={"class": ["guide-title bold tooltip"]}).text.encode('utf-8')

def getUpdate(guide):
    text = guide.find(name="td", attrs={"class": ["grey text-left last-updated"]}).text.split(' ')
    try:
        upd = int(text[3])
    except ValueError:
        upd = 0

    metric = text[4]

    if metric.startswith('week'):
        upd = upd * 7
    elif metric.startswith('month'):
        upd = upd * 30
    elif metric.startswith('year'):
        upd = upd * 365

    return upd 

def getFeatured(guide):
    p = guide.find(name="td", attrs={"class": ["blue"]}).text
    return (p == 'Pro Guide' or p == 'Featured Guide')

def getAuthor(guide):
    return guide.find(name="td", attrs={"class": ["bold text-center"]}).text.encode('utf-8')

def getRating(guide):
    s = guide.find(name="span")
    like = getattr(s, 'attrs', None)[0][1].split(':')[1][:-1]
    return int(float(like))
    #return confidence_fixed(likes, dislikes)

