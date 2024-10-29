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

#Now I find the difference of coral cover from the year 2020 to 2100 by subtracting 
#coral cover from 2100 from 2020
df['coral_cover_difference'] = df['coral_cover_2020'] - df['coral_cover_2100']

#I want to represent the data in a bar chart so the best way to do that is make bins
#This arranges latitude which will be on the x-axis into bins ranging from -30 to 30 degrees
#and the bins categorized by 5
#The last part makes the bins left-inclusive and also creates simple labels for each bin 
# which makes it a lot easier and quicker to process
df['latitude_bin'] = pd.cut(df['latitude'], bins=np.arange(-30, 30, 5), 
right=False, labels=False)

#This groups the datapoints under coral_cover_difference into the different bins created
#and finds the average of each bin so that I can plot it
df_avg = df.groupby('latitude_bin')['coral_cover_difference'].mean().reset_index()

#This creates a loop that goes through the range and creates the bins in increments of 5
bin_labels = [f"[{i}, {i+5})" for i in range(-30, 30, 5)]

#This creates a dictionary where the bin types are indexed with a value and then the 
#bins created from the dataset are assigned to the corresponding value
df_avg['latitude_bin'] = df_avg['latitude_bin'].map(dict(enumerate(bin_labels)))

#this makes the chart with latitude on the x axis and difference in coral cover on the y axis
#made sure to use df_avg now as the data and not just df since it has the averages sorted
cover_chart = sns.lineplot(data=df_avg, x='latitude_bin', y='coral_cover_difference')
sns.despine() #cleans up the chart by taking out part of the frame
#Lables the x and y axis
cover_chart.set(xlabel='Latitude', ylabel='Average coral cover (km$^{2}$)')
plt.xticks(rotation=45) #Makes the x-axis labels look fancy
plt.title('Average coral cover loss from 2020 to 2100 in relation to latitude')