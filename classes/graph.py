from members import *

class Graph:
    def __init__(self):
        self.residents = [];
        self.hospitals = [];
        self.edges = [];

    def printResident(self, name):
        for r in self.residents:
            if(r.name == name):
                print('name: ' + r.name)
                print 'Preferences: ',
                for h in r.pref:
                    print h.name + ' ',
                print('')
                return

    def printHospital(self, name):
        for h in self.hospitals:
            if(h.name == name):
                print('name: ' + h.name)
                print('lq: {}'.format(h.lq))
                print('hq: {}'.format(h.hq))
                print 'Preferences: ',
                for r in h.pref:
                    print r.name + ' ',
                print('')
                return

    def getResident(self, name):
        for r in self.residents:
            if(r.name == name):
                return r
        return None

    def getHospital(self, name):
        for h in self.hospitals:
            if(h.name == name):
                return h
        return None

    def getTotalHospitals(self):
        return len(self.hospitals)

    def getTotalResidents(self):
        return len(self.residents)

def createGraph(path, hr=0):
    g = Graph()
    choice = 0
    f = open(path, "r")
    for line in f.readlines():
        line = line.strip()
        if(len(line) == 0 or line == '@End'):
            continue
        if(line == '@PartitionA'):
            choice = 1
            continue
        if(line == '@PartitionB'):
            choice = 2
            continue
        if(line == '@PreferenceListsA'):
            choice = 3
            continue
        if(line == '@PreferenceListsB'):
            choice = 4
            continue

        if(choice == 1):
            line_trim = line.replace(' ', '')[:-1]
            line_split = line_trim.split(',')
            for res in line_split:
                g.residents.append(Resident(res))

        if(choice == 2):
            if(hr != 2):
                line_trim = line.replace(' ', '')[:-2]
                line_split = line_trim.split('),')
                for hosp in line_split:
                    hosp_split = hosp.split('(')
                    h = hosp_split[0]
                    quotas = hosp_split[1].split(',')
                    if(hr==0):
                        lq = int(quotas[0])
                        hq = int(quotas[1])
                        g.hospitals.append(Hospital(h, lq, hq))
                    else:
                        lq = 0
                        hq = int(quotas[0])
                        g.hospitals.append(Hospital(h, lq, hq))
            else:
                line_trim = line.replace(' ', '')[:-1]
                line_split = line_trim.split(',')
                for hosp in line_split:
                    g.hospitals.append(Hospital(hosp, 0, 1))

        if(choice == 3):
            line_trim = line.replace(' ', '')[:-1]
            temp_split = line_trim.split(':')
            res = temp_split[0]
            r_ind = res[1:]
            pref_list = temp_split[1].split(',')
            r = g.getResident(res)
            for h in pref_list:
                h_ind = h[1:]
                r.pref.append(g.getHospital(h))
                g.edges.append(Edge(r_ind, h_ind))

        if(choice == 4):
            line_trim = line.replace(' ', '')[:-1]
            temp_split = line_trim.split(':')
            hosp = temp_split[0]
            pref_list = temp_split[1].split(',')
            h = g.getHospital(hosp)
            for r in pref_list:
                if(r != ''):
                    h.pref.append(g.getResident(r))

    f.close()
    return g