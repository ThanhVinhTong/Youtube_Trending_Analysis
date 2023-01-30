from datetime import datetime
import numpy as np
import pandas as pd
import os

REGIONS = ['US', 'GB', 'JP', 'KR', 'IN']
datasets_filenames = []
path = "data"
dates = []


def merge(filenames):
    list_of_df = []
    for filename in filenames:
        current_df = pd.read_csv(filename, sep='\t')
        list_of_df.append(current_df)

    all_df = pd.concat(list_of_df)
    all_df.reset_index(drop=True, inplace=True)
    return all_df


def list_file(path):
    filenames = os.listdir(path=path)
    for i in range(1, len(filenames)):
        dates.append(filenames[i])
        datasets_filenames.append("data/" + filenames[i])
    print(dates)


def convert_to_datetime(date, flag, i):
    day = date.split("T")[0]
    if(date[-1] != 'Z'):
        print("date:", date)
        print("flag:", flag)
        print("i=", i)
    hour = (date.split("T")[1].split("Z"))[0]
    if flag == 1:
        day = datetime.strptime(day, "%Y-%m-%d").strftime("%d-%m-%Y")

    date = day + " " + hour
    date = datetime.strptime(date, "%d-%m-%Y %H:%M:%S")

    return date


def get_video_age(published_date, trending_date, i):
    published_date = convert_to_datetime(published_date, 1, i)
    trending_date = convert_to_datetime(trending_date, 0, i)
    age = (trending_date-published_date).total_seconds()/3600
    return int(age)


def add_age_column(dataset):

    df = dataset.copy(deep=True)

    # get video age
    age = []
    for i in range(0, len(df)):
        temp = get_video_age(
            df['publishedAt'][i], df['trending_date'][i], i)
        age.append(temp)
    df['age'] = age

    return df


def add_rating_disabled_column(dataset):

    df = dataset.copy(deep=True)
    rating_disabled = []

    # get rating disabled
    for x in df.index:
        if df.loc[x, 'likes'] <= 0:
            rating_disabled.append(True)
        elif df.loc[x, 'likes'] > 0:
            rating_disabled.append(False)

    df['rating_disabled'] = rating_disabled

    return df


def read():
    return pd.read_csv("data/merged_files.csv")


def main():
    list_file(path=path)

    combined_df = merge(datasets_filenames)
    combined_df = add_age_column(combined_df)
    combined_df = add_rating_disabled_column(combined_df)

    print("Cleaned Data's shape: {}".format(combined_df.shape))
    print("Cleaned Data's Attributes: {}".format(combined_df.columns))
    combined_df.to_csv('data/merged_files.csv')
