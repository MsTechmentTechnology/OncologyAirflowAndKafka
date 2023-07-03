## Title and Description

This Proof of Concept (POC) project demonstrates the migration of CSV, XML, and FHIR data to Snowflake using Apache Airflow. The POC showcases the orchestration of data extraction, transformation, and loading processes, highlighting the efficiency and feasibility of using Airflow for seamless data migration to Snowflake.
## Documentation

### Prerequisites
Configure your AWS credentials in Airflow web UI. Update the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY variables with your AWS credentials.

Configure Snowflake credentials in Airflow web UI. Update the database name, account, username , password, schema with your snowflake credentials.

Create a Snowflake database and tables as per your requirements. Adjust the table schemas and credentials in snowflake_hook.py accordingly.

### Explaination

This Proof of Concept (POC) project demonstrates a data migration workflow that involves the migration of CSV data from MySQL to an AWS S3 bucket, extraction of data from a FHIR API, XML file stored in AWS S3 bucket and migration of these files to Snowflake. The POC aims to showcase the integration of various data sources and the seamless migration process to Snowflake for efficient data processing and analytics.

The project utilizes Apache Airflow, an open-source platform for orchestrating workflows, to manage the data migration tasks. The Airflow DAG defines the workflow and dependencies between the tasks.

The first task in the workflow involves migrating CSV data from a MySQL database.  This step ensures that the CSV data is stored in a centralized location for further processing.

The second task focuses on extracting data from a FHIR API using  Python script which retrieves the required data. This data is then stored in the same AWS S3 bucket for consolidation.

The third task focuses on extracting data from an XML file which is stored in AWS S3 bukcet using  Python script which retrieves the required data. This data is then stored in the same AWS S3 bucket for consolidation.

Finally, the fourth task focuses on migrating the data from the AWS S3 bucket to Snowflake. The SnowflakeOperator interacts with Snowflake and loads the CSV and FHIR data into the appropriate Snowflake tables. This enables further analysis and processing of the data using Snowflake's powerful querying capabilities.

Throughout the POC, custom operators, hooks, and utility functions are employed to handle specific tasks and facilitate seamless data migration. The project structure ensures modularity and extensibility, allowing for easy integration of additional data sources and migration targets.

By following the provided instructions, users can set up the POC on their local environment and trigger the data migration process using the Airflow UI. The POC serves as a foundation for building robust and scalable data migration workflows, demonstrating the potential for leveraging Airflow and Snowflake for efficient data processing and analysis.



## Installation

Step 1: Fetch docker-compose.yaml
The first thing we’ll need is the docker-compose.yaml file. Create a new directory on your home directory (let’s call it airflow-local):

$ mkdir airflow-local
$ cd airflow-local
And fetch the docker-compose.yaml file (note that we will be using Airflow v2.3.0)

$ curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.3.0/docker-compose.yaml'

Feel free to inspect the compose file and the services defined in it namely airflow-scheduler, airflow-webserver, airflow-worker, airflow-init, flower, postgres and redis.

Step 2: Create directories
Now while you are in the airflow-local directory, we will need to create three additional directories:

dags
logs
plugins
$ mkdir ./dags ./logs ./plugins

Step 3: Setting the Airflow user
Now we would have to export an environment variable to ensure that the folder on your host machine and the folders within the containers share the same permissions. We will simply add these variables into a file called .env.

$ echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
Inspect the content of .env using cat and ensure that it contains the two aforementioned variables.

$ cat .env
AIRFLOW_UID=501
AIRFLOW_GID=0
Step 4: Initialise the Airflow Database
Now we are ready initialise the Airflow Database by first starting the airflow-init container:

$ docker-compose up airflow-init
This service will essentially run airflow db init and create the admin user for the Airflow Database. By default, the account created has the login airflow and the password airflow.

Step 5: Start Airflow services
The final thing we need to do to get Airflow up and running is start the Airflow services we’ve seen in Step 1.

$ docker-compose up
Note that the above command may take a while since multiple services need to be started. Once done, you can verify that these images are up and running using the following command in a new command-line tab:

$ docker ps

Airflow images up and running — Source: Author
Step 6: Access Airflow UI
In order to access Airflow User Interface simply head to your preferred browser and open localhost:8080.
