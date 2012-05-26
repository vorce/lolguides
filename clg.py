rom BeautifulSoup import BeautifulSoup
import urllib2
import httplib
import time
import re

from scrapeutils import *

def getUrlNameFeatured(g):
    urlAndTitle = g.find(name="div", attrs={"class":["clg-guideTitle"]})

    urlEnd = getattr(urlAndTitle.a, 'attrs', None)[0][1]
    url = 'http://clgaming.net{0}'.format(urlEnd)

    title = urlAndTitle.a.text
    f = False
    if urlAndTitle.span != None:
        f = True

    return (url, title, f)

def getAuthorRating(g):
    everything = g.find(name="div", attrs={"class":["clg-guideMeta"]})

    author = everything.a.text
    rating = int(g.findAll("div")[1].text.split(" ")[0])

    return (author, rating)

def getUpdate(g, exp):
    upd = g.find(name="div", attrs={"class":["clg-guideDate"]}).text
    upd = upd.replace(',', '')

    m = exp.match(upd)

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

    return days

def getGuides(url):
    page = None
    page, skip = getPage(url)

    if skip:
        return {}

    soup = BeautifulSoup(page)
    guideList = soup.findAll(name="li", attrs={"class":["clg-guideItem"]})

    periods = '(years|year|months|month|weeks|week|days|day|hours|hour|minutes|minute|seconds|second)'

    reg = '^(\\d+) ' + periods + ' ago'
    exp = re.compile(reg)

    urls = []
    names = []
    ratings = []
    updates = []
    authors = []
    featureds = []

    for g in guideList:
        (url, name, featured) = getUrlNameFeatured(g)
        (author, rating) = getAuthorRating(g)
        update = getUpdate(g, exp)

        urls.append(url)
        names.append(name)
        featureds.append(featured)
        updates.append(update)
        authors.append(author)
        ratings.append(rating)

    guideInfo = zip(names, ratings, updates, authors, featureds)
    return dict(zip(urls, guideInfo))

