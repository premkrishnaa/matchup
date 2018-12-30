import sys
sys.path.insert(0, 'classes/')
from graph import *

def getYokoiInstance(g):
    g_y = Graph()
    r_y = set()
    h_y = set()
    for h in g.hospitals:
        if(h.lq > 0):
            h_y.add(h.name)
            g_y.hospitals.append(Hospital(h.name, 0, h.lq))
            for r in h.pref:
                r_y.add(r.name)
                g_y.edges.append(Edge(r.name[1:], h.name[1:]))

    for r_name in r_y:
        g_y.residents.append(Resident(r_name))

    for r in g.residents:
        if(r.name in r_y):
            res_y = g_y.getResident(r.name)
            for h in r.pref:
                if(h.name in h_y):
                    res_y.pref.append(g_y.getHospital(h.name))

    for h in g.hospitals:
        if(h.name in h_y):
            hosp_y = g_y.getHospital(h.name)
            for r in h.pref:
                if(r.name in r_y):
                    hosp_y.pref.append(g_y.getResident(r.name))

    return g_y