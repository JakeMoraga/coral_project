import numpy as np
import seaborn as sns
import pandas as pd

#this uploads the data without the first row containing units so the data 
#starts in the first row and also only uses the columns that I want to look
#at which are coral cover and latitude
df = pd.read_csv('Coral_Dataset/coral_forecast.csv', skiprows= [1],
usecols= ['coral_cover_2020', 'coral_cover_2100', 'latitude'])

#making sure that all the data is now a float type since they have decimal points
df['latitude']= df['latitude'].astype(float)
df['coral_cover_2020']= df['coral_cover_2020'].astype(float)
df['coral_cover_2100']= df['coral_cover_2100'].astype(float)

#Now I find the difference of coral cover from the year 2020 to 2100 by subtracting coral cover
#from 2100 from 2020
df['coral_cover_difference'] = df['coral_cover_2020'] - df['coral_cover_2100']

#I want to represent the data in a bar chart so the best way to do that is make bins
#This arranges latitude which will be on the x-axis into bins ranging from -30 to 30 degrees
#and the bins categorized by 5
df['latitude_bin'] = pd.cut(df['latitude'], bins=np.arange(-30, 30, 5))

#This converts the new dataset "latitude_bin" to be in str format so that it can be used
#in the graph by being the right data type
df['latitude_bin'] = df['latitude_bin'].astype(str)

#This groups the datapoints under coral_cover_difference into the different bins created and finds
#the average of each bin so that I can plot it
df_avg = df.groupby('latitude_bin')['coral_cover_difference'].mean().reset_index()

#I want to see what my data looks like now
print(df)