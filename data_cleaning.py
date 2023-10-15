# First Graphs# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('drive/MyDrive/crashes.csv')

# Remove rows where any of the specified columns are missing
columns_to_check = ['BOROUGH', 'ZIP CODE', 'LATITUDE', 'LONGITUDE', 'LOCATION', 'ON STREET NAME', 'CROSS STREET NAME', 'OFF STREET NAME']
df_cleaned = df.dropna(subset=columns_to_check)

# Display the first few rows to understand the data
print(df.head())

# Basic analysis: Number of crashes by Borough
borough_counts = df['BOROUGH'].value_counts()
borough_counts.plot(kind='bar', color='c')
plt.title('Number of Crashes by Borough')
plt.ylabel('Number of Crashes')
plt.xlabel('Borough')
plt.xticks(rotation=45)
plt.show()

# Analysis: Average number of persons injured by vehicle type
avg_injured_by_vehicle = df.groupby('VEHICLE TYPE CODE 1')['NUMBER OF PERSONS INJURED'].mean().sort_values(ascending=False).head(10)
avg_injured_by_vehicle.plot(kind='bar', color='m')
plt.title('Average Number of Persons Injured by Vehicle Type')
plt.ylabel('Average Number of Persons Injured')
plt.xlabel('Vehicle Type')
plt.xticks(rotation=45)
plt.show()

# Analysis: Distribution of crashes throughout the day
df['CRASH TIME'] = pd.to_datetime(df['CRASH TIME'])
df['Hour'] = df['CRASH TIME'].dt.hour
hourly_crashes = df['Hour'].value_counts().sort_index()
hourly_crashes.plot(kind='line', marker='o', color='b')
plt.title('Distribution of Crashes Throughout the Day')
plt.ylabel('Number of Crashes')
plt.xlabel('Hour of the Day')
plt.grid(True)
plt.show()