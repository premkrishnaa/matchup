from members import *
from random import randint
from random import sample
from random import seed
from datetime import datetime

seed(datetime.now())

class Graph:
    def __init__(self):
        self.residents = [];
        self.hospitals = [];
        self.edges = [];

    def initResidentCapacities(self):
        res = self.residents
        for r in res:
            n = len(r.pref)
            r.hq = randint(1, n)

    def initResidentClass(self, res):
        n = len(res.pref)
        rpref = []
        for h in res.pref:
            rpref.append(h.name)
        used_classes = []
        tot_classes = randint(0, n)
        ct = 0
        while(n > 1 and ct < tot_classes):
            cur_class_size = randint(2, n)
            cur_class = sample(rpref, cur_class_size)
            if(set(cur_class) not in used_classes):
                c = Classification()
                used_classes.append(set(cur_class))
                c.class_list = cur_class
                c.cap = randint(1, cur_class_size-1)
                res.classes.append(c)
                ct += 1;

    def initAllResidentClass(self):
        for res in self.residents:
            self.initResidentClass(res)

    def printFormat(self):
        print('@PartitionA')
        res = self.residents
        rlen = len(res)
        for i, r in enumerate(res):
            if(i != rlen-1):
                print r.name + ' (' + str(r.hq) + '),',
            else:
                print r.name + ' (' + str(r.hq) + ') ;'
        print('@End\n')

        print('@PartitionB')
        hosp = self.hospitals
        hlen = len(hosp)
        for i, h in enumerate(hosp):
            if(i != hlen-1):
                print h.name + ' (' + str(h.hq) + '),',
            else:
                print h.name + ' (' + str(h.hq) + ') ;'
        print('@End\n')

        print('@PreferenceListsA')
        for r in res:
            print r.name + ' :',
            for i, h in enumerate(r.pref):
                if(i != len(r.pref)-1):
                    print h.name + ',',
                else:
                    print h.name + ' ;'
        print('@End\n')

        print('@PreferenceListsB')
        for h in hosp:
            print h.name + ' :',
            for i, r in enumerate(h.pref):
                if(i != len(h.pref)-1):
                    print r.name + ',',
                else:
                    print r.name + ' ;'
        print('@End\n')

        print('@ClassificationA')
        for r in res:
            if(len(r.classes) > 0):
                print r.name + ' :',
                for i, c in enumerate(r.classes):
                    if(i != len(r.classes)-1):
                        c.printClass() 
                        print ',',
                    else:
                        c.printClass() 
                        print ';'
        print('@End')

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

def createGraphWithClasses(path):
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
        if(line == '@ClassificationA'):
            choice = 5
            continue

        if(choice == 1):
            line_trim = line.replace(' ', '')[:-2]
            line_split = line_trim.split('),')
            for res in line_split:
                res_split = res.split('(')
                r = res_split[0]
                quotas = res_split[1].split(',')
                lq = 0
                hq = int(quotas[0])
                g.residents.append(Resident(r, hq))

        if(choice == 2):
            line_trim = line.replace(' ', '')[:-2]
            line_split = line_trim.split('),')
            for hosp in line_split:
                hosp_split = hosp.split('(')
                h = hosp_split[0]
                quotas = hosp_split[1].split(',')
                lq = 0
                hq = int(quotas[0])
                g.hospitals.append(Hospital(h, lq, hq))

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

        if(choice == 5):
            line_trim = line.replace(' ', '')[:-1]
            temp_split = line_trim.split(':')
            r = g.getResident(temp_split[0])
            classes_str = temp_split[1]
            classes = classes_str.split('}')[:-1]
            for i in range(len(classes)):
                if(i == 0):
                    classes[i] = classes[i][1:]
                else:
                    classes[i] = classes[i][2:]
            for c in classes:
                class_split = c.split('-')
                class_members = class_split[0][1:-1].split(',')
                class_cap = int(class_split[1])
                temp_class = Classification()
                temp_class.class_list = class_members
                temp_class.cap = class_cap
                r.classes.append(temp_class)

    f.close()
    return g

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
