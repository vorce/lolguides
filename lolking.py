import datetime
import scrapeutils
from BeautifulSoup import BeautifulSoup


lolking_url_base = 'http://www.lolking.net'


def getGuides(page, skip, champURL):
    lolking_div_style = 'border-bottom: 1px solid #111; display: table-cell; padding: 12px 8px 4px 4px; text-align: left; vertical-align: top;'
    guideItems = []

    if not skip:
        soup = BeautifulSoup(page)
        guideItems = soup.findAll(name="div", attrs={"class": "guide-row"})

    urls = []
    names = []
    ratings = []
    updates = []
    authors = []
    featureds = []

    sutil = scrapeutils.ScrapeUtils()
    for i in guideItems:
        champName = sutil.cleanName(i.div.text)

        if not champURL.endswith(champName):
            continue  # skip if not correct champ

        guideBasics = i.find(name="div", attrs={"style": lolking_div_style})

        url = getUrl(guideBasics)
        urls.append(url)

        name = getName(guideBasics)
        names.append(name)

        rating = getRating(i)
        ratings.append(rating)

        update = getUpdate(guideBasics)
        updates.append(update)

        author = getAuthor(guideBasics)
        authors.append(author)

        featured = getFeatured(guideBasics)
        featureds.append(featured)

    namesRatingsUpdates = zip(names, ratings, updates, authors, featureds)
    return dict(zip(urls, namesRatingsUpdates))


def getUrl(guideItem):
    return '{0}{1}'.format(lolking_url_base, guideItem.a.attrs[0][1])


def getName(guideItem):
    return guideItem.a.text


def getRating(guideItem):
    rating = 0

    rating_list = guideItem.find(name='ul', attrs={'class': 'crown_rating'})
    if not rating_list:
        return rating

    full = rating_list.findAll(name='li', attrs={'class': 'full'})
    half = rating_list.findAll(name='li', attrs={'class': 'half'})

    if full:
        rating += (len(full) * 2)
    if half:
        rating += len(half)

    return rating


def getFeatured(guideItem):
    featured = guideItem.find(name='span', attrs={'class': 'guide-flag guide-flag-gold'})
    return (featured is not None)


def getUpdate(guideItem):
    date_string = guideItem.find(name='span',
                                 attrs={'style': ' text-shadow: 0 0 1px #000;'}).text
    if not date_string:
        return -1

    dt = datetime.datetime.strptime(date_string, "%B %d, %Y")
    now = datetime.datetime.today()
    delta = now - dt
    return delta.days


def getAuthor(guideItem):
    return guideItem.findAll('a')[1].text
