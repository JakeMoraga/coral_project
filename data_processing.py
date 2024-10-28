import numpy as np
import seaborn as sns
import pandas as pd

#this uploads the data without the first row containing units so the data 
#starts in the first row and also only uses the columns that I want to look
#at which are coral cover and latitude
main_df = pd.read_csv('coral_project/Coral_Dataset/coral_forecast.csv', skiprows= [1],
usecols= ['coral_cover_2020', 'coral_cover_2100', 'latitude'])
