from datetime import datetime
import numpy as np
import pandas as pd
import os

"""
Data preprocessing steps:
1. Integrate all data files into 1 combined dataframe.
2. Replace all NaN in video description(videos without a description).
3. Delete all records with a missing value.
4. Change format of trending_date from original YouTube API standard(%Y-%m-%dT%H:%M:%SZ) to a more familiar format(%d/%m/%Y).
5. Delete all records with its ratings disabled(videos with like and dislike 
buttons disabled).
6. Correct wrong numbers in likes/dislikes/view_count/comments_count.
7. Rename some columns for uniformity(channelTitle -> channel_title; publishedAt -> published_at; categoryId -> category_id).
8. Delete irrelevant column(ratings_disabled).
9. Create a new column ‘notes’ to hold new values.
10. Add the number of regions the video is trending in to ‘notes’.
11. Drop duplicate records.
12. Reset index for dataframe.
"""

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


def clean(dataset):
    clean_df = dataset.copy(deep=True)

    clean_df.info()

    # Replace NaN in description with space
    clean_df["description"].fillna(" ", inplace=True)

    # Delete all rows with a missing values if any
    clean_df.dropna(inplace=True)

    print(len(clean_df))

    # get video age
    age = []
    for i in range(0, len(clean_df)):
        temp = get_video_age(
            clean_df['publishedAt'][i], clean_df['trending_date'][i], i)
        age.append(temp)
    clean_df['age'] = age

    # Correct negative values, if any
    for x in clean_df.index:
        clean_df.loc[x, 'view_count'] = int(clean_df.loc[x, 'view_count'])
        clean_df.loc[x, 'likes'] = int(clean_df.loc[x, 'likes'])
        clean_df.loc[x, 'comment_count'] = int(
            clean_df.loc[x, 'comment_count'])
        if clean_df.loc[x, 'view_count'] < 0:
            clean_df.loc[x, 'view_count'] = 0
        if clean_df.loc[x, 'likes'] < 0:
            clean_df.loc[x, 'likes'] = 0
        if clean_df.loc[x, 'comment_count'] < 0 or clean_df.loc[x, 'comments_disabled'] == True:
            clean_df.loc[x, 'comment_count'] = 0

    # Rename some columns for uniformity
    clean_df.rename(columns={'channelTitle': 'channel_title',
                             'publishedAt': 'published_at',
                             'channelId': 'channel_id',
                             'categoryId': 'category_id'}, inplace=True)

    # Create new empty column for the number of regions the video is trending in
    clean_df['notes'] = "1"

    # Add number of regions the video is trending to 'notes'
    dups = clean_df[clean_df.duplicated(
        subset=['video_id', 'published_at'], keep=False)]
    for x in dups.index:
        id = dups.loc[x, 'video_id']
        date = dups.loc[x, 'published_at']
        temp = clean_df[(clean_df['video_id'] == id) &
                        (clean_df['published_at'] == date)]
        temp = len(temp.index)
        for i in clean_df.index:
            if clean_df['video_id'][i] == id and clean_df['published_at'][i] == date:
                clean_df.loc[i, 'notes'] = temp
                break

    # Drop duplicates
    clean_df.drop_duplicates(
        subset=['video_id', 'published_at'], keep='first', inplace=True)

    # Add "temperature" column
    clean_df['temperature'] = (clean_df['view_count']/clean_df['age']).round(0)

    # Reindex columns 
    clean_df = clean_df.reindex(columns=['video_id', 'title', 'published_at', 'channel_id', 'channel_title',
                                         'category_id', 'trending_date', 'view_count', 'likes',
                                         'comment_count', 'comments_disabled', 'description', 'notes', 'age', 'temperature'])

    clean_df.reset_index(drop=True, inplace=True)

    return clean_df


def read():
    return pd.read_csv("data/clean.csv")


def main():
    list_file(path=path)

    combined_df = merge(datasets_filenames)

    clean_df = clean(combined_df)

    print("Cleaned Data's shape: {}".format(clean_df.shape))
    print("Cleaned Data's Attributes: {}".format(clean_df.columns))
    clean_df.to_csv('data/clean.csv')
