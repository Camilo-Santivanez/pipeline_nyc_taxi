#!/usr/bin/env python
# coding: utf-8

import pandas as pd 
from sqlalchemy import create_engine, Integer, DateTime
import click

#NYC green taxi data
taxi_trips_nov2025 = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
zone_dataset = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

#Ensuring data types
dtypes = { 
    "VendorID": Integer(),
    "lpep_pickup_datetime": DateTime(),
    "lpep_dropoff_datetime": DateTime(),
    "RatecodeID": Integer(), 
    "passenger_count": Integer(),
    "payment_type": Integer(),
    "trip_type": Integer()
}   

@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='green_ny_taxi', help='PostgreSQL database name')
@click.option('--target-table', default='green_taxi_data', help='Target table name')
@click.option('--zones-table', default='taxi_zones', help='Zones table name')
def ingest_data(pg_user, pg_pass, pg_host, pg_port, pg_db, target_table, zones_table):

    #LOAD DATA INTO DATAFRAMES 
    df_taxi_trips = pd.read_parquet(taxi_trips_nov2025)
    df_zone = pd.read_csv(zone_dataset)

    # Creating an engine using SQLAlchemy
    engine = create_engine(f'postgresql+psycopg2://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # Create target table first
    try: 
        print("Creating tables ...")
        df_taxi_trips.head(0).to_sql(name=f'{target_table}', con=engine, if_exists = "replace", 
                                     index=False, dtype=dtypes)
    except Exception as e:
        print(f'Error at creating the table: {e}')
        return
    #Load into Postgres
    try:
        print("Loading data into Postgres")
        df_taxi_trips.to_sql(name=f'{target_table}', con=engine, if_exists = "append", index=False,
                             method="multi", chunksize=5000)
    except Exception as e:
        print(f'Error inserting data into the table: {e}')
        return 
    
    #Adding zone tables
    try:
        print("Creating zones table ...")
        df_zone.head(0).to_sql(name=zones_table, con=engine, if_exists="replace", index=False)
        print("Loading zones into Postgres")
        df_zone.to_sql(name=zones_table, con=engine, if_exists="append", index=False)
    except Exception as e:
        print(f'Error inserting zones into the table: {e}')
        return

# To make it executable
if __name__ == '__main__':
    ingest_data()