# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('drive/MyDrive/crashes.csv')

master_mapping = {
    "Sedan": 554471,
    "Station Wagon\/Sport Utility Vehicle": 436504,
    "PASSENGER VEHICLE": 416206,
    "SPORT UTILITY \/ STATION WAGON": 180291,
    "Taxi": 50170,
    "4 dr sedan": 40162,
    "Pick-up Truck": 33548,
    "TAXI": 31911,
    "VAN": 25266,
    "Box Truck": 23570,
    "OTHER": 22967,
    "Bus": 20525,
    "UNKNOWN": 19936,
    "LARGE COM VEH(6 OR MORE TIRES)": 14397,
    "Bike": 14120,
    "BUS": 13993,
    "SMALL COM VEH(4 TIRES) ": 13216,
    "nan": 12790,
    "PICK-UP TRUCK": 11505,
    "LIVERY VEHICLE": 10481,
    "Tractor Truck Diesel": 10033,
    "Van": 8702,
    "Motorcycle": 7724
}

mapping = {
    "MOTORCYCLE": "Motorcycle",
    "Ambulance": "Ambulance",   # Not in master, will use 'Ambulance'
    "Convertible": "Sedan",    # Assuming a Convertible is a type of Sedan
    "Dump": "Dump",            # Not in master, will use 'Dump'
    "E-Bike": "Bike",
    "2 dr sedan": "Sedan",
    "AMBULANCE": "Ambulance",  
    "PK": "PICK-UP TRUCK",  
    "Flat Bed": "Flat Bed",    # Not in master, will use 'Flat Bed'
    "Garbage or Refuse": "SMALL COM VEH(4 TIRES)",
    "E-Scooter": "Bike",      # E-Scooter not in master, categorizing as 'OTHER'
    "Carry All": "Station Wagon\/Sport Utility Vehicle",
    "Tractor Truck Gasoline": "Tractor Truck Diesel", 
    "Moped": "Motorcycle",     # Moped closely aligns with Motorcycle
    "Tow Truck \/ Wrecker": "OTHER",
    "FIRE TRUCK": "LARGE COM VEH(6 OR MORE TIRES)",
    "Chassis Cab": "Sedan",  
    "Tanker": "OTHER",         # Not specific in master, using 'OTHER'
    "Motorscooter": "Motorcycle",
    "BICYCLE": "Bike",
    "Concrete Mixer": "OTHER",
    "Motorbike": "Motorcycle",
    "Refrigerated Van": "Van",
    "van": "Van",
    "AMBUL": "Ambulance",
    "Flat Rack": "Flat Bed",
    "Armored Truck": "OTHER",
    "3-Door": "Sedan",         # Assuming 3-Door is a type of Sedan
    "Beverage Truck": "OTHER",
    "SCOOTER": "Bike",
    "LIMO": "LIMO",           # LIMO can be a specialized Sedan but marking as 'OTHER' for distinction
    "Lift Boom": "OTHER",
    "TRUCK": "OTHER",
    "School Bus": "Bus",
    "TRAIL": "OTHER",
    "Stake or Rack": "OTHER",
    "FIRE": "LARGE COM VEH(6 OR MORE TIRES)",
    "FDNY": "LARGE COM VEH(6 OR MORE TIRES)",
    "MOPED": "Motorcycle",
    "E-Sco": "E-Bike",
    "Snow Plow": "OTHER",
    "ambul": "Ambulance",
    "Multi-Wheeled Vehicle": "OTHER",
    "E-Bik": "E-Bike",
    "DUMP": "Dump",
    "TRACT": "OTHER",
    "Ambul": "Ambulance",
    "AMBU": "Ambulance",
    "Open Body": "OTHER",
    "USPS": "SMALL COM VEH(4 TIRES)",           # USPS might have different types of vehicles; marking as 'OTHER' for now
    "Bulk Agriculture": "OTHER",
    "UNKNO": "UNKNOWN",
    "ambulance": "Ambulance"
}

inv_mapping = {v: k for k, v in mapping.items()}

df['VEHICLE TYPE CODE 1'] = df['VEHICLE TYPE CODE 1'].replace(mapping)

filtered_mapping = {k: inv_mapping[k] for k in set(master_mapping.keys()).union(set(mapping.values())) if k in inv_mapping}

df = df[df['VEHICLE TYPE CODE 1'].isin(filtered_mapping.keys())]

print(df)

# Remove rows where any of the specified columns are missing
columns_to_check = ['BOROUGH', 'ZIP CODE', 'LATITUDE', 'LONGITUDE', 'LOCATION', 'ON STREET NAME', 'CROSS STREET NAME', 'OFF STREET NAME']
df_cleaned = df.dropna(subset=columns_to_check)

# Display the first few rows to understand the data
print(df.head())

# Count the occurrences of each vehicle type
vehicle_type_counts = df['VEHICLE TYPE CODE 1'].value_counts(dropna=False)

# Rename NaN values to "Unknown"
vehicle_type_counts = vehicle_type_counts.rename({pd.NA: 'Unknown'})

# Separate the counts based on the threshold of 5000
more_than_100 = vehicle_type_counts[vehicle_type_counts > 5000]
less_than_100 = vehicle_type_counts[vehicle_type_counts <= 5000].sort_values(ascending=False)

# Plotting for vehicle types with more than 5000 crashes
plt.figure(figsize=(20,6))
more_than_100.plot(kind='bar', color='seagreen')
plt.title('Vehicle Types with More than 5000 Crashes')
plt.ylabel('Number of Crashes')
plt.xlabel('Vehicle Type')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Print the dictionary
print(more_than_100.to_json())


# Print the dictionary
print(less_than_100.to_json())