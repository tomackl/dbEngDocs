#
# coding: utf-8

# This module is used to manage variables into the DB and their use within the app.

import json

class importVariablesFile():
    """
    This class is used to open and import the actual .config file. The class will provide a JSON object that can be
    passed to another object.
    """

    def __init__(self, path):
        """
        :param path: the path to the file.
        """
        self.path = path
        self.configFile = None
        self.openConfigJSON()

    def __del__(self):
        """
        Tidy up on deletion of the object.
        """
        if self.configFile is not None:
            self.closeConfig()
            # print("File closed")
        else:
            pass

    def __str__(self):
        """
        """
        return str(self.configFile)

    def openConfigJSON(self):
        """
        This function is intended to open a JSON formatted .config file.
        """
        self.configFile = json.load(open(self.path))

    def closeConfig(self):
        """
        Close the JSON .config file.
        """
        pass

    # def configFile(self):
    #     """
    #     Return the imported file.
    #     """
    #     return self.configFile
