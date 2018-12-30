class Resident:
    def __init__(self, name):
        self.name = name
        self.pref = []
        self.matched = None
        self.prefPtr = 0
        self.lq = 0
        self.hq = 0
        self.classes = []

    def getIndex(self):
        return self.name[1:]

    def getPrefSize(self):
        return len(self.pref)

    def getRank(self, hosp_name):
        for i, h in enumerate(self.pref):
            if(h.name == hosp_name):
                return i+1

class Hospital:
    def __init__(self, name, lq, hq):
        self.name = name
        self.pref = []
        self.lq = lq
        self.hq = hq
        self.matched = []
        self.worstRankRes = None

    def getIndex(self):
        return self.name[1:]

    def getPrefSize(self):
        return len(self.pref)

    def getRank(self, res_name):
        for i, r in enumerate(self.pref):
            if(r.name == res_name):
                return i+1

    def computeWorstRankRes(self):
        worstRank = -1
        worstRankResident = None
        for r in self.matched:
            curRank = self.getRank(r.name)
            if(curRank > worstRank):
                worstRank = curRank
                worstRankResident = r
        self.worstRankRes = worstRankResident

class Edge:
    def __init__(self, r_ind, h_ind):
        self.name = 'x_' + r_ind + '_' + h_ind
        self.r_ind = r_ind
        self.h_ind = h_ind

class Classification:
    def __init__(self):
        self.class_list = []
        self.cap = 0

    def printClass(self):
        print '{(',
        for i, e in enumerate(self.class_list):
            if(i != len(self.class_list)-1):
                print e + ' ,',
            else:
                print e + ' ): ' + str(self.cap) +'}',