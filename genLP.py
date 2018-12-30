import sys
sys.path.insert(0, 'classes/')
from graph import *
from stableMatching import *
from yokoiInstance import *
from blowUpInstance import *

def generateMinBPLP(g, path, opt):
    f = open(path, "w")
    f.write("minimize\nblocking_pairs: ")
    for i, edge in enumerate(g.edges):
        f.write('y' + edge.name[1:] + ' ')
        if(i != len(g.edges)-1):
            f.write('+ ')

    f.write('\n\nst\n')
    for r in g.residents:
        r_ind = r.name[1:]
        f.write(r.name + ': ')
        for i, h in enumerate(r.pref):
            h_ind = h.name[1:]
            f.write('x_' + r_ind + '_' + h_ind + ' ')
            if(i != len(r.pref)-1):
                f.write('+ ')
        f.write('<= 1\n')

    for h in g.hospitals:
        h_ind = h.name[1:]
        if(h.lq > 0 and len(h.pref) > 0):
            f.write(h.name + '_lq: ')
            for i, r in enumerate(h.pref):
                r_ind = r.name[1:]
                f.write('x_' + r_ind + '_' + h_ind + ' ')
                if(i != len(h.pref)-1):
                    f.write('+ ')
            f.write('>= ' + str(h.lq) + '\n')

    for h in g.hospitals:
        h_ind = h.name[1:]
        if(len(h.pref) > 0):
            f.write(h.name + '_hq: ')
            for i, r in enumerate(h.pref):
                r_ind = r.name[1:]
                f.write('x_' + r_ind + '_' + h_ind + ' ')
                if(i != len(h.pref)-1):
                    f.write('+ ')
            f.write('<= ' + str(h.hq) + '\n')

    for edge in g.edges:
        r_name = 'r' + str(edge.r_ind)
        h_name = 'h' + str(edge.h_ind)
        res = g.getResident(r_name)
        hosp = g.getHospital(h_name)
        str_to_write = ''

        for i in range(len(hosp.pref)):
            r = hosp.pref[i]
            if(r.name == r_name):
                break
            str_to_write += 'x_' + r.getIndex() + '_' + hosp.getIndex() + ' + '

        for i in range(len(res.pref)):
            h = res.pref[i]
            if(h.name == h_name):
                str_to_write += str(hosp.hq)
            else:
                str_to_write += str(hosp.hq + 1)
            
            str_to_write += ' x_' + res.getIndex() + '_' + h.getIndex() + ' '
            if(h.name == h_name):
                break
            str_to_write += '+ '

        str_to_write += '+ ' + str(hosp.hq) + ' y' + edge.name[1:] + ' >= ' + str(hosp.hq) + '\n'
        f.write('edge_' + res.getIndex() + '_' + hosp.getIndex() + ': ')
        f.write(str_to_write)

    if(opt == 1):
        f.write('\nbin\n')
        for i, edge in enumerate(g.edges):
            f.write(edge.name + ' ')
            if(i%31 == 0 and i != 0):
                f.write('\n')

    # if(opt == 0):
    #     f.write('\nbin\n')
        for i, edge in enumerate(g.edges):
            f.write('y' + edge.name[1:] + ' ')
            if(i%31 == 0 and i != 0):
                f.write('\n')
        f.write('\n')

    f.write('\nend')
    f.close()


def generateMaxCardLP(g, path):
    f = open(path, "w")
    f.write("maximize\nsize: ")
    for i, edge in enumerate(g.edges):
        f.write(edge.name + ' ')
        if(i != len(g.edges)-1):
            f.write('+ ')

    f.write('\n\nst\n')
    for r in g.residents:
        r_ind = r.name[1:]
        f.write(r.name + ': ')
        for i, h in enumerate(r.pref):
            h_ind = h.name[1:]
            f.write('x_' + r_ind + '_' + h_ind + ' ')
            if(i != len(r.pref)-1):
                f.write('+ ')
        f.write('<= 1\n')

    for h in g.hospitals:
        h_ind = h.name[1:]
        if(len(h.pref) > 0):
            f.write(h.name + '_hq: ')
            for i, r in enumerate(h.pref):
                r_ind = r.name[1:]
                f.write('x_' + r_ind + '_' + h_ind + ' ')
                if(i != len(h.pref)-1):
                    f.write('+ ')
            f.write('<= ' + str(h.hq) + '\n')

    f.write('\nbin\n')
    for i, edge in enumerate(g.edges):
        f.write(edge.name + ' ')
        if(i%31 == 0 and i != 0):
            f.write('\n')
    f.write('\n')

    f.write('\nend')
    f.close()

def generateStableLP(g, path, opt):
    f = open(path, "w")
    f.write("maximize\nsize: ")
    for i, edge in enumerate(g.edges):
        f.write(edge.name + ' ')
        if(i != len(g.edges)-1):
            f.write('+ ')

    f.write('\n\nst\n')
    for r in g.residents:
        r_ind = r.name[1:]
        f.write(r.name + ': ')
        for i, h in enumerate(r.pref):
            h_ind = h.name[1:]
            f.write('x_' + r_ind + '_' + h_ind + ' ')
            if(i != len(r.pref)-1):
                f.write('+ ')
        f.write('<= 1\n')

    for h in g.hospitals:
        h_ind = h.name[1:]
        if(len(h.pref) > 0):
            f.write(h.name + '_hq: ')
            for i, r in enumerate(h.pref):
                r_ind = r.name[1:]
                f.write('x_' + r_ind + '_' + h_ind + ' ')
                if(i != len(h.pref)-1):
                    f.write('+ ')
            f.write('<= ' + str(h.hq) + '\n')

    for edge in g.edges:
        r_name = 'r' + str(edge.r_ind)
        h_name = 'h' + str(edge.h_ind)
        res = g.getResident(r_name)
        hosp = g.getHospital(h_name)
        str_to_write = ''

        for i in range(len(hosp.pref)):
            r = hosp.pref[i]
            if(r.name == r_name):
                break
            str_to_write += 'x_' + r.getIndex() + '_' + hosp.getIndex() + ' + '

        for i in range(len(res.pref)):
            h = res.pref[i]
            if(h.name == h_name):
                str_to_write += str(hosp.hq)
            else:
                str_to_write += str(hosp.hq)
            
            str_to_write += ' x_' + res.getIndex() + '_' + h.getIndex() + ' '
            if(h.name == h_name):
                break
            str_to_write += '+ '

        str_to_write += '>= ' + str(hosp.hq) + '\n'
        f.write('edge_' + res.getIndex() + '_' + hosp.getIndex() + ': ')
        f.write(str_to_write)

    if(opt == 1):
        f.write('\nbin\n')
        for i, edge in enumerate(g.edges):
            f.write(edge.name + ' ')
            if(i%31 == 0 and i != 0):
                f.write('\n')
        f.write('\n')

    f.write('\nend')
    f.close()

def generateEnvyFreeLP(g, path, opt):
    f = open(path, "w")
    f.write("maximize\nsize: ")
    for i, edge in enumerate(g.edges):
        f.write(edge.name + ' ')
        if(i != len(g.edges)-1):
            f.write('+ ')

    f.write('\n\nst\n')
    for r in g.residents:
        r_ind = r.name[1:]
        f.write(r.name + ': ')
        for i, h in enumerate(r.pref):
            h_ind = h.name[1:]
            f.write('x_' + r_ind + '_' + h_ind + ' ')
            if(i != len(r.pref)-1):
                f.write('+ ')
        f.write('<= 1\n')

    for h in g.hospitals:
        h_ind = h.name[1:]
        if(h.lq > 0 and len(h.pref) > 0):
            f.write(h.name + '_lq: ')
            for i, r in enumerate(h.pref):
                r_ind = r.name[1:]
                f.write('x_' + r_ind + '_' + h_ind + ' ')
                if(i != len(h.pref)-1):
                    f.write('+ ')
            f.write('= ' + str(h.lq) + '\n')

    for h in g.hospitals:
        h_ind = h.name[1:]
        if(h.lq == 0 and len(h.pref) > 0):
            f.write(h.name + '_hq: ')
            for i, r in enumerate(h.pref):
                r_ind = r.name[1:]
                f.write('x_' + r_ind + '_' + h_ind + ' ')
                if(i != len(h.pref)-1):
                    f.write('+ ')
            f.write('<= ' + str(h.hq) + '\n')

    for edge in g.edges:
        r_name = 'r' + str(edge.r_ind)
        h_name = 'h' + str(edge.h_ind)
        res = g.getResident(r_name)
        hosp = g.getHospital(h_name)
        flag = 0
        flag_ = 0
        str_to_write = ''
        for i in range(len(hosp.pref)):
            r = hosp.pref[i]
            if(r.name == r_name):
                flag = 1
                continue
            if(flag == 1):
                flag_ = 1
                str_to_write += 'x_' + r.getIndex() + '_' + hosp.getIndex() + ' '
                if(i != len(hosp.pref) - 1):
                    str_to_write += '+ '

        for i in range(len(res.pref)):
            h = res.pref[i]
            if(h.name == h_name):
                break
            flag_ = 1
            str_to_write += '- x_' + res.getIndex() + '_' + h.getIndex() + ' '

        if(flag_ == 1):
            str_to_write += '<= 0\n'
        if(str_to_write != ''):
            f.write('edge_' + res.getIndex() + '_' + hosp.getIndex() + ': ')
            f.write(str_to_write)

    if(opt == 1):
        f.write('\nbin\n')
        for i, edge in enumerate(g.edges):
            f.write(edge.name + ' ')
            if(i%31 == 0 and i != 0):
                f.write('\n')
        f.write('\n')

    f.write('\nend')
    f.close()

def generateEnvyFreeLPAlternate(g, path, opt):
    f = open(path, "w")
    f.write("maximize\nsize: ")
    for i, edge in enumerate(g.edges):
        f.write(edge.name + ' ')
        if(i != len(g.edges)-1):
            f.write('+ ')

    f.write('\n\nst\n')
    for r in g.residents:
        r_ind = r.name[1:]
        f.write(r.name + ': ')
        for i, h in enumerate(r.pref):
            h_ind = h.name[1:]
            f.write('x_' + r_ind + '_' + h_ind + ' ')
            if(i != len(r.pref)-1):
                f.write('+ ')
        f.write('<= 1\n')

    for h in g.hospitals:
        h_ind = h.name[1:]
        if(h.lq > 0 and len(h.pref) > 0):
            f.write(h.name + '_lq: ')
            for i, r in enumerate(h.pref):
                r_ind = r.name[1:]
                f.write('x_' + r_ind + '_' + h_ind + ' ')
                if(i != len(h.pref)-1):
                    f.write('+ ')
            f.write('= ' + str(h.lq) + '\n')

    for h in g.hospitals:
        h_ind = h.name[1:]
        if(h.lq == 0 and len(h.pref) > 0):
            f.write(h.name + '_hq: ')
            for i, r in enumerate(h.pref):
                r_ind = r.name[1:]
                f.write('x_' + r_ind + '_' + h_ind + ' ')
                if(i != len(h.pref)-1):
                    f.write('+ ')
            f.write('<= ' + str(h.hq) + '\n')

    for edge in g.edges:
        r_name = 'r' + str(edge.r_ind)
        h_name = 'h' + str(edge.h_ind)
        res = g.getResident(r_name)
        hosp = g.getHospital(h_name)
        for r_dash in hosp.pref[:hosp.getRank(r_name)-1]:
            f.write('triplet_' + res.getIndex() + '_' + hosp.getIndex() + '_' + r_dash.getIndex() + ': ')
            f.write(edge.name + ' ')
            for h_dash in r_dash.pref[:r_dash.getRank(h_name)-1]:
                f.write('- x_' + r_dash.getIndex() + '_' + h_dash.getIndex() + ' ')
            f.write('<= 0\n')

    for edge in g.edges:
        r_name = 'r' + str(edge.r_ind)
        h_name = 'h' + str(edge.h_ind)
        res = g.getResident(r_name)
        hosp = g.getHospital(h_name)
        flag = 0
        flag_ = 0
        str_to_write = ''
        for i in range(len(hosp.pref)):
            r = hosp.pref[i]
            if(r.name == r_name):
                flag = 1
                continue
            if(flag == 1):
                flag_ = 1
                str_to_write += 'x_' + r.getIndex() + '_' + hosp.getIndex() + ' '
                if(i != len(hosp.pref) - 1):
                    str_to_write += '+ '

        for i in range(len(res.pref)):
            h = res.pref[i]
            if(h.name == h_name):
                break
            flag_ = 1
            str_to_write += '- x_' + res.getIndex() + '_' + h.getIndex() + ' '

        if(flag_ == 1):
            str_to_write += '<= 0\n'
        if(str_to_write != ''):
            f.write('edge_' + res.getIndex() + '_' + hosp.getIndex() + ': ')
            f.write(str_to_write)

    if(opt == 1):
        f.write('\nbin\n')
        for i, edge in enumerate(g.edges):
            f.write(edge.name + ' ')
            if(i%31 == 0 and i != 0):
                f.write('\n')
        f.write('\n')

    f.write('\nend')
    f.close()
