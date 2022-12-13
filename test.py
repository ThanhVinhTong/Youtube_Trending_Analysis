import os
import pandas 

def list_file(path):
    filenames = os.listdir(path=path)
    for i in range(1, len(filenames)):
        print("data/" + filenames[i])

list_file("data")

os.path.join("data", '2022-11-28.csv')

pandas.read_csv("data/2022-12-13.csv")