import datetime
import scrapeutils
import sys
import genutils


csUrl = 'http://www.championselect.net/champ/{0}'


def genChampPage(cName, data, notice=""):
    scrape_util = scrapeutils.ScrapeUtils()
    c = scrape_util.cleanName(cName)

    filePath = 'wok_site/content/champions'

    print('Creating {0}/{1}.raw'.format(filePath, c))

    fp = open('{0}/{1}.raw'.format(filePath, c), 'w')

    fp.write('title: {0}\n'.format(cName))
    fp.write('url: /champions/{0}.html\n'.format(c))
    fp.write('icon: ../gfx/{0}.png\n'.format(c))

    csn = scrape_util.csName(cName)  # championselect.net name
    csChampUrl = csUrl.format(csn)
    fp.write('champion_select: <a href="{0}">Counter-pick details at ChampionSelect</a>\n'.format(csChampUrl))

    if notice != "":
        notice = "{0}: {1}".format(datetime.date.today().isoformat(), notice)
        fp.write('notice: |\n')
        fp.write(' <br /><div class="alert alert-info">\n')
        fp.write(' {0}\n'.format(notice))
        fp.write(' </div>\n')

    topGuidesHTML = ''

    # top guides, featured first
    sortedByFeatured = sorted(data[0].items(),
                              key=lambda g: g[1][4], reverse=True)

    guideIndex = 0
    for g in sortedByFeatured:
        if guideIndex % 2 == 0:
            topGuidesHTML += getGuideHtml(g)
        guideIndex += 1

    topGuidesHTML += ' </div> <!-- col1 -->\n'
    topGuidesHTML += ' <div class="span4"> <!-- col 2 -->\n'

    guideIndex = 0
    for g in sortedByFeatured:
        if guideIndex % 2 == 1:
            topGuidesHTML += getGuideHtml(g)
        guideIndex += 1

    fp.write('top_guides: |\n')
    fp.write(topGuidesHTML)

    latestGuidesHTML = ''

    # latest guides by update (days). lowest first.
    sortedByUpdate = sorted(data[1].items(), key=lambda g: g[1][2])

    guideIndex = 0
    for g in sortedByUpdate:
        if guideIndex % 2 == 0:
            latestGuidesHTML += getGuideHtml(g)
        guideIndex += 1

    latestGuidesHTML += ' </div> <!-- col1 -->\n'
    latestGuidesHTML += ' <div class="span4"> <!-- col 2 -->\n'

    guideIndex = 0
    for g in sortedByUpdate:
        if guideIndex % 2 == 1:
            latestGuidesHTML += getGuideHtml(g)
        guideIndex += 1

    fp.write('latest_guides: |\n')
    fp.write(latestGuidesHTML)

    fp.write('---\n')
    fp.close()


def getGuideHtml(guideData):
    (url, [name, rating, update, author, featured]) = guideData

    if update == -1:
        update = '?'

    if len(name) > 45:
        name = name[:45] + "..."

    site = url.split('/')[2]
    sicon = None  # source icon
    ficon = None  # featured icon
    siteurl = 'http://{0}'.format(site)

    if site.find('solomid') != -1:
        sicon = '../gfx/icons/tsmlogo.png'
    elif site.find('clgaming') != -1:
        sicon = '../gfx/icons/clglogo.png'
    elif site.find('lolpro') != -1:
        sicon = '../gfx/icons/curselogo.png'
    elif site.find('lolking') != -1:
        sicon = '../gfx/icons/kinglogo.png'

    if featured:
        ficon = '../gfx/icons/featured.png'
    else:
        ficon = '../gfx/icons/notfeatured.png'

    guideHtml = ' <div class="well well-small">\n'
    guideHtml += ' <div class="media">\n'
    guideHtml += ' <p class="pull-right">\n'
    guideHtml += ' <img class="icon" src="{3}" alt=""/><br />\n'
    guideHtml += ' <a href="{6}"><img class="icon" src="{7}" alt=""/></a></p>\n'
    guideHtml += ' <div class="media-body">\n'
    guideHtml += ' <h4 class="media-heading"><a href="{0}">{1}</a></h4>\n'
    guideHtml += ' <ul><li>By: <span class="label">{4}</span></li>\n'
    guideHtml += ' <li>Rating: <span class="label">{2}</span></li>\n'
    guideHtml += ' <li>Updated <strong>{5}</strong> days ago</li></ul>\n'
    guideHtml += ' </div> <!-- media-body -->\n'
    guideHtml += ' </div> <!-- media -->\n'
    guideHtml += ' </div> <!-- well -->\n'
    guideHtml = guideHtml.format(url.encode('utf-8'), name.encode('utf-8'), rating, ficon, author.encode('utf-8'), update, siteurl, sicon, site)
    return guideHtml


def genAllChampPages(data, notice=""):
    if notice != "":
        print("Creating champion pages with notice: {0}".format(notice))

    for c in data:
        genChampPage(c, data[c], notice)


def makeChampMap(champs):
    champIds = []
    champNames = []

    for c in champs:
        infoType = getattr(c, 'name', None)

        if infoType == 'a':
            champIds.append(getChampId(c))
        elif infoType == 'div':
            champName = getChampName(c)
            champNames.append(champName)
        else:
            pass  # something's terribly wrong

    return dict(zip(champNames, champIds))


def getChampId(info):
    while getattr(info, 'name', None) != 'img':
        info = info.next

    champId = getattr(info, 'attrs', None)[0][1].split('/')[-1].split('.jpg')[0]
    return champId


def getChampName(info):
    champName = info.text
    return champName


def genIndex(filename, notice=""):
    print("Generating index")
    
    if notice != "":
        print("With notice: {0}".format(notice))

    scrape_util = scrapeutils.ScrapeUtils()
    champions = scrape_util.getChampions()
    champions = filter(lambda c: c['id'] != 0, champions)  # remove 'N/A' entries

    fp = open(filename, 'w')

    names = ', '.join([c['name'] for c in champions])

    fp.write('title: Home\n')
    fp.write('url: /index.html\n')
    fp.write('type: home\n')
    fp.write('typeahead_champs: [{0}]\n'.format(names))
    if notice != "":
        fp.write('notice: |\n')
        fp.write(' <br /><div class="alert alert-info">\n')
        notice = "{0}: {1}".format(datetime.date.today().isoformat(), notice)
        fp.write(' {0}\n'.format(notice))
        fp.write(' </div>\n')

    fp.write('---\n')  # wok content file

    fp.write('<table class="table table-striped" id="champs">\n')
    fp.write('<tbody>\n')

    cIndex = 0
    tableCols = 5
    champions = sorted(champions, key=lambda c: c['name'])  # sort by name

    while cIndex < len(champions):
        if champions[cIndex].get('id', 0) != 0:
            c = champions[cIndex].get('name')
            # print('curl -O http://solomid.net/guide/champ/{0}.png;'.format(cleanName(c)))

            if cIndex % tableCols == 0:
                fp.write('<tr>\n')

            fp.write('<td><a href="{0}">{1}</a></td>'.format(champUrl(c), c))

            if cIndex % tableCols == (tableCols - 1):
                fp.write('</tr>\n')
        cIndex = cIndex + 1
   
    fp.write('</tbody>\n</table>\n\n')

    fp.close()


def champUrl(c):
    url = c.replace(' ', '')
    url = url.replace("'", '')
    url = url.replace('.', '')
    url = url.lower()
    url = 'champions/{0}.html'.format(url)

    return url

if __name__ == '__main__':
    dataz = genutils.loadJSONs()  # ('guide_data.json')

    if len(sys.argv) <= 1:
        genAllChampPages(dataz)
        genIndex('wok_site/content/home.raw')
    else:
        genAllChampPages(dataz, sys.argv[1])
        genIndex('wok_site/content/home.raw', sys.argv[1])

