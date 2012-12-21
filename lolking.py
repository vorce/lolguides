import datetime
import scrapeutils
from BeautifulSoup import BeautifulSoup


lolking_url_base = 'http://www.lolking.net'


def getGuides(page, skip, champURL, rating_func=None):
    lolking_div_style = 'border-bottom: 1px solid #111; display: table-cell; padding: 12px 8px 4px 4px; text-align: left; vertical-align: top;'
    guideItems = []

    if not skip:
        soup = BeautifulSoup(page)
        guideItems = soup.findAll(name="div", attrs={"class": "guide-row"}) +
        featuredRows = soup.findAll(name="div", attrs={"class": "guide-row-featured guide-row-featured-top guide-row"})
        guideItems += featuredRows
    else:
        return {}

    urls = []
    names = []
    ratings = []
    updates = []
    authors = []
    featureds = []

    sutil = scrapeutils.ScrapeUtils()
    for i in guideItems:
        champName = i.findAll('div')[3].text
        champName = sutil.cleanName(champName)

        if not champURL.endswith(champName):
            continue  # skip if not correct champ

        guideBasics = i.find(name="div", attrs={"style": lolking_div_style})

        url = getUrl(guideBasics)
        urls.append(url)

        name = getName(guideBasics)
        names.append(name)

        rating = getRating(i, rating_func)
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


def getRating(guideItem, rating_func=None):
    rating = 0

    upvote_style = "font-size: 14px; color:#54c200; text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.6); line-height: 10px;"
    upvotes = int(guideItem.find(name="div", attrs={"style": upvote_style}).text)

    downvote_style = "font-size: 14px; color:#d90014; text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.6); line-height: 10px;"
    downvotes = int(guideItem.find(name="div", attrs={"style": downvote_style}).text)

    if rating_func is not None:
        return rating_func(upvotes, downvotes)

    return 0

    """
    rating_list = guideItem.find(name='ul', attrs={'class': 'crown_rating'})
    if not rating_list:
        return rating

    full = rating_list.findAll(name='li', attrs={'class': 'full'})
    half = rating_list.findAll(name='li', attrs={'class': 'half'})

    if full:
        rating += (len(full) * 2)
    if half:
        rating += len(half)
    """
    # return rating


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
