#
# coding: utf-8


from pymongo import MongoClient

"""
Set up the global variables for connecting to the database.
"""

globalhost = None
globalport = None
globaldb = None
globalclient = None


def set_global_host(value):
    """
    Update the host global variable.
    :param value:
    :return:
    """
    global globalhost
    globalhost = value


def set_global_client(hoststring=None, portnumber=None):
    """
    Update the global 'client' variable.
    :param hoststring:
    :param portnumber:
    :return:
    """
    global globalclient
    globalclient = MongoClient(hoststring, portnumber)


def set_global_database(value):
    """
    Update the global database variable.
    :param value:
    :return:
    """
    global globaldb
    globaldb = value


def define_collection(collection):
    """
    Define a collection that relates to the global database.
    :param collection: the collection to be connected to.
    :return:
    """
    global globaldb
    return globaldb[collection]


class DB:
    """
    Class to allow connection to a MongoDB. Each object allows a separate
    connection to be created. The intention is that these will be used on
    specific collections.
    """
    def __init__(self, host=None, port=None, database=None, *args, **kwargs):
        """
        Initialise the database.
        :param host: DB host details
        :param port: DB host port
        :param db: database name
        :param collection: collection to collect to.
        :param args: random arguments that may be passed to the db.
        :param kwargs: random keyword arguments that may be passed to the db.
        """
        self._host = None
        self._port = None
        self._client = None
        # self._collection = None
        self._connectCollection = None
        self.client()
        # self.client(host, port)
        self._db = database
        # self.collection(collection)
        self.args = args
        self.kwargs = kwargs

    # @property
    def client(self): #, host=None, port=None
        """
        Set the client details.
        :param host: host details
        :param port: host port details
        :return:
        """
        # self._host = host
        # self._port = port
        self._client = MongoClient(self._host, self._port)

    # @client.getter
    # def client(self):
    #     """
    #     Get the client details.
    #     :return:
    #     """
    #     return self._client

    @property
    def db(self, value):
        """
        Set the DB names.
        :param value:
        :return:
        """
        self._db = value

    @db.getter
    def db(self):
        """
        Get the DB name
        :return:
        """
        return self._db

    # @property
    def collection(self, value):
        """
        Set the collection name.
        :param value:
        :return:
        """
        self._collection = value

    # @collection.getter
    # def collection(self):
    #     """
    #     Get the collection name
    #     :return:
    #     """
    #     return self._collection

    @property
    def connect_collection(self):
        """
        Connect to a DB collection
        :return:
        """
        self._connectCollection = self.db[self.collection]

    @connect_collection.getter
    def connect_collection(self):
        """
        Return a connection to a DB collection.
        :return:
        """
        return self._connectCollection


def add_cable():
    # Method to allow the addition of a new cable
    pass


def modify_cable():
    # Method to modify an existing cable.
    pass


def delete_cable():
    # Method to delete an existing cable from the database.
    pass


def export_details():
    # Method to export database details
    pass
