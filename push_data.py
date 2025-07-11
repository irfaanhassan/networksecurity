import os
import sys
import json

from dotenv import load_dotenv  
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)
import certifi
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo
from Networksecurity.exception.exception import NetworkSEcurityException
from Networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass

        except Exception as e:
            raise NetworkSEcurityException(e,sys)
        
    def cv_to_jison(self,filepath):
        try:
            data=pd.read_csv(filepath)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSEcurityException(e,sys)
        
    def insert_data_mongodb(self,records,collection,database):
        try:
            self.records=records
            self.collection=collection
            self.database=database

            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database=self.mongo_client[self.database]

            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)

            return (len(self.records))
        except Exception as e:
            raise NetworkSEcurityException(e,sys)
        
if __name__=="__main__":
    Filepath="Network_Data\phisingData.csv"
    DATABASE="irfaan"
    Collection="networkdata"
    networkobj=NetworkDataExtract()
    records=networkobj.cv_to_jison(filepath=Filepath)
    print(records)
    no_of_records=networkobj.insert_data_mongodb(records,Collection,DATABASE)
    print(no_of_records)
