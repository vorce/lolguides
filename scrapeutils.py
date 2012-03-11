def cleanName(c):
    cleanName = c.lower()
    cleanName = cleanName.replace('.', '')
    cleanName = cleanName.replace("'", '')
    cleanName = cleanName.replace(' ', '')
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

