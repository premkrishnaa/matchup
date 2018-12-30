#!/usr/bin/python
from __future__ import print_function
import cplex
from genLP import *
import os

def answer():
    # model = cplex.Cplex()
    # model.objective.set_sense(model.objective.sense.maximize)
    # model.variables.add(names=["x1", "x2"], lb=[0.0]*2, obj=[1.0]*2, types=[model.variables.type.integer]*2)

    # model.linear_constraints.add(
    #     lin_expr=[cplex.SparsePair(ind=["x1", "x2"], val=[1.0, 2.0]),
    #               cplex.SparsePair(ind=["x1", "x2"], val=[4.0, 2.0]),
    #               cplex.SparsePair(ind=["x1", "x2"], val=[-1.0, 1.0])],
    #     senses=["L"]*3,
    #     rhs=[4.0, 12.0, 1.0])

    # model = cplex.Cplex("LP_HRLQ/master/n1_1000_n2_100_k_15/1000_100_15_10_2.txt")
    f1 = open('LP_HRLQ/hrlq_soln_integral_small.txt', 'w', buffering=0)
    f2 = open('LP_HRLQ/hrlq_soln_fractional_small.txt', 'w', buffering=0)
    f3 = open('LP_HRLQ/hrlq_soln_difference_small.txt', 'w', buffering=0)
    model1 = cplex.Cplex("LP_HRLQ/samples/instance_4.txt")
    model1.solve()
    model2 = cplex.Cplex("LP_HRLQ/samples/instance_4_.txt")
    model2.solve()

    var = model1.variables.get_names()

    f1.write("Cost: {}\n".format(model1.solution.get_objective_value()))
    f2.write("Cost: {}\n".format(model2.solution.get_objective_value()))
    for v in var:
        v1 = model1.solution.get_values(v)
        v2 = model2.solution.get_values(v)
        if(v1 != 0.0):
            f1.write(v + ': ' + str(v1) + '\n') 
        if(v2 != 0.0):
            f2.write(v + ': ' + str(v2) + '\n')
        if(v1 != v2):
            if(v1 == 0.0):
                v1 = 0.0
            f3.write(v + ': ' + str(v1) + ', ' + str(v2) + '\n')

    f1.close()
    f2.close()
    f3.close()

def generateHRLPFiles():
    path = 'popular/HR/'
    print('master:')
    folders = ['n1_1000_n2_1000_k_5', 'n1_1000_n2_100_k_5', 'n1_1000_n2_10_k_5', 'n1_1000_n2_20_k_5']
    for folder in folders:
        print('\n\t' + folder + ':')
        folder_split = folder.split('_')
        n1 = int(folder_split[1])
        n2 = int(folder_split[3])
        hq = n1/n2
        path_ = path + 'master/' + folder + '/'
        outpath = 'LP_HR/master/' + folder + '/'
        file_prefix = str(n1) + '_' + str(n2) + '_' + folder_split[5] + '_' + str(hq) + '_'
        for i in range(1, 11):
            print('\t\t#{}'.format(i))
            fulloutpath = outpath + file_prefix + str(i) + '_.txt'
            fullpath = path_ + file_prefix + str(i) + '.txt'
            hr = 1
            if(hq == 1):
                hr = 2
            g = createGraph(fullpath, hr)
            generateStableLP(g, fulloutpath, 1)

    print('\nrandom:')
    folders = ['n1_1000_n2_1000_k_5', 'n1_1000_n2_100_k_5', 'n1_1000_n2_10_k_5', 'n1_1000_n2_20_k_5']
    for folder in folders:
        print('\n\t' + folder + ':')
        folder_split = folder.split('_')
        n1 = int(folder_split[1])
        n2 = int(folder_split[3])
        hq = n1/n2
        path_ = path + 'random/' + folder + '/'
        outpath = 'LP_HR/random/' + folder + '/'
        file_prefix = str(n1) + '_' + str(n2) + '_' + folder_split[5] + '_' + str(hq) + '_'
        for i in range(1, 11):
            print('\t\t#{}'.format(i))
            fulloutpath = outpath + file_prefix + str(i) + '_.txt'
            fullpath = path_ + file_prefix + str(i) + '.txt'
            hr = 1
            if(hq == 1):
                hr = 2
            g = createGraph(fullpath, hr)
            generateStableLP(g, fulloutpath, 1)

    print('\nshuffle:')
    folders = ['n1_1000_n2_1000_k_5', 'n1_1000_n2_100_k_5', 'n1_1000_n2_10_k_5', 'n1_1000_n2_20_k_5']
    for folder in folders:
        print('\n\t' + folder + ':')
        folder_split = folder.split('_')
        n1 = int(folder_split[1])
        n2 = int(folder_split[3])
        hq = n1/n2
        path_ = path + 'shuffle/' + folder + '/'
        outpath = 'LP_HR/shuffle/' + folder + '/'
        file_prefix = str(n1) + '_' + str(n2) + '_' + folder_split[5] + '_' + str(hq) + '_'
        for i in range(1, 11):
            print('\t\t#{}'.format(i))
            fulloutpath = outpath + file_prefix + str(i) + '_.txt'
            fullpath = path_ + file_prefix + str(i) + '.txt'
            hr = 1
            if(hq == 1):
                hr = 2
            g = createGraph(fullpath, hr)
            generateStableLP(g, fulloutpath, 1)

def generateLPFiles():
    path = 'popular/HRLQ/'
    print('master:')
    folders = ['n1_1000_n2_100_k_15', 'n1_1000_n2_100_k_5',
               'n1_1000_n2_10_k_5', 'n1_1000_n2_20_k_5']
    for folder in folders:
        print('\n\t' + folder + ':')
        folder_split = folder.split('_')
        n1 = int(folder_split[1])
        n2 = int(folder_split[3])
        hq = n1/n2
        path_ = path + 'master/' + folder + '/'
        outpath = 'LP_HRLQ/master/' + folder + '/'
        file_prefix = str(n1) + '_' + str(n2) + '_' + folder_split[5] + '_' + str(hq) + '_'
        for i in range(1, 11):
            print('\t\t#{}'.format(i))
            fulloutpath = outpath + file_prefix + str(i) + '.txt'
            fulloutpath_ = outpath + file_prefix + str(i) + '_.txt'
            fullpath = path_ + file_prefix + str(i) + '.txt'
            g = createGraph(fullpath)
            generateMinBPLP(g, fulloutpath_, 0)
            # generateMinBPLP(g, fulloutpath, 1)

    print('\nshuffle:')
    folders = ['n1_1000_n2_100_k_15', 'n1_1000_n2_100_k_5',
               'n1_1000_n2_10_k_5', 'n1_1000_n2_20_k_5']
    for folder in folders:
        print('\n\t' + folder + ':')
        folder_split = folder.split('_')
        n1 = int(folder_split[1])
        n2 = int(folder_split[3])
        hq = n1/n2
        path_ = path + 'shuffle/' + folder + '/'
        outpath = 'LP_HRLQ/shuffle/' + folder + '/'
        file_prefix = str(n1) + '_' + str(n2) + '_' + folder_split[5] + '_' + str(hq) + '_'
        for i in range(1, 11):
            print('\t\t#{}'.format(i))
            fulloutpath = outpath + file_prefix + str(i) + '.txt'
            fulloutpath_ = outpath + file_prefix + str(i) + '_.txt'
            fullpath = path_ + file_prefix + str(i) + '.txt'
            g = createGraph(fullpath)
            generateMinBPLP(g, fulloutpath_, 0)
            generateMinBPLP(g, fulloutpath, 1)

def feasbilityChecker():
    path = 'popular/HRLQ/'
    print('master:')
    folders = ['n1_1000_n2_100_k_15', 'n1_1000_n2_100_k_25', 'n1_1000_n2_100_k_5', 'n1_1000_n2_100_k_50',
               'n1_1000_n2_100_k_75', 'n1_1000_n2_100_k_80', 'n1_1000_n2_10_k_5', 'n1_1000_n2_20_k_15',
               'n1_1000_n2_20_k_5']
    for folder in folders:
        print('\n\t' + folder + ':')
        folder_split = folder.split('_')
        n1 = int(folder_split[1])
        n2 = int(folder_split[3])
        hq = n1/n2
        path_ = path + 'master/' + folder + '/'
        file_prefix = str(n1) + '_' + str(n2) + '_' + folder_split[5] + '_' + str(hq) + '_'
        for i in range(1, 11):
            fullpath = path_ + file_prefix + str(i) + '.txt'
            g = createGraph(fullpath)
            g_y = getYokoiInstance(g)
            m = getStableMatching(g_y)
            print('\t\t#{}.\t{}\t{}'.format(i, checkEnvyFreeFeasibility(g_y), verifyEnvyFree(g, g_y)))

    print('\nrandom:')
    folders = ['n1_1000_n2_20_k_5', 'n1_1000_n2_100_k_5']
    for folder in folders:
        print('\n\t' + folder + ':')
        folder_split = folder.split('_')
        n1 = int(folder_split[1])
        n2 = int(folder_split[3])
        hq = n1/n2
        path_ = path + 'random/' + folder + '/'
        file_prefix = str(n1) + '_' + str(n2) + '_' + folder_split[5] + '_' + str(hq) + '_'
        for i in range(1, 11):
            fullpath = path_ + file_prefix + str(i) + '.txt'
            g = createGraph(fullpath)
            g_y = getYokoiInstance(g)
            m = getStableMatching(g_y)
            print('\t\t#{}.\t{}\t{}'.format(i, checkEnvyFreeFeasibility(g_y), verifyEnvyFree(g, g_y)))

    print('\nshuffle:')
    folders = ['n1_1000_n2_100_k_15', 'n1_1000_n2_100_k_25', 'n1_1000_n2_100_k_5', 'n1_1000_n2_100_k_50',
               'n1_1000_n2_100_k_75', 'n1_1000_n2_10_k_5', 'n1_1000_n2_20_k_15', 'n1_1000_n2_20_k_5']
    for folder in folders:
        print('\n\t' + folder + ':')
        folder_split = folder.split('_')
        n1 = int(folder_split[1])
        n2 = int(folder_split[3])
        hq = n1/n2
        path_ = path + 'shuffle/' + folder + '/'
        file_prefix = str(n1) + '_' + str(n2) + '_' + folder_split[5] + '_' + str(hq) + '_'
        for i in range(1, 11):
            fullpath = path_ + file_prefix + str(i) + '.txt'
            g = createGraph(fullpath)
            g_y = getYokoiInstance(g)
            m = getStableMatching(g_y)
            print('\t\t#{}.\t{}\t{}'.format(i, checkEnvyFreeFeasibility(g_y), verifyEnvyFree(g, g_y)))

def getHRStableSizes():
    f = open('stats_LP_HR_re.txt', 'w', buffering=0)
    folders = ['n1_1000_n2_1000_k_5', 'n1_1000_n2_100_k_5', 'n1_1000_n2_10_k_5', 'n1_1000_n2_20_k_5']
    main_folders = ['master', 'random', 'shuffle']
    path = 'LP_HR'
    for main_folder in main_folders:
        f.write(main_folder + '\n')
        for folder in folders:
            avg = 0.0
            f.write(folder + ':\n')
            folder_split = folder.split('_')
            n1 = int(folder_split[1])
            n2 = int(folder_split[3])
            hq = n1/n2
            file_prefix = str(n1) + '_' + str(n2) + '_' + folder_split[5] + '_' + str(hq) + '_'
            for i in range(1, 11):
                f.write('\t#{}:\t'.format(i))
                fullpath = path + '/' + main_folder + '/' + folder + '/' + file_prefix + str(i) + '.txt'
                model = cplex.Cplex(fullpath)
                model.solve()
                status = model.solution.get_status()
                soln = model.solution.get_objective_value()
                avg += (0.1*soln)
                f.write("Solution status: {},\t".format(status))
                f.write("Size: {}\n".format(soln))
            f.write("\tAverage Size: {}\n\n".format(avg))

    f.close()

def main():
    # generateLPFiles()
    feasbilityChecker()
    # g = createGraph("samples/instance_4.txt")
    # g_one = getOnetoOneInstance(g)
    # generateEnvyFreeLP(g_one, "LP_HRLQ/samples/instance_2.txt", 0)
    # g = createGraph("base_instances/master/n1_100_n2_100_k_20/100_100_20_1_7.txt", 2)
    # m = getStableMatching(g)
    # generateMaxCardLP(g, 'temp.txt')
    # model = cplex.Cplex('temp.txt')
    # model.solve()
    # var = model.variables.get_names()
    # for v in var:
    #     v_split = v.split('_')
    #     h_name = 'h' + v_split[2]
    #     h = g.getHospital(h_name)
    #     if(model.solution.get_values(v) != 0.0):
    #         if(len(h.pref) > 0 and len(h.matched) == 0):
    #             h.lq = 1

    # for h in g.hospitals:
    #     print(h.name + ' (' + str(h.lq) + ', ' + str(h.hq) + '), ', end='')
    # print('')
    # os.remove('temp.txt')
    # generateEnvyFreeLP(g, "LP_HRLQ/samples/instance_4.txt", 1)
    # generateEnvyFreeLP(g, "LP_HRLQ/samples/instance_4_.txt", 0)
    # answer()
    # generateHRLPFiles()
    # getHRStableSizes()

if __name__ == '__main__':
    main()
