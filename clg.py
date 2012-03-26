from BeautifulSoup import BeautifulSoup
import urllib2
import httplib
import time

from scrapeutils import *

def getGuides(url):
    page = None
    page, skip = getPage(url)

    if skip:
        return {}

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
        updateDays = getUpdateDays(exp, update)
        updates.append(updateDays)

        i = i + 3; # voodoo

    guideInfo = zip(names, ratings, updates, authors, featureds)
    return dict(zip(urls, guideInfo))


# Fixme: Don't compile the same regex all the time heh.
def getUpdateDays(exp, update):
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
