from BeautifulSoup import BeautifulSoup


def getGuides(page, skip, url, conf_f):
    if skip:
        return {}

    soup = BeautifulSoup(page)
    guideUl = soup.find(name="ul", attrs={"class": ["silverGuideList"]})
    guideListItems = guideUl.findAll("li")[1:]

    urls = []
    names = []
    ratings = []
    updates = []
    authors = []
    featureds = []  # It's a word.

    for g in guideListItems:
        guideSections = g.findAll(name="div", attrs={"class":
                                  ["title", "rating", "author", "image"]})

        correctChamp = True

        for s in guideSections:
            infoType = getattr(s, 'attrs', None)

            # Do not include guides of another champion...
            if infoType[0][1] == 'image':
                chmp = getGuideChamp(s)
                if not url.endswith(chmp):
                    correctChamp = False

        if correctChamp:
            for s in guideSections:
                infoType = getattr(s, 'attrs', None)
                if infoType[0][1] == 'title':
                    (url, name, update, featured) = getUrlNameUpdate(s)
                    urls.append(url)
                    names.append(name)
                    featureds.append(featured)
                    updates.append(update)
                elif infoType[0][1] == 'rating':
                    rating = getRating(s, conf_f)
                    ratings.append(rating)
                elif infoType[0][1] == 'author':
                    author = getAuthor(s)
                    authors.append(author)
                else:
                    pass  # something terrible has happened!!

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


def getRating(guide, conf_f):
    rating = guide.findAll("span", attrs={"class": ["green", "red"]})
    likes = int(rating[0].text)
    dislikes = int(rating[1].text)

    return conf_f(likes, dislikes)

