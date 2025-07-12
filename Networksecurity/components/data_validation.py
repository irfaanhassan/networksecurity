from Networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from Networksecurity.entity.config_entity import DataValidationConfig
from Networksecurity.exception.exception import NetworkSEcurityException
from Networksecurity.logging.logger import logging
from scipy.stats import ks_2samp#for drift data
import pandas as pd
import numpy as np
import os,sys
from Networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from Networksecurity.utils.main_utils.utils import read_yaml_files,write_yaml_file


class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_config=read_yaml_files(SCHEMA_FILE_PATH)
        except Exception as e:
            raise  NetworkSEcurityException(e,sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise NetworkSEcurityException(e,sys)
        
    def valid_no_of_col(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_col=len(self.schema_config)
            logging.info(f"Requires number of coloumns:{number_of_col}")
            logging.info(f"data frame has coloumns:{len(dataframe.columns)}")
            if len(dataframe.columns)==number_of_col:
                return True
            return False
        except Exception as e :
            raise NetworkSEcurityException(e,sys)
        

    
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for coloumn in base_df.columns:
               d1=base_df[coloumn]
               d2=current_df[coloumn]
               is_same_dist=ks_2samp(d1,d2)
               if threshold<=is_same_dist.pvalue:
                   is_found=False

               else:
                   is_found=True
                   status=False
               report.update({coloumn:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                }}) 
            drift_report_path=self.data_validation_config.drift_report_file_path

            dir_path=os.path.dirname(drift_report_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_path,content=report)
        except Exception as e:
            raise NetworkSEcurityException(e,sys)
        

        


    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            train_df=DataValidation.read_data(train_file_path)
            test_df=DataValidation.read_data(test_file_path)


            #validate no of col
            status=self.valid_no_of_col(dataframe=train_df)
            if not status:
                error_message=f"Train dataframe does not contain all coloumns.\n"
            status=self.valid_no_of_col(dataframe=test_df)
            if not status:
                error_message=f"Test dataframe does not contain all coloumns.\n"

            if len(train_df.select_dtypes(include='number').columns) > 0:
                error_message = f'train_df consists of numeric columns'
            #drift data check
            status=self.detect_dataset_drift(base_df=train_df,current_df=test_df)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_df.to_csv(
                self.data_validation_config.valid_train_file_path, index=False, header=True

            )

            test_df.to_csv(
                self.data_validation_config.valid_test_file_path, index=False, header=True
            )
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSEcurityException(e,sys)




            
        except Exception as e:
            raise NetworkSEcurityException(e,sys)    