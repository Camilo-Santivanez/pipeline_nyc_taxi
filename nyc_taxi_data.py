#!/usr/bin/env python
# coding: utf-8

# # Ingest Data
# First we import all the necessary libraries

# In[1]:


import pandas as pd 
from sqlalchemy import create_engine, Integer, DateTime


# Now we import the data into a dataframe

# In[2]:


# Parquet
taxi_trips_nov2025 = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet"
#CSV
zone_dataset = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv"

df_taxi_trips = pd.read_parquet(taxi_trips_nov2025)
df_zone = pd.read_csv(zone_dataset)


# # First visualization of the data that we are going to use:

# In[3]:


df_taxi_trips


# In[4]:


df_taxi_trips.dtypes


# In[5]:


df_zone


# In[6]:


df_zone.dtypes


# # Preparing the data for the ingestion into Postgres

# In[7]:


# Creating an engine using SQLAlchemy
engine = create_engine('postgresql+psycopg2://root:root@localhost:5432/green_ny_taxi')


# Get DDL schema (sql command): 

# In[8]:


print(pd.io.sql.get_schema(df_taxi_trips, name="green_taxi_data", con=engine))


# Check dtypes:

# In[9]:


#To deal with NaN values, Pandas considers columns type as Float instead of Integer
#So we deal with it manually, ensuring that the data type in SQL is as we expected

dtypes = { 
    "VendorID": Integer(),
    "lpep_pickup_datetime": DateTime(),
    "lpep_dropoff_datetime": DateTime(),
    "RatecodeID": Integer(), 
    "passenger_count": Integer(),
    "payment_type": Integer(),
    "trip_type": Integer()
}   


# Checking again the DDL schema

# In[10]:


print(pd.io.sql.get_schema(df_taxi_trips, name="green_taxi_data", con=engine, dtype=dtypes))


# Now we check the schema structure is correctly created:

# In[11]:


df_taxi_trips.head(0).to_sql(name="green_taxi_data", con=engine, if_exists = "replace")
# 0 means it works 


# # Finally, we ingest the data into PostgresQL

# In[12]:


df_taxi_trips.to_sql(name="green_taxi_data", con=engine, if_exists = "append")


# We check if everything works:

# In[13]:


check = pd.read_sql("SELECT * FROM green_taxi_data LIMIT 10;", con = engine)
print(check)


# Number of rows:

# In[14]:


rows_number = pd.read_sql("SELECT COUNT(1) FROM green_taxi_data;", con = engine)
print(rows_number)

