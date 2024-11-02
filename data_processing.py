import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

#this uploads the data without the first row containing units so the data 
#starts in the first row and also only uses the columns that I want to look
#at which are coral cover and SST from 2020 and 2100 and latitude
df = pd.read_csv('Coral_Dataset/coral_forecast.csv', skiprows= [1],
usecols= ['coral_cover_2020', 'coral_cover_2100', 'latitude', 'SST_2020', 'SST_2100'])

#making sure that all the data is now a float type since they have decimal points
df['latitude']= df['latitude'].astype(float)
df['coral_cover_2020']= df['coral_cover_2020'].astype(float)
df['coral_cover_2100']= df['coral_cover_2100'].astype(float)
df['SST_2020'] = df['SST_2020'].astype(float)
df['SST_2100'] = df['SST_2100'].astype(float)

#Now I find the difference of coral cover as well as SST from the year 2020 to 2100 by 
#subtracting coral cover from 2100 from 2020
df['coral_cover_difference'] = df['coral_cover_2020'] - df['coral_cover_2100']
df['SST_difference'] = df['SST_2100'] - df['SST_2020']

#This arranges latitude which will be on the x-axis into bins ranging from -30 to 30 degrees
#and the bins categorized by 5
#The last part makes the bins left-inclusive and also creates simple labels for each bin 
# which makes it a lot easier and quicker to process
df['latitude_bin'] = pd.cut(df['latitude'], bins=np.arange(-30, 30, 5), 
right=False, labels=False)

#This is a copy of the above code but without the left incluse and labels for the catplot
#since these functions taken out don't generate a correct x-axis
df['latitude_bin_2'] = pd.cut(df['latitude'], bins=np.arange(-30, 30, 5)) 

#This ensures that if there are any duplicate rows in the df that they are dropped 
df.drop_duplicates(subset=['latitude_bin_2', 'coral_cover_2020', 'coral_cover_2100'], inplace=True)

#Similar to above with latitude but it categorizes SST_difference neatly to be used on the x-axis
#of the plot
df['SST_bin'] = pd.cut(df['SST_difference'], bins=np.arange(-5, 5.5, 0.5))

#I want to create a new dataframe for coral cover for the third plot with coral cover from
#both 2020 and 2100 but not the difference
#This copies coral_cover_2020 and latitude_bin so that they can be modified outside the main
#dataframe
df_2020 = df[['latitude_bin_2', 'coral_cover_2020']].copy()
df_2020['Year'] = '2020' #adds another column with the year to identify
df_2020.rename(columns={'coral_cover_2020': 'Coral Cover'}, inplace=True) #renames the copy to be 'Coral Cover'

#This chunk of code does the same thing but with the coral cover from 2100
df_2100 = df[['latitude_bin_2', 'coral_cover_2100']].copy()
df_2100['Year'] = '2100'
df_2100.rename(columns={'coral_cover_2100': 'Coral Cover'}, inplace=True)

#This code combines the new dfs for coral cover in 2020 and 2100 into one and also creates
#a new index where values are not duplicated which causes errors
df_coral = pd.concat([df_2020, df_2100], ignore_index=True)

#This groups the datapoints under coral_cover_difference into the different bins created
#and finds the average of each bin so that I can plot it
df_avg = df.groupby('latitude_bin')['coral_cover_difference'].mean().reset_index()

#This groups average coral cover again but pairs it up with the average SST difference rather 
#than latitude for the second graph
df_avg_2 = df.groupby('SST_bin').agg({'SST_difference': 'mean', 'coral_cover_difference': 'mean'}).reset_index()

#This creates a loop that goes through the range and creates the bins in increments of 5
bin_labels = [f"[{i}, {i+5})" for i in range(-30, 30, 5)]

#This creates a dictionary where the bin types are indexed with a value and then the 
#bins created from the dataset are assigned to the corresponding value
df_avg['latitude_bin'] = df_avg['latitude_bin'].map(dict(enumerate(bin_labels)))

#This makes the catplot with latitude on the x-axis and coral cover on the y
coral_difference_chart = sns.catplot(data=df_coral, x='latitude_bin_2', y='Coral Cover', hue='Year', kind='bar', height=6, aspect=2, palette='dark')
coral_difference_chart.set(xlabel='Latitude', ylabel='Average Coral Cover (km$^{2}$)') #Sets axis names
plt.title('Average Coral Cover in 2020 and 2100')
#Makes a caption for the figure, placing it below the x-axis and determining the size
plt.figtext(0.5, -0.25, 'This figure shows the average coral cover in 2020 and 2100 as a function of latitude.\n Latitude is shown on the x-axis in bins of five,\n ranging from -30 to 25. From this figure it is evident that average coral cover \nis much higher in the year 2020 than 2100', ha='center', fontsize=16)
plt.xticks(rotation=45)  # Makes the x-axis labels look fancy
plt.show()

#this makes the chart with latitude on the x axis and difference in coral cover on the y axis
#made sure to use df_avg now as the data and not just df since it has the averages sorted
cover_chart = sns.lineplot(data=df_avg, x='latitude_bin', y='coral_cover_difference')
sns.despine()  # Cleans up the chart by taking out part of the frame
cover_chart.set(xlabel='Latitude', ylabel='Average Coral Cover Loss (km$^{2}$)') #Sets axis names
plt.xticks(rotation=45)  # Makes the x-axis labels look fancy
#Makes a caption below the figure.
plt.figtext(0.5, -0.35, 'This figure shows the average coral cover loss between 2020 and 2100 \nas a function of latitude. Latitude is similarly binned by \nintervals of 5 on the x-axis as the above figure but the y-axis is average coral cover loss. \n From this figure it is evident that the largest loss of coral cover is in the [20,25] bin \n and that average cover loss fluctates with latitude', ha='center', fontsize=12)
plt.title('Predicted Change in Coral Cover From 2020 to 2100 in Relation to Latitude') #plot title name
plt.show() #shows me the chart

#This is very similar to the first chart but uses SST_difference for the x-axis instead of latitude
#and the correct data set for comparing the two
cover_chart_2 = sns.lineplot(data=df_avg_2, x='SST_difference', y='coral_cover_difference')
sns.despine()  # Cleans up the chart by taking out part of the frame
cover_chart_2.set(xlabel='Increase in SST (\u00B0C)', ylabel='Average Coral Cover Loss (km$^{2}$)') #Sets axis names
plt.xticks(rotation=45)  # Makes the x-axis labels look fancy
#Makes a caption below the figure.
plt.figtext(0.5, -0.25, 'This figure shows the average coral cover loss between 2020 and 2100 \n as a function of SST change. In this figure, the x-axis is \nnow change in SST and the y-axis remains the same as the above figure. \nLooking at this figure it is apparent that average coral cover loss is greatest between a \n1.5 and 2 degree celcius increase.', ha='center', fontsize=12)
plt.title('Predicted Change in Coral Cover From 2020 to 2100 in Relation to Increasing SST') #plot title name
plt.show() #shows me the chart
