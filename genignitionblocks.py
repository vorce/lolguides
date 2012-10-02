import MySQLdb
import genpages
from genutils import *
from scrapeutils import *


def gen_champ_blocks(data, notice):
    # TODO, handle notice
    return (gen_champ_top_block(data), gen_champ_new_block(data))

def gen_champ_top_block(data):
    top_guides_html = ''
    top_guides = sorted(data[0].items(), key=lambda g: g[1][1], reverse=True)

    guide_index = 0
    for g in top_guides:
        if guide_index % 2 == 0:
            top_guides_html += genpages.getGuideHtml(g)
        guide_index += 1

    top_guides_html += '</div> <!-- col1 -->\n<div class="span4"> <!-- col 2 -->\n'
    top_guides_html += '<h2>&nbsp;</h2>\n'

    guide_index = 0
    for g in top_guides:
        if guide_index % 2 == 1:
            top_guides_html += genpages.getGuideHtml(g)
        guide_index += 1

    return top_guides_html

def gen_champ_new_block(data):
    new_guides_html = ''
    new_guides = sorted(data[1].items(), key=lambda g: g[1][2])

    guide_index = 0
    for g in new_guides:
        if guide_index % 2 == 0:
            new_guides_html += genpages.getGuideHtml(g)
        guide_index += 1

    new_guides_html += '</div> <!-- col1 -->\n<div class="span4"> <!-- col 2 -->\n'
    new_guides_html += '<h2>&nbsp;</h2>\n'

    guide_index = 0
    for g in new_guides:
        if guide_index % 2 == 1:
            new_guides_html += getGuideHtml(g)
        guide_index += 1

    return new_guides_html

def update_all_blocks(data, notice=""):
    table = 'rawtextblock'
    content_row = 'content'
    top_suffix = '_top'
    new_suffix = '_new'
    update_string = "UPDATE {0} SET {1}=%s WHERE name=%s".format(table,
                                                                 content_row)
    db = None 
    try:
        db = MySQLdb.connect(passwd="", db="")
        cursor = db.cursor()

        for d in data:
            (name, (top, new)) = (cleanName(d), gen_champ_blocks(data[d], notice))

            cursor.execute(update_string, (top, name + top_suffix,))
            cursor.execute(update_string, (new, name + new_suffix,))
    except MySQLdb.Error, e:
        print("Error {0}: {1}".format(e.args[0], e.args[1]))
    finally:
        if db:
            db.close()
