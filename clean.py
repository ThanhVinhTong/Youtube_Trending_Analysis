import datetime
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

def merge(filenames):
	list_of_df = []
	for filename in filenames:
		current_df = pd.read_csv(filename, sep='\t')
		list_of_df.append(current_df)

	all_df = pd.concat(list_of_df)
	all_df.reset_index(drop=True, inplace=True)
	return all_df

def list_file(path):
    filenames = os.listdir( path = path )
    for i in range(1, len(filenames)):
        datasets_filenames.append("data/" + filenames[i])

def clean(dataset):
	clean_df = dataset.copy(deep=True)

    # Replace NaN in description with space
	clean_df["description"].fillna(" ", inplace=True)

    # Delete all rows with a missing values if any
	clean_df.dropna(inplace=True)

	# Change format of trending_date to discard crawl time
	# clean_df['trending_date'].mask(clean_df['trending_date'] == '2022-12-10T00:00:00Z','10/12/2022',inplace=True)
	
	# Correct negative values, if any
	for x in clean_df.index:
		clean_df.loc[x,'view_count'] = int(clean_df.loc[x,'view_count'])
		clean_df.loc[x,'likes'] = int(clean_df.loc[x,'likes'])
		clean_df.loc[x,'comment_count'] = int(clean_df.loc[x,'comment_count'])
		if clean_df.loc[x,'view_count'] < 0:
			clean_df.loc[x,'view_count'] = 0
		if clean_df.loc[x,'likes'] < 0:
			clean_df.loc[x,'likes'] = 0
		if clean_df.loc[x,'comment_count'] < 0 or clean_df.loc[x,'comments_disabled'] == True:
			clean_df.loc[x,'comment_count'] = 0


    # Rename some columns for uniformity
	clean_df.rename(columns={'channelTitle': 'channel_title',
			     'publishedAt': 'published_at',
			     'channelId': 'channel_id',
							 'categoryId' : 'category_id'}, inplace=True)

	# Create new empty column for the number of regions the video is trending in
	clean_df['notes'] = "1"

	# Add number of regions the video is trending to 'notes'
	dups = clean_df[clean_df.duplicated(subset=['video_id','trending_date'],keep=False)]	
	for x in dups.index:
		id = dups.loc[x,'video_id']
		date = dups.loc[x,'trending_date']
		temp = clean_df[(clean_df['video_id'] == id) & (clean_df['trending_date'] == date)]
		temp = len(temp.index)
		for i in clean_df.index:
			if clean_df['video_id'][i] == id and clean_df['trending_date'][i] == date:
				clean_df.loc[i,'notes'] = temp
				break

	# Drop duplicates
	clean_df.drop_duplicates(subset=['video_id','trending_date'],keep='first',inplace=True)
	
	clean_df = clean_df.reindex(columns=['video_id', 'title', 'published_at', 'channel_id', 'channel_title',
					 'category_id', 'trending_date', 'view_count', 'likes', 
										 'comment_count', 'comments_disabled', 'description', 'notes'])

	clean_df.reset_index(drop=True, inplace=True)

	return clean_df

def main():
	list_file(path = path)

	combined_df = merge(datasets_filenames)
	print(combined_df.shape)
	print(combined_df.columns)

	clean_df = clean(combined_df)

	print(clean_df.shape)
	print(clean_df.columns)
	clean_df.to_csv('data/clean.csv')