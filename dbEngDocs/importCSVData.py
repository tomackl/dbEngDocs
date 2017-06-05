#
# coding: UTF-8

import csv


def import_data_generator(path):
    """
    This function will import the documents listed in a .csv file.

    BASIC OUTLINE:
    1. import CSV file
    2. use the header as the field values. (assume correctly formated).
    3. loop through the file creating an object of 'x'
    4. save() and the del() object 'x'
    5. next document
    :param collection: mongoDB collection
    :param path: path to the file
    """
    # TODO: Does this have to be a generator?
    try:
        with open(path) as dataFile:
            reader = csv.DictReader(dataFile)
            for row in reader:
                # print("{} {}" .format(reader.line_num, row))
                yield row

    except Exception as e:
        pass

#     what else needs to go here?





def exportData(temp):
    """
    Placeholder
    """
    pass