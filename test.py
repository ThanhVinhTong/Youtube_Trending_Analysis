import os
import pandas 
from datetime import datetime

str = ["2022-12-10T08:24:00Z", "2022-12-11T00:00:00Z"]
time = []
for date in str:
    day = date.split("T")[0]
    hour = (date.split("T")[1].split("Z"))[0]
    print(date)

    print(day, hour)
    date = day + " " + hour
    temp = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    time.append(temp)

print(str)

age = time[1]- time[0]

print(age.total_seconds())