import json
import urllib2
import datetime
from BeautifulSoup import BeautifulSoup

from scrapeutils import *

# map for championselect.net, sigh :-)
csMap = {
    'ahri':2,
    'akali':5,
    'alistar':6,
    'amumu':7,
    'anivia':8,
    'annie':9,
    'ashe':10,
    'blitzcrank':11,
    'brand':12,
    'caitlyn':13,
    'cassiopeia':14,
    'chogath':15,
    'corki':16,
    'drmundo':17,
    'evelynn':18,
    'ezreal':19,
    'fiddlesticks':20,
    'fiora':97,
    'fizz':21,
    'galio':22,
    'gangplank':23,
    'garen':24,
    'gragas':25,
    'graves':26,
    'heimerdinger':27,
    'hecarim':99,
    'irelia':28,
    'janna':29,
    'jarvaniv':30,
    'jax':31,
    'karma':32,
    'karthus':33,
    'kassadin':34,
    'katarina':35,
    'kayle':36,
    'kennen':37,
    'kogmaw':38,
    'leblanc':39,
    'leesin':40,
    'leona':41,
    'lulu':98,
    'lux':42,
    'malphite':43,
    'malzahar':44,
    'maokai':45,
    'masteryi':46,
    'missfortune':47,
    'mordekaiser':48,
    'morgana':49,
    'nasus':50,
    'nautilus':96,
    'nidalee':51,
    'nocturne':52,
    'nunu':53,
    'olaf':54,
    'orianna':55,
    'pantheon':56,
    'poppy':57,
    'rammus':58,
    'renekton':59,
    'riven':60,
    'rumble':61,
    'ryze':62,
    'sejuani':63,
    'shaco':64,
    'shen':65,
    'shyvana':66,
    'singed':67,
    'sion':68,
    'sivir':69,
    'skarner':70,
    'sona':71,
    'soraka':72,
    'swain':73,
    'talon':74,
    'taric':75,
    'teemo':76,
    'tristana':77,
    'trundle':78,
    'tryndamere':79,
    'twistedfate':80,
    'twitch':81,
    'udyr':82,
    'urgot':83,
    'vayne':84,
    'veigar':85,
    'viktor':86,
    'vladimir':87,
    'volibear':88,
    'warwick':89,
    'wukong':90,
    'xerath':91,
    'xinzhao':92,
    'yorick':93,
    'ziggs':94,
    'zilean':95
}
csUrl = 'http://www.championselect.net/index.php?r=champions/view&id={0}'

htmlHeader = '<!doctype html>\n \
<html lang="en">\n \
<head>\n\n \
<link href=\'http://fonts.googleapis.com/css?family=Unna|Ovo|Adamina|Days+One\' rel=\'stylesheet\' type=\'text/css\'> \
\n\n \
<meta http-equiv="content-type" content="text/html; charset=UTF-8">\n \
<meta name="description" content="Champion guides for League of Legends. The top rated champion guides from the pro sites!"/>\n'

htmlStyle = '<style type="text/css">\n \
@import "../css/lg.css";\n \
</style>\n'

#htmlMeta = <meta name="description" content="Champion guides for League of Legends"/>
#<meta name="keywords" content="League of Legends, LoL, Guides, Champion guides, Builds, Items, Skills, Clgaming, Solomid, TSM, CLG, Riot"/>

def loadJSONs():
    lolproDump = loadJSON('lolpro_data.json')
    clgDump = loadJSON('clg_data.json')
    tsmDump = loadJSON('solomid_data.json')

    return concatJSONDumps(lolproDump, tsmDump, clgDump) 

def concatJSONDumps(lp, tsm, clg):
    cd = {}
    for c in lp:
        lp_c = lp.get(c, [{}, {}])
        tsm_c = tsm.get(c, [{}, {}])
        clg_c = clg.get(c, [{}, {}])

        cd[c] = [dict(lp_c[0].items() + clg_c[0].items() +
                      tsm_c[0].items()),
                 dict(lp_c[1].items() + clg_c[1].items() +
                      tsm_c[1].items())]
    return cd


def loadJSON(filename):
    fp = open(filename, 'r')
    pr = fp.read()
    jsonDump = json.loads(pr)
    fp.close()
    return jsonDump

# TODO:
# Check for champ icon. If it doesn't exist use unknown.png.
def genChampPage(cName, data, notice=""):
    c = cleanName(cName)

    print('Creating html/champions/{0}.html'.format(c))

    fp = open('html/champions/{0}.html'.format(c), 'w')

    fp.write(htmlHeader)

    # dont cache champ pages
    fp.write('<META HTTP-EQUIV="Cache-Control" CONTENT="max-age=0">\n')
    fp.write('<META HTTP-EQUIV="Cache-Control" CONTENT="no-cache">\n')
    fp.write('<META http-equiv="expires" content="0">\n')
    fp.write('<META HTTP-EQUIV="Expires" CONTENT="Tue, 01 Jan 1980 1:00:00 GMT">\n')
    fp.write('<META HTTP-EQUIV="Pragma" CONTENT="no-cache">\n')

    metaKeywords = cName + ', League of Legends, Guide, LoL, Champion guide, Build, Online gaming, DOTA, MOBA, lolguides, lol guide' 
    fp.write('<meta name="keywords" content="{0}"/>'.format(metaKeywords))
    
    fp.write('<link rel="shortcut icon" href="../gfx/favicon.ico" type="image/x-icon" />')
    fp.write('<title>{0} @ Lolguides</title>\n'.format(cName))

    fp.write('<meta name="author" content="lolguides.net">\n')

    fp.write('<!-- google page on g+ -->\n')
    fp.write('<script type="text/javascript">\n \
  var _gaq = _gaq || []; \
  _gaq.push([\'_setAccount\', \'UA-27511188-1\']);\
  _gaq.push([\'_trackPageview\']);\
  (function() {\
    var ga = document.createElement(\'script\'); ga.type = \'text/javascript\';ga.async = true;\
    ga.src = (\'https:\' == document.location.protocol ? \'https://ssl\' : \'http://www\') + \'.google-analytics.com/ga.js\';\
    var s = document.getElementsByTagName(\'script\')[0]; s.parentNode.insertBefore(ga, s);\
  })();\
\n</script>\n')

    fp.write('<!-- bootstrap -->\n')
    fp.write('<link href="../bootstrap/css/bootstrap.css" rel="stylesheet">\n')
    fp.write('<style>\n')
    fp.write('body {\n')
    fp.write('padding-top: 60px;\n')
    fp.write('}\n</style>\n')
    fp.write('<link href="../bootstrap/css/bootstrap-responsive.css" rel="stylesheet">\n')

    fp.write('<style type="text/css">\n \
             @import "../css/lg2.css";\n \
             </style>\n')

    fp.write('</head>\n<body>\n')

    fp.write('<!-- top navigation bar -->\n')
    fp.write('<div class="navbar navbar-fixed-top">\n')
    fp.write('  <div class="navbar-inner">\n')
    fp.write('    <div class="container">\n')
    fp.write('      <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">\n')
    fp.write('        <span class="icon-bar"></span>\n')
    fp.write('        <span class="icon-bar"></span>\n')
    fp.write('        <span class="icon-bar"></span>\n')
    fp.write('      </a>\n')
    fp.write('      <a class="brand" href="http://lolguides.net">LOLGUIDES.NET</a>\n')
    fp.write('      <div class="nav-collapse">\n')
    fp.write('        <ul class="nav">\n')
    fp.write('          <li><a href="../index.html">Guides</a></li>\n')
    fp.write('          <li><a href="../faq.html">FAQ</a></li>\n')
    fp.write('          <li><a href="../about.html">About</a></li>\n')
    fp.write('        </ul>\n')
    fp.write('      </div><!--/.nav-collapse -->\n')
    fp.write('    </div>\n')
    fp.write('  </div>\n')
    fp.write('</div>\n')

    fp.write('<div class="container">\n')
    fp.write('  <div class="row">\n')
    fp.write('      <div class="span9">\n')

    if notice != "":
        notice = "{0}: {1}".format(datetime.date.today().isoformat(), notice) 
        fp.write('<div class="alert alert-info">\n')
        fp.write('{0}\n'.format(notice))
        fp.write('</div>\n')

    fp.write('<h1><img alt="{0}" class="champ" src="../gfx/{1}.png" /> {0}</h1>\n'.format(cName, c))
   
    fp.write('<br />\n')

    csChampUrl = csUrl.format(csMap[c])

    fp.write('<a href="{0}">Champion details @ ChampionSelect</a>\n'.format(csChampUrl))
    #fp.write('<a href="http://soloqueue.com/#{0}">Champion details @ soloqueue.com</a>\n'.format(cName))
    fp.write('<br />\n\n')

    fp.write('<div class="hero-unit">\n')
    fp.write('                <div class="row">\n')
    fp.write('                <div class="span4">\n')

    fp.write('<h2 class="h2-guide">Top guides</h2>\n')

    # top guides by rating. highest first.
    sortedByRating = sorted(data[0].items(), key=lambda g: g[1][1], reverse=True)

    guideIndex = 0
    for g in sortedByRating:
        if guideIndex % 2 == 0:
            fp.write(getGuideHtml(g))
        guideIndex += 1

    fp.write('</div> <!-- col1 -->\n')
    fp.write('<div class="span4"> <!-- col 2 -->\n')
    fp.write('<h2>&nbsp;</h2>\n')

    guideIndex = 0
    for g in sortedByRating:
        if guideIndex % 2 == 1:
            fp.write(getGuideHtml(g))
        guideIndex += 1

    fp.write('</div> <!-- span4 -->\n</div> <!-- row -->\n\n')

    fp.write('<hr />\n\n<div class="row">\n')
    fp.write('<div class="span4">\n')
    fp.write('<h2 class="h2-guide">Latest guides</h2>\n')

    # latest guides by update (days). lowest first.
    sortedByUpdate = sorted(data[1].items(), key=lambda g: g[1][2])

    guideIndex = 0
    for g in sortedByUpdate:
        if guideIndex % 2 == 0:
            fp.write(getGuideHtml(g))
        guideIndex += 1

    fp.write('</div> <!-- col1 -->\n')
    fp.write('<div class="span4"> <!-- col 2 -->\n')
    fp.write('<h2>&nbsp;</h2>\n')

    guideIndex = 0
    for g in sortedByUpdate:
        if guideIndex % 2 == 1:
            fp.write(getGuideHtml(g))
        guideIndex += 1

    fp.write('</div> <!-- span4 -->\n</div> <!-- row -->\n')
    fp.write('</div> <!-- hero -->\n\n')

    fp.write('</div>\n<div class="span3">\n')

    fp.write('<h1> </h1><br /><br /><p>&nbsp;</p>\n')

    fp.write('          <script type="text/javascript"><!--\n')
    fp.write('google_ad_client = "ca-pub-0220560223746642";\n')
    fp.write('/* Lolguides.net ad */\n')
    fp.write('google_ad_slot = "7978945808";\n')
    fp.write('google_ad_width = 120;\n')
    fp.write('google_ad_height = 240;\n')
    fp.write('//-->\n')
    fp.write('</script>\n')
    fp.write('<script type="text/javascript"\n')
    fp.write('src="http://pagead2.googlesyndication.com/pagead/show_ads.js">\n')
    fp.write('</script>\n')
    fp.write('      </div>\n')
    fp.write('  </div>\n')
    fp.write('</div>\n')

    fp.write('<script src="../bootstrap/js/bootstrap.js"></script>\n\n')

    fp.write('</body>\n</html>\n')
    fp.close()

def getGuideHtml(guideData):
    (url, [name, rating, update, author, featured]) = guideData

    if update == -1:
        update = '?'

    site = url.split('/')[2]
    sicon = None # source icon
    ficon = None # featured icon
    siteurl = 'http://{0}'.format(site)

    if site.find('solomid') != -1:
        sicon = '../gfx/icons/tsmlogo.png'
    elif site.find('clgaming') != -1:
        sicon = '../gfx/icons/clglogo.png'
    elif site.find('lolpro') != -1:
        sicon = '../gfx/icons/curselogo.png'

    if featured:
        ficon = '../gfx/icons/featured.png'
    else:
        ficon = '../gfx/icons/notfeatured.png'

    guideHtml = '<div class="well">\n<table class="table table-condensed table-guide">\n'
    guideHtml += '<tr>\n<td class="guide-title"><a href="{0}">{1}</a></td>\n'
    guideHtml += '<td class="guide-data"><span class="norm">Rating</span><br />\n'
    guideHtml += '<span class="big">{2}</span></td><td class="guide-icon"><img class="icon" src="{3}" alt=""/></td>\n'
    guideHtml += '</tr>\n<tr>\n'
    guideHtml += '<td class="guide-author">By: {4}</td>\n'
    guideHtml += '<td class="guide-data"><span class="norm">Updated</span><br />\n'
    guideHtml += '<span class="big">{5}</span><br />\n'
    guideHtml += '<span class="norm">days ago</span></td>\n'
    guideHtml += '<td class="guide-icon"><a href="{6}"><img class="icon" src="{7}" alt="{8}" /></a></td>\n'
    guideHtml += '</tr>\n</table>\n</div> <!-- well -->\n\n'
    guideHtml = guideHtml.format(url, name.encode('utf-8'), rating, ficon, author.encode('utf-8'), update, siteurl, sicon, site)
    return guideHtml


def genAllChampPages(data, notice=""):
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
            pass #something's terribly wrong

    return dict(zip(champNames, champIds))

def getChampId(info):
    while getattr(info, 'name', None) != 'img':
        info = info.next

    champId = getattr(info, 'attrs', None)[0][1].split('/')[-1].split('.jpg')[0]
    return champId

def getChampName(info):
    champName = info.text
    return champName

def genIndex(notice=""):
    print("Generating index")
    print("With notice: {0}".format(notice))

    page = urllib2.urlopen('http://na.leagueoflegends.com/champions')
    soup = BeautifulSoup(page)
    champData = soup.findAll(name=["div", "a"],
                      attrs={"class" : ["lol_champion", "champion_name"]})
    champions = makeChampMap(champData)

    fp = open('html/index.html', 'w')

    fp.write(htmlHeader)

    fp.write('<meta name="keywords" content="Lolguides.net, Lolguides, League of Legends, LoL, \
Guides, Champion guides, Builds, Items, Skills, Clgaming, Solomid, TSM, \
CLG, Riot, Online gaming, DOTA, MOBA"/>')

    fp.write('<link rel="shortcut icon" href="gfx/favicon.ico" type="image/x-icon" />')
    fp.write('<title>Lolguides - League of Legends guides</title>\n')

    fp.write('<meta name="author" content="lolguides.net">\n')
  
    fp.write('<!-- flattr -->\n')
    fp.write('<script type="text/javascript">\n')
    fp.write('/* <![CDATA[ */\n')
    fp.write('(function() {\n')
    fp.write('var s = document.createElement(\'script\'), t = document.getElementsByTagName(\'script\')[0];\n')
    fp.write('s.type = \'text/javascript\';\n')
    fp.write('s.async = true;\n')
    fp.write('s.src = \'http://api.flattr.com/js/0.6/load.js?mode=auto\';\n')
    fp.write('t.parentNode.insertBefore(s, t);\n')
    fp.write('})();\n')
    fp.write('/* ]]> */</script>\n\n')

    fp.write('<!-- google analytics -->\n')
    fp.write('<script type="text/javascript">\n \
  var _gaq = _gaq || []; \
  _gaq.push([\'_setAccount\', \'UA-27511188-1\']);\
  _gaq.push([\'_trackPageview\']);\
  (function() {\
    var ga = document.createElement(\'script\'); ga.type = \'text/javascript\';ga.async = true;\
    ga.src = (\'https:\' == document.location.protocol ? \'https://ssl\' : \'http://www\') + \'.google-analytics.com/ga.js\';\
    var s = document.getElementsByTagName(\'script\')[0]; s.parentNode.insertBefore(ga, s);\
  })();\
\n</script>\n')

    fp.write('<!-- google page on g+ -->\n')
    fp.write('<link href="https://plus.google.com/111118564432197584206" rel="publisher" />')
    fp.write('<script type="text/javascript">\n \
(function()\n\
{var po = document.createElement("script");\n\
po.type = "text/javascript"; po.async = true;po.src = "https://apis.google.com/js/plusone.js";\n\
var s = document.getElementsByTagName("script")[0];\n\
s.parentNode.insertBefore(po, s);\n\
})();</script>\n')

    fp.write('<!-- bootstrap -->\n')
    fp.write('<link href="bootstrap/css/bootstrap.css" rel="stylesheet">\n')
    fp.write('<style>\n')
    fp.write('body {\n')
    fp.write('padding-top: 60px;\n')
    fp.write('}\n</style>\n')
    fp.write('<link href="bootstrap/css/bootstrap-responsive.css" rel="stylesheet">\n')

    fp.write('<style type="text/css">\n \
             @import "css/lg2.css";\n \
             </style>\n')
    
    fp.write('</head>\n<body>\n')

    fp.write('<!-- navigation top bar -->\n')
    fp.write('<div class="navbar navbar-fixed-top">\n')
    fp.write('<div class="navbar-inner">\n')
    fp.write('<div class="container">\n')
    fp.write('<a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">\n')
    fp.write('<span class="icon-bar"></span>\n')
    fp.write('<span class="icon-bar"></span>\n')
    fp.write('<span class="icon-bar"></span>\n')
    fp.write('</a>\n')
    fp.write('<a class="brand" href="http://lolguides.net">LOLGUIDES.NET</a>\n')
    fp.write('<div class="nav-collapse">\n')
    fp.write('<ul class="nav">\n')
    fp.write('<li class="active"><a href="index.html">Guides</a></li>\n')
    fp.write('<li><a href="faq.html">FAQ</a></li>\n')
    fp.write('<li><a href="about.html">About</a></li>\n')
    fp.write('</ul>\n')
    fp.write('</div><!--/.nav-collapse -->\n')
    fp.write('</div>\n')
    fp.write('</div>\n')
    fp.write('</div>\n')


    fp.write('<div class="container">\n')
    fp.write('  <div class="row">\n')
    fp.write('    <div class="span9">\n')

    if notice != "":
        fp.write('<div class="alert alert-info">\n')
        notice = "{0}: {1}".format(datetime.date.today().isoformat(), notice)
        fp.write('{0}\n'.format(notice))
        fp.write('</div>\n')
        
    fp.write('    	<h1>WELCOME</h1>\n')
    fp.write('        <div class="hero-unit">\n')
    
    fp.write('<p>LoLguides list only the top rated ')
    fp.write('and newest champion guides from clgaming, solomid and curse\'s lolpro. ')
    fp.write('Don\'t waste your time wading through pages of ')
    fp.write('out dated or low quality guides - let us filter ')
    fp.write('those out for you.</p>\n</div>\n\n')
    fp.write('        <h1>GUIDES</h1>\n')
    fp.write('        <div class="hero-unit">\n')
    
    fp.write('<table class="table table-striped" id="champs">\n')
    fp.write('         <thead>\n')
    fp.write('         <tr>\n')
    fp.write('             <th scope="col"></th>\n')
    fp.write('             <th scope="col"></th>\n')
    fp.write('             <th scope="col"></th>\n')
    fp.write('             <th scope="col"></th>\n')
    fp.write('             <th scope="col"></th>\n')
    fp.write('         </tr>\n')
    fp.write('     </thead>\n')
    fp.write('     <tbody>\n')

    cIndex = 0
    tableCols = 5 
    champions = sorted(champions)
    while cIndex < len(champions):
        c = champions[cIndex]
        # print('curl -O http://solomid.net/guide/champ/{0}.png;'.format(cleanName(c)))

        if cIndex % tableCols == 0:
            fp.write('<tr>\n')

        fp.write('<td><a href="{0}">{1}</a></td>'.format(champUrl(c), c))

        if cIndex % tableCols == (tableCols - 1):
            fp.write('</tr>\n')

        cIndex = cIndex + 1
   
    fp.write('</tbody>\n</table>\n</div>\n\n')

    fp.write('</div>\n<div class="span3">\n')

    fp.write('<!-- twitter feed -->\n')
    fp.write('<h1>&nbsp;</h1>\n')
    fp.write('<script charset="utf-8" src="http://widgets.twimg.com/j/2/widget.js"></script>\n')
    fp.write('<script>\n')
    fp.write('new TWTR.Widget({\n')
    fp.write('version: 2,\n')
    fp.write('type: \'profile\',\n')
    fp.write('rpp: 4,\n')
    fp.write('interval: 30000,\n')
    fp.write('width: 215,\n')
    fp.write('height: 350,\n')
    fp.write('theme: {\n')
    fp.write('shell: {\n')
    fp.write('background: \'#bcd1c6\',\n')
    fp.write('color: \'#24171c\'\n')
    fp.write('},\n')
    fp.write('tweets: {\n')
    fp.write('background: \'#ffffff\',\n')
    fp.write('color: \'#000000\',\n')
    fp.write('links: \'#21839c\'\n')
    fp.write('}\n')
    fp.write('},\n')
    fp.write('features: {\n')
    fp.write('scrollbar: true,\n')
    fp.write('loop: false,\n')
    fp.write('live: true,\n')
    fp.write('behavior: \'all\'\n')
    fp.write('}\n')
    fp.write('}).render().setUser(\'Lolguidesnet\').start();\n')
    fp.write('</script>\n\n')

    fp.write('<br />\n')

    fp.write('<!-- adsense -->\n')
    fp.write('<script type="text/javascript"><!--\n')
    fp.write('google_ad_client = "ca-pub-0220560223746642";\n')
    fp.write('/* Lolguides.net ad */\n')
    fp.write('google_ad_slot = "7978945808";\n')
    fp.write('google_ad_width = 120;\n')
    fp.write('google_ad_height = 240;\n')
    fp.write('//-->\n')
    fp.write('</script>\n')
    fp.write('<script type="text/javascript"\n')
    fp.write('src="http://pagead2.googlesyndication.com/pagead/show_ads.js">\n')
    fp.write('</script>\n<br />\n')

    # skip "news". fuck dat. go minimalz nigga
    '''fp.write('<h1>NEWS</h1>\n \
            <div id="news">\n')

    # insert news.txt
    nfp = open('news.txt', 'r')
    allNews = nfp.read()
    nfp.close()
    fp.write(allNews)
    '''

    fp.write('<!-- g+ page -->\n')
    fp.write('<g:plus href="https://plus.google.com/111118564432197584206" size="badge"></g:plus>\n<br />\n')

    fp.write('<!-- flattr button -->\n')
    fp.write('<a class="FlattrButton" style="display:none;" href="http://lolguides.net"></a>\n')
    fp.write('<noscript><a href="http://flattr.com/thing/506833/Lolguides-net" target="_blank">\n')
    fp.write('<img src="http://api.flattr.com/button/flattr-badge-large.png" alt="Flattr this" title="Flattr this" border="0"/></a></noscript>\n')

    fp.write('\n</div>\n</div>\n')

    fp.write('<hr />\n')

    fp.write('<footer>\n')
    fp.write('    <p>&copy; Lolguides.net 2011 - 2012</p>\n')
    fp.write('  </footer>\n')

    fp.write('</div> <!-- /container -->\n')


    fp.write('<!-- bootstrap -->\n')
    fp.write('<script src="bootstrap/js/bootstrap.js"></script>\n')

    fp.write('</body>\n</html>\n')

    fp.close()

def champUrl(c):
    url = c.replace(' ', '')
    url = url.replace("'", '')
    url = url.replace('.', '')
    url = url.lower()
    url = 'champions/{0}.html'.format(url)

    return url

if __name__ == '__main__':
    dataz = loadJSONs() # ('guide_data.json')
    genAllChampPages(dataz)
    genIndex()

