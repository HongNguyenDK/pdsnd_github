# Bike Sharing

> Python program to view statistics for bike sharing.

### Date created

Repo created on 12 Nov 2023

### Description

See statistics for bike sharing data. The program can read data from one of three files (must be provided by you):

- chicago.csv
- new_york_city.csv
- washington.csv

The schemas of these CSV files:

```
Data columns (total 9 columns):
 #   Column         Non-Null Count   Dtype  
---  ------         --------------   -----  
 0   ID             187645 non-null  int64  
 1   Start Time     187645 non-null  object 
 2   End Time       187645 non-null  object 
 3   Trip Duration  187645 non-null  int64  
 4   Start Station  187645 non-null  object 
 5   End Station    187645 non-null  object 
 6   User Type      187645 non-null  object 
 7   Gender         149658 non-null  object 
 8   Birth Year     149679 non-null  float64
dtypes: float64(1), int64(2), object(6)
memory usage: 12.9+ MB
```

### How to use

Run the program like this:

```bash
python bikeshare.py
```

### Files used

To use the project you need to download csv files for bike data.

### Credits

The idea for this repository came from the Udacity course "Programming for Data Science in Python".

