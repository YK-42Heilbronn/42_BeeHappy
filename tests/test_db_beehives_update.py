# python 3.12

import json
import os
import psycopg2
from dotenv import load_dotenv

import __init__
from src.s3_db.a1_connect_fetch import (sensorNodes_dataDict)
from src.s3_db.a98_db_beehives_update import (read_beehives_sensornodes_json,
                                           data_from_RESTAPI,
                                           preparing_beehives_table_data,
                                           trigger_automatic_db_schema_update)


load_dotenv()
db_password = os.getenv("DB_PASSWORD")

# Database connection
conn = psycopg2.connect(
            host=os.getenv("HOST"),
            database="beehappydb3",
            user="beehappyuser3",
            password=db_password,
            port="5432"
        )
cursor = conn.cursor()

json_dict=read_beehives_sensornodes_json()
server_dict=data_from_RESTAPI()


def test_read_beehives_sensornodes_json():
    # json_dict=read_beehives_sensornodes_json()
    # server_dict=data_from_RESTAPI()
    print(json.dumps(json_dict, sort_keys=True, indent=4))
    print("----------------------------------")
    print(json.dumps(server_dict, sort_keys=True, indent=4))
    print("++++++++++++++++++++++++++++++++++")
    print(*preparing_beehives_table_data(json_dict, server_dict), sep='\n')

def test_conditional_automation():
    # --- test with DB
    trigger_automatic_db_schema_update(cursor, json_dict, sensorNodes_dataDict()) 


if __name__=="__main__":
    test_read_beehives_sensornodes_json()
    # test_conditional_automation()
    pass
