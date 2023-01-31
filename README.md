# Youtube_Trending_Analysis
This is group project for introduction to data science

## Set-up
Install the following Python libraries:
- Google API Client: 
```
pip install google-api-python-client
```
- NumPy:
```
pip install numpy
```
- Pandas:
```
pip install pandas
```
- Matplotlib:
```
pip install matplotlib
```
- word_cloud:
```
pip install wordcloud
```

## Compile

Our project was written in Python. Therefore, no compilation is necessary.

## Run the program

```
python main.py ...PLOT CODE... [options]

e.g. python main.py 1 --crawl
```

### Options
```--crawl```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Enable crawling for data from Youtube trending tab. The data will be saved in folder *data* under the name *YYY-MM-DD.csv*.  
```--merge_files```
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Merges the files containing crawled data into one file and filters out invalid entries. The cleaned data is saved in folder *data* under the name *clean.csv*.

### Warning
- Deleting the *data* folder renders the program unusable.
- The merge_files.py file only merges our already crawled data. Deleting this data renders some files unusable. Any newly crawled data will not be taken into consideration.
