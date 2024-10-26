import numpy as np
import seaborn as sns
import pandas as pd

#this uploads the data without the first row containing the headers
coral_data = pd.read_csv('Datasets/coral_forecast.csv', skiprows=[1])