import pytest, yaml
from pymongo import MongoClient

class TestClass:
    with open("config.yaml", "r") as f:
        conf = yaml.safe_load(f)['MOOC']
    assert conf

    client = MongoClient(conf['mongoUri'])

    def test_mongodb_exist(self):
        assert self.client != None

    def test_collection_exist(self):
        with open("config.yaml", "r") as f:
            conf = yaml.safe_load(f)['MOOC']
        collection = self.client[conf['db']][conf['collection']]
        print(collection)
        returned = collection.find_one()
        assert returned != None