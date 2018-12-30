import sys
sys.path.insert(0, 'classes/')
from members import *

def computeStable(g):
    q = []
    for r in g.residents:
        q.append(r)

    while(len(q) > 0):
        curRes = q.pop(0)
        hospToPropose = curRes.pref[curRes.prefPtr]
        curRes.prefPtr += 1
        if(len(hospToPropose.matched) < hospToPropose.hq):
            curRes.matched = hospToPropose
            hospToPropose.matched.append(curRes)
            if(hospToPropose.worstRankRes == None):
                hospToPropose.worstRankRes = curRes
            elif(hospToPropose.getRank(curRes.name) > hospToPropose.getRank(hospToPropose.worstRankRes.name)):
                hospToPropose.worstRankRes = curRes
        else:
            worstRankRes = hospToPropose.worstRankRes
            if(hospToPropose.getRank(curRes.name) > hospToPropose.getRank(worstRankRes.name)):
                if(curRes.prefPtr != len(curRes.pref)):
                    q.append(curRes)
            else:
                hospToPropose.matched.remove(worstRankRes)
                worstRankRes.matched = None
                if(worstRankRes.prefPtr != len(worstRankRes.pref)):
                    q.append(worstRankRes)
                curRes.matched = hospToPropose
                hospToPropose.matched.append(curRes)
                hospToPropose.computeWorstRankRes()

def getStableMatching(g):
    computeStable(g)
    m = []
    for r in g.residents:
        r_ind = r.name[1:]
        h = r.matched
        if(h != None):
            h_ind = h.name[1:]
            m.append(Edge(r_ind, h_ind))
    
    return m

def checkEnvyFreeFeasibility(g):
    flag = 0
    for h in g.hospitals:
        if(h.hq > len(h.matched)):
            flag = 1
            break
    
    if(flag == 0):
        return True
    return False

def resetMatching(g):
    for r in g.residents:
        r.prefPtr = 0
        r.matched = None

    for h in g.hospitals:
        h.matched = []
        h.worstRankRes = None

def printMatching(m):
    for edge in m:
        e_split = edge.name.split('_')
        rname = 'r' + e_split[1]
        hname = 'h' + e_split[2]
        print(rname + ',' + hname)

def verifyEnvyFree(g, g_y):
    for res in g.residents:
        hosp = None
        r_y = g_y.getResident(res.name)
        if(r_y != None and r_y.matched != None):
            hosp = g.getHospital(r_y.matched.name)

        for h in res.pref:
            if(h == hosp):
                break
            h_y = g_y.getHospital(h.name)
            if(h_y != None):
                for res_matched_y in h_y.matched:
                    res_matched = g.getResident(res_matched_y.name)
                    if(h.getRank(res_matched.name) > h.getRank(res.name)):
                        return False

    return True