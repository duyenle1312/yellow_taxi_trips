# -*- coding: utf-8 -*-
"""
Original file is located at
    https://colab.research.google.com/drive/1soVQAq3wW4AYBIcFqWP5zSrDe4MDvWni
Author: Duyen Le
"""

"""### Load dataset"""

import pyarrow.parquet as pq
import datetime
import pandas as pd

trips = pq.read_table('yellow_tripdata_2020-01.parquet')
df = trips.to_pandas()

# Filtering out datapoints with timestamp values not in Jan 2020
new_df = df[(df['tpep_dropoff_datetime'] >= pd.Timestamp(2020, 1, 1)) & (df['tpep_dropoff_datetime'] < pd.Timestamp(2020, 2, 1))]

# Convert timestamp columns to datetime for spliting purposes
new_df['tpep_dropoff_date'] = new_df['tpep_dropoff_datetime'].apply(lambda x: x.date())

# Check unique date after filtering falsy data (should be 31 days since January has 31 days)
print(len(new_df['tpep_dropoff_date'].unique()))

"""### Save clean data to csv"""

new_df.to_csv('yellow_tripdata_2020_Jan.csv')


"""### Split the data of January 2020 based on the date of the month"""
# set tpep_dropoff_date as the index column, this is the additional column created
dfd = pd.read_csv('yellow_tripdata_2020_Jan.csv', index_col='tpep_dropoff_date', parse_dates=True).iloc[:, 1:]

# Group by date
result = [group[1] for group in dfd.groupby(dfd.index.date)]

"""# Save csv files by date (could choose other format such as parquet)"""

for i in range(len(result)):
  result[i].to_csv('./data_by_date/yellow_tripdata_2020_Jan_{}.csv'.format(i+1))


"""# Load dataset to our db instance"""
from sqlalchemy import create_engine
engine = create_engine('mysql+pymysql://admin:duyenle1312@yellow-taxi.cwnrxwplws9a.us-east-1.rds.amazonaws.com/Jan2020')

import os
# Go to folder with data that is set in the saving files step
os.chdir("./data_by_date")

# Get current directory
curren_dir = os.listdir(os.getcwd())

# Loop through all files in the directory
for (index, filename) in enumerate(curren_dir, 1):
  # Print progress
  # print(filename)
  # Get full path
  filename_full = os.path.join(os.getcwd(), filename)
  # Read CSV file
  df = pd.read_csv(filename_full, index_col='tpep_dropoff_date', parse_dates=True)
  # Insert to database, if_exists="replace" => replace existing tables with new data
  df.to_sql("yellow_taxi_{}Jan".format(index), con=engine, if_exists="replace", index=False)