import airflow
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.operators.snowflake_operator import SnowflakeOperator
from airflow.contrib.operators.snowflake_operator import SnowflakeOperator
from datetime import datetime, timedelta
import os
import requests
from airflow.models.connection import Connection
import boto3

conn_id='aws_connector'
BUCKET = 'oncologypoc'
name = 'csv/cancerpatient.csv'

# Default settings applied to all tasks
default_args = {
    'owner': 'Rajshri',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5)
}


date = '{{ yesterday_ds_nodash }}'
with DAG('csv_to_snowflake',
         start_date=datetime.today(),
         max_active_runs=3,
        #  schedule_interval='0 * * * *',
         schedule='@once',
         default_args=default_args,
         catchup=False
         ) as dag:

    dummystart = EmptyOperator(task_id='start')
    query1 = [
        """use schema PUBLIC ;""",
        """CREATE OR REPLACE STAGE CSV_STAGE URL= 's3://oncologypoc/csv/' 
            CREDENTIALS = (aws_key_id ='<aws_key_id>' aws_secret_key = '<aws_secret_key>');
        """,
        """CREATE or replace TABLE Cancer_Patient(
            Patient_Id                  varchar,    
            Age                          int,
            Gender                       string,
            Air_Pollution                int,
            Alcohol_use                  string,
            Dust_Allergy                 string,  
            OccuPational_Hazards         int,  
            Genetic_Risk                 int,
            chronic_Lung_Disease         int,  
            Balanced_Diet                int,
            Obesity                      int,
            Smoking                      int,
            Passive_Smoker               int,
            Chest_Pain                   int,
            Coughing_of_Blood            int,  
            Fatigue                      int,
            Weight_Loss                  int,  
            Shortness_of_Breath          int,  
            Wheezing                     int,  
            Swallowing_Difficulty        int,  
            Clubbing_of_Finger_Nails     int,  
            Frequent_Cold                int,
            Dry_Cough                    int,  
            Snoring                      int,
            Level                        string,
            ServivalRateeofPatient       string
            );"""       
    ]
    query2 = [
        """use schema PUBLIC ;""",
        """COPY INTO Cancer_Patient from @CSV_STAGE FILE_FORMAT = (FORMAT_NAME = 'mycsvformat') ON_ERROR = 'CONTINUE';"""

    ]
    snowflakefileformat = SnowflakeOperator(
        task_id="snowflake_file_format",
        sql ="""use schema PUBLIC ; create or replace file format mycsvformat type ='CSV' field_delimiter =',' skip_header = 1;""",
        snowflake_conn_id = "snowflake_connection_demo",
    )
    snowflakestage =SnowflakeOperator(
        task_id="snowfalke_stagecreation",
        sql=query1,
        snowflake_conn_id="snowflake_connection_demo",
    )
    copydatafromstage =SnowflakeOperator(
        task_id="copydatafromstage",
        sql=query2,
        snowflake_conn_id="snowflake_connection_demo",
    )

    dummyend=EmptyOperator(task_id='end')

    dummystart >>snowflakefileformat >>snowflakestage >> copydatafromstage >> transformation  >> dummyend