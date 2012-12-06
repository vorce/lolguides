import json


def loadJSONs():
    lolproDump = loadJSON('lolpro_data.json')
    clgDump = loadJSON('clg_data.json')
    tsmDump = loadJSON('solomid_data.json')
    lolkingDump = loadJSON('lolking_data.jon')

    return concatJSONDumps({'lolpro': lolproDump, 'tsm': tsmDump,
                            'lolking': lolkingDump, 'clg': clgDump}) 

def concatJSONDumps(dumps):
    cd = {}
    for c in dumps['lolpro']:  # use lolpro as champion reference
        lp_c = dumps['lolpro'].get(c, [{}, {}])
        tsm_c = dumps['tsm'].get(c, [{}, {}])
        clg_c = dumps['clg'].get(c, [{}, {}])
        king_c = dumps['lolking'].get(c, [{}, {}])

        cd[c] = [dict(lp_c[0].items() + clg_c[0].items() +
                      tsm_c[0].items() + king_c[0].items()),
                 dict(lp_c[1].items() + clg_c[1].items() +
                      tsm_c[1].items() + king_c[1].items())]
    return cd


def loadJSON(filename):
    fp = open(filename, 'r')
    pr = fp.read()
    jsonDump = json.loads(pr)
    fp.close()
    return jsonDump

