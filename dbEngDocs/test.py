from importVariablesFile import importVariablesFile

import mongoengine as me
import Cables as Cables
import CableRun as CableRun
import importCSVData as importCSV
import hashlib as hash
import pymongo
import dbConnect
import random as r

database = "dbEngDocs"
coll = "Cable"

files = ["CABLESOlexSinglePhase1CCuV-90.csv",
         "CABLESOlexSinglePhase1CCuAlX-90.csv",
         "CABLESOlexSinglePhase2C+ECuAlV-90.csv",
         # "CABLESOlexThreePhase1CCuAlX-90.csv",
         "CABLESOlexThreePhase1CCuAlV-90.csv",
         "CABLESOlexThreephase3C+E4C+ECuAlV-90.csv",
         "CABLESOlexThreephase3C+E4C+ECuAlX-90.csv",
         "CABLESOlexSinglePhase2C+ECuAlX-90.csv"]
cablerunsImport = ['CABLERUNDummyInstallation.csv']
folder = './database/'

db = me.connect(database)


def importCables():
    """
    Bulk import of cables.
    :return:
    """
    for each in files:
        path = folder+each
        Cables.import_cable_data(db, path)


def importRuns():
    """
    Bulk import of cable runs.
    :return:
    """
    for each in cablerunsImport:
        path = folder+each
        CableRun.import_cablerun_data(db, path)


def addRandomCables(number, cableRuns):
    """
    Add a number of random cables to each cable run. Each cable shall be different.
    :param number: The number of cables to be added to each run.
    :param cableRuns: The query object containing the runs.
    :return:
    """
    for run in cableRuns:
        i = 0
        x = []
        while i < number:
            seed = r.uniform(0, 0.5) * 1000
            cable = Cables.Cable.objects.find_cablecurrent_gte('UNENCLOSED_SPACED', seed).find_corearrangement(
                '4C+E').first()
            x.append(cable)
            i += 1
        run.add_cable(x)


# importCables()
# importRuns()

cable_runs = CableRun.CableRun.objects().no_dereference()
# cable = Cables.Cable.objects.find_hasneutral(False)

# for each in cable_runs:
#     # print("###")
#     i = each.query_cable1()
#     # print(i)
#     for x in i:
#         # print(x)
#         # print('----')
#         print('{} : {} {}' .format(each.circuit.loadCurrent, x.description, x.circuitType))

# addRandomCables(2, cable_runs)

# for each in cable:
#     print(each.description)

# i = cable_runs.find_empty_cable_run()
# for run in cable_runs:
#     print(run.description)
# # ------- >>> TEST Calc CCC

# def gen(i):
#     for each in i:
#         yield each

# x = 0
# v = gen(cable)
# while x < 5:
#     print(next(v).description)
#     x += 1

# print(len(cable))
# for i in cable:
#     print(i.description)

    # for x in i.installMethod:
    #     if x.name == install:
    #         for each in x:
    #             print(each)
        # print(i.description, i.installMethod.)

# >>>> Size cable run cables
# for cablerun in cable_runs:
#     print("\n")
#     print(cablerun.description)
#     cablerun.size_cablerun() #maxconductorsize=630) #maxconductorsize=25)

    # for each in cablerun.show_cables():
    #     print("{}".format(each.description))

for cableRun in cable_runs:
    cableRun.setCableArmour('nil')
    print(cableRun.default.cableArmour)
