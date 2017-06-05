# import mongoengine as me
# import Cables as Cables
# import importCSVData as importCSV
# import pymongo
#
# database = "dbEngDocs"
# coll = "Cable"
# client = pymongo.MongoClient()
# db = client[database]
#
# files = ["CABLESOlexSinglePhase1CCuV-90.csv", "CABLESOlexSinglePhase1CCuAlX-90.csv", "CABLESOlexSinglePhase2C+ECuAlV-75.csv", "CABLESOlexThreephase3C+E4C+ECuAlV-75.csv", "CABLESOlexThreephase3C+E4C+ECuAlX-90.csv", "CABLESOlexSinglePhase2C+ECuAlX-90.csv"]
# folder = './database/'
#
# db = me.connect(database)
# for each in files:
#     path = folder+each
#     print(each)
#     temp = importCSV.import_data_generator(path)
#     Cables.import_cable_data(db, path)