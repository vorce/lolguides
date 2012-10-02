import json


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

