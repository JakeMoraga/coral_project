import numpy as np
import seaborn as sns
import pandas as pd

#this uploads the data without the first row containing units so the data 
#starts in the first row and also only uses the columns that I want to look
#at which are coral cover and latitude
df = pd.read_csv('coral_forecast.csv', skiprows= [1],
usecols= ['coral_cover_2020', 'coral_cover_2100', 'latitude'])

#making sure that all the data is now a float type since they have decimal points
df['latitude']= df['latitude'].astype(float)
df['coral_cover_2020']= df['coral_cover_2020'].astype(float)
df['coral_cover_2100']= df['coral_cover_2100'].astype(float)
