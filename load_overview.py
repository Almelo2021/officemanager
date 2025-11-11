import glob
import pandas as pd
import numpy as np
import math
import streamlit as st
import os, shutil
#from generandom import generate_csv_files_based_on_template
import altair as alt
import random
import genebait
from genebait import generate_dataframes_based_on_template

additionalHoursLocal = {}

removeifbelow = 20
addifabove = 80

parts = {
    "BowOne": {
        'Glazen bovenpaneel': 3,
        'Glazen onderpaneel': 3,
        'Hoekstaander': 4,
        'Omkeerbaar kozijn': 1,
        'Glazen deur': 1,
        'Dakpaneel sensor + spot': 1,
        'Duco + ombouw + buizen - Geen sensor': 1,
        'instellen van Duco': 1,
        'Schap': 1,
        'Schaphaakset': 1,
        'Inhangkoker': 2,
        'Bevestigingsplaatje inhangkoker': 2,
        'Dekplaat onder': 2,
        'Dekplaat boven': 2,
        'Akoestiek boven': 2,
        'Akoestiek onder': 2,
        'opzetbox met aansluitkabel': 1,
        'Stekkerdoos': 1,
        'installatieset': 1
    },
    "BowTwo": {
        'Glazen bovenpaneel': 5,
        'Glazen onderpaneel': 5,
        'Hoekstaander': 4,
        'Doorkoppelpaal': 2,
        'Omkeerbaar kozijn': 1,
        'Glazen deur': 1,
        'Dakpaneel sensor + spot': 1,
        'Dakpaneel spot': 1,
        'Dakbalk 1200': 1,
        'Duco + ombouw + buizen': 1,
        'Inhangkoker': 2,
        'Bevestigingsplaatje inhangkoker': 2,
        'Dekplaat onder': 2,
        'Dekplaat boven': 2,
        'Akoestiek boven': 2,
        'Powercube': 1,
        'Akoestiek onder': 2,
        'opzetbox met aansluitkabel': 1,
        'Stekkerdoos': 1,
        'installatieset': 1
        },
    "BowFour": {
        'Glazen bovenpaneel': 7,
        'Glazen onderpaneel': 7,
        'Hoekstaander': 4,
        'Doorkoppelpaal': 4,
        'Omkeerbaar kozijn': 1,
        'Glazen deur': 1,
        'Dakpaneel sensor + spot': 1,
        'Dakpaneel spot': 3,
        'Dakbalk 1200': 2,
        'Dakbalk 2400': 1,
        'Duco + ombouw + buizen': 1,
        'Inhangkoker': 2,
        'Bevestigingsplaatje inhangkoker': 2,
        'Dekplaat onder': 4,
        'Dekplaat boven': 4,
        'Akoestiek boven': 4,
        'Akoestiek onder': 4,
        'Powercube': 1,
        'Stekkerdoos': 1,
        'installatieset': 1
    },
    "BowSix": {
        'Glazen bovenpaneel': 9,
        'Glazen onderpaneel': 9,
        'Hoekstaander': 4,
        'Doorkoppelpaal': 6,
        'Omkeerbaar kozijn': 1,
        'Glazen deur': 1,
        'Dakpaneel sensor + spot': 1,
        'Dakpaneel spot': 5,
        'Dakbalk 1200': 3,
        'Dakbalk 2400': 2,
        'Duco + ombouw + buizen': 1,
        'Inhangkoker': 2,
        'Bevestigingsplaatje inhangkoker': 2,
        'Dekplaat onder': 4,
        'Dekplaat boven': 4,
        'Akoestiek boven': 4,
        'Akoestiek onder': 4,
        'Powercube': 1,
        'Stekkerdoos': 1,
        'installatieset': 1
    },
    "BowNine": {
        'Glazen bovenpaneel': 11,
        'Glazen onderpaneel': 11,
        'Hoekstaander': 4,
        'Doorkoppelpaal': 8,
        'Omkeerbaar kozijn': 1,
        'Glazen deur': 1,
        'Dakpaneel sensor + spot': 1,
        'Dakpaneel spot': 8,
        'Dakbalk 1200': 6,
        'Dakbalk 3600': 2,
        'Duco + ombouw + buizen': 1,
        'Inhangkoker': 2,
        'Bevestigingsplaatje inhangkoker': 2,
        'Dekplaat onder': 6,
        'Dekplaat boven': 6,
        'Akoestiek boven': 6,
        'Akoestiek onder': 6,
        'Powercube': 1,
        'Stekkerdoos': 1,
        'installatieset': 1
    },
    "BowTwelve": {
        'Glazen bovenpaneel': 13,
        'Glazen onderpaneel': 13,
        'Hoekstaander': 4,
        'Doorkoppelpaal': 10,
        'Omkeerbaar kozijn': 1,
        'Glazen deur': 1,
        'Dakpaneel sensor + spot': 1,
        'Dakpaneel spot': 11,
        'Dakbalk 1200': 8,
        'Dakbalk 3600': 3,
        'Duco + ombouw + buizen': 1,
        'Inhangkoker': 2,
        'Bevestigingsplaatje inhangkoker': 2,
        'Dekplaat onder': 6,
        'Dekplaat boven': 6,
        'Akoestiek boven': 6,
        'Akoestiek onder': 6,
        'Powercube': 1,
        'Stekkerdoos': 1,
        'installatieset': 1
        }
}

dealerprices = {
    'Glazen bovenpaneel': '€285',
    'Glazen onderpaneel': '€245',
    'Hoekstaander': '€110',
    'Omkeerbaar kozijn': '€380',
    'Glazen deur': '€555',
    'Dakpaneel sensor + spot': '€275',
    'Duco + ombouw + buizen - Geen sensor': '€370',
    'instellen van Duco': '€0',
    'Schap': '€35',
    'Schaphaakset': '€20',
    'Inhangkoker': '€45',
    'Bevestigingsplaatje inhangkoker': '€5',
    'Dekplaat onder': '€55',
    'Dekplaat boven': '€100',
    'Akoestiek boven': '€75',
    'Akoestiek onder': '€45',
    'opzetbox met aansluitkabel': '€70',
    'Stekkerdoos': '€20',
    'installatieset': '€25',
    'Doorkoppelpaal': '€100',
    'Dakpaneel spot': '€255',
    'Dakbalk 1200': '€20',
    'Duco + ombouw + buizen': '€745',
    'Powercube': '€55',
    'Dakbalk 2400': '€45',
    'Dakbalk 3600': '€45'
    }

locofint = {}
cumulative_occupancy_frequency = {}
weekday_occupancy_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}  # Monday=0, Tuesday=1, ..., Sunday=6
total_intervals = 0
interval_occupancy_data = {}
data_rows = []

def get_max_occupancy(start_time, end_time, df):
    mask = (df['received_at'] >= start_time) & (df['received_at'] < end_time)
    filtered_df = df.loc[mask, 'people_counter_all']
    return 0 if filtered_df.empty else filtered_df.max()

def getdays(erin, dataframes, month, include_weekends=False):
    print("Transforming ",erin)
    try:
        df = pd.read_csv(erin)
    except Exception as error:
        print("svennnnx,",error)
        df = dataframes[erin]
    df['received_at'] = pd.to_datetime(df['received_at'])
    # Find the maximum date in the 'received_at' column
    max_date = df['received_at'].max()

    # Calculate the date 30 days before the maximum date
    start_date = max_date - pd.Timedelta(days=30*month)

    # Filter the DataFrame to only include rows from the last 30 days
    df = df[df['received_at'] >= start_date]
    df['date'] = df['received_at'].dt.date

        # Determine the day of the week for each date (Monday=0, Sunday=6)
    if include_weekends:
        days = df['date'].nunique()
        #st.write("YESWEEKENDS DAYS",days)

    else:
        df['weekday'] = df['received_at'].dt.weekday

        # Filter for weekdays (Monday through Friday) and count unique dates
        days = df[df['weekday'].between(0, 4)]['date'].nunique()

    return days

def transformMOS(erin, eruit, additionalHours, subtractHours, room_type, locView, locToRem, dataframes, bear, month, include_weekends):
    print("Transforming ",erin)
    global total_intervals
    global interval_occupancy_data
    global weekday_occupancy_counts
    global data_rows
    try:
        build = erin.name.split('#')[2]
        conf = erin.name.split('#')[3]
    except:
        build = erin.split('#')[2]
        conf = erin.split('#')[3]
    if bear is "random":
        df = dataframes[erin]
    else:
        erin.seek(0)
        df = pd.read_csv(erin)
        
    df['received_at'] = pd.to_datetime(df['received_at'])

    # Find the maximum date in the 'received_at' column
    max_date = df['received_at'].max()

    # Calculate the date 30 days before the maximum date
    start_date = max_date - pd.Timedelta(days=30*month)

    # Filter the DataFrame to only include rows from the last 30 days
    df = df[df['received_at'] >= start_date]

    if not include_weekends:
        #st.write("Excluding Weekend Data...")
        # Filter out weekends: keep only rows where day of the week is less than 5 (Monday=0, Tuesday=1, ..., Friday=4)
        df = df[df['received_at'].dt.dayofweek < 5]

    df['date'] = df['received_at'].dt.date

    df['weekday'] = df['received_at'].dt.dayofweek  # Extract the weekday

    # Update weekday_occupancy_counts with the number of occupancies for each weekday
    for weekday, count in df.groupby('weekday').size().items():
        weekday_occupancy_counts[weekday] += count

    intervals_df = pd.DataFrame()

    for single_date in pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='D'):
        datetime_range = pd.date_range(start=pd.Timestamp(single_date).replace(hour=8, minute=0),
                                       end=pd.Timestamp(single_date).replace(hour=18, minute=0),
                                       freq='30T')
        temp_df = pd.DataFrame({'DateTime': datetime_range, 'Occupancy': np.nan})
        intervals_df = pd.concat([intervals_df, temp_df], ignore_index=True)

        total_intervals += len(datetime_range)

    for i, row in intervals_df.iterrows():
        intervals_df.at[i, 'Occupancy'] = get_max_occupancy(row['DateTime'], row['DateTime'] + pd.Timedelta(minutes=30), df)

    for i, row in intervals_df.iterrows():
        interval = str(row['DateTime'])  # Convert interval timestamp to string for dictionary key
        occupancy = row['Occupancy']  # Directly use the 'Occupancy' column value for this interval

        # Check if this interval is already in the aggregation structure
        if interval in interval_occupancy_data:
            interval_occupancy_data[interval].append(occupancy)
        else:
            interval_occupancy_data[interval] = [occupancy]
    
    print(intervals_df)
    print("aha")
    intervals_df['Occupancy'].fillna(0, inplace=True)
    intervals_df.to_csv(eruit, index=False)
    name = build + " " + conf.replace(".csv","")
    conftype = conf.split("-")[0]
    if conftype == "BowOne":
        maxpos = 1
    elif conftype == "BowTwo":
        maxpos = 1
    elif conftype == "BowFour":
        maxpos = 4
    elif conftype == "BowSix":
        maxpos = 6
    elif conftype == "BowNine":
        maxpos = 6
    elif conftype == "BowTwelve":
        maxpos = 8
    newrow = analyze_mos_file(eruit, name, maxpos)
    data_rows.append(newrow)

    occupancy_frequency = intervals_df['Occupancy'].value_counts().to_dict()

    for occupancy_level, count in occupancy_frequency.items():
        if occupancy_level > 0:  # Assuming you want to start at 1 occupant
            if occupancy_level in cumulative_occupancy_frequency:
                cumulative_occupancy_frequency[occupancy_level] += count
            else:
                cumulative_occupancy_frequency[occupancy_level] = count

    #print("Occupancy Frequencies:", occupancy_frequency)
    #st.write(occupancy_frequency)
    if occupancy_frequency:
        highest_occupancy = max(occupancy_frequency.keys())
        #st.write(f"Highest Recorded Occupancy: {highest_occupancy}")
    else:
        print("No occupancy records found.")

    # Assuming occupancy_frequency is a dictionary like {1: count1, 2: count2, ...}
    total_occupancies = sum(occupancy_frequency.values())  # Calculate total number of occupancy records

    # Calculate percentage for each occupancy level
    occupancy_percentage = {occupant: (count / total_occupancies) * 100 for occupant, count in occupancy_frequency.items()}

    # Now occupancy_percentage will look something like {1: 20%, 2: 15%, ...}
    # You can print it out or use it as needed
    #st.write("Occupancy Percentages:", occupancy_percentage)

    # Filter out zero occupancy since we're interested in when the room is occupied
    occupied_occupancy_frequency = {k: v for k, v in occupancy_frequency.items() if k != 0}

    # Calculate the weighted sum of occupants (each level multiplied by its count)
    weighted_sum_occupants = sum(occupant * count for occupant, count in occupied_occupancy_frequency.items())

    # Calculate total number of occupied records
    total_occupied = sum(occupied_occupancy_frequency.values())

    # Calculate the average number of occupants when occupied
    if total_occupied > 0:  # To avoid division by zero
        average_occupied = weighted_sum_occupants / total_occupied
        #st.write(f"Average Number of Occupants When Occupied: {average_occupied:.2f}")
    else:
        print("No occupied records found.")

    num_rows_non_zero = (intervals_df['Occupancy'] > 0).sum()
    percentage_non_zero = (num_rows_non_zero / len(intervals_df)) * 100
    st.write(f"Processing {name}")
    print(f"Percentage of intervals where Occupancy is not 0: {percentage_non_zero:.2f}%")

    previous_occupancy = None  # Initialize a variable to hold the occupancy of the previous interval
    
    if percentage_non_zero > addifabove or percentage_non_zero < removeifbelow:
        #print("sven")
        for occupancy in intervals_df['Occupancy']:
            if occupancy == 1:
                if previous_occupancy is not None:  # Check if there is a previous occupancy to print
                    print(f"Previous occupancy: {previous_occupancy}")
                    if previous_occupancy == 0:
                        additionalHours['BowOne'] += 1
                        if 'BowOne' in additionalHoursLocal[build]:
                            additionalHoursLocal[build]['BowOne'] += 1
                        else:
                            additionalHoursLocal[build]['BowOne'] = 1
                    elif previous_occupancy == 1:
                        additionalHours['BowTwo'] += 1
                        if 'BowOne' in additionalHoursLocal[build]:
                            additionalHoursLocal[build]['BowTwo'] += 1
                        else:
                            additionalHoursLocal[build]['BowTwo'] = 1
                    else:
                        additionalHours['BowOne'] += 1
                        if 'BowOne' in additionalHoursLocal[build]:
                            additionalHoursLocal[build]['BowOne'] += 1
                        else:
                            additionalHoursLocal[build]['BowOne'] = 1
            elif occupancy == 2:
                additionalHours['BowTwo'] += 1
                if 'BowTwo' in additionalHoursLocal[build]:
                    additionalHoursLocal[build]['BowTwo'] += 1
                else:
                    additionalHoursLocal[build]['BowTwo'] = 1
            elif occupancy == 3:
                additionalHours['BowFour'] += 1
                if 'BowFour' in additionalHoursLocal[build]:
                    additionalHoursLocal[build]['BowFour'] += 1
                else:
                    additionalHoursLocal[build]['BowFour'] = 1
            elif occupancy in [4, 5]:
                additionalHours['BowSix'] += 1
                if 'BowSix' in additionalHoursLocal[build]:
                    additionalHoursLocal[build]['BowSix'] += 1
                else:
                    additionalHoursLocal[build]['BowSix'] = 1
            elif occupancy == 6:
                additionalHours['BowNine'] += 1
                if 'BowNine' in additionalHoursLocal[build]:
                    additionalHoursLocal[build]['BowNine'] += 1
                else:
                    additionalHoursLocal[build]['BowNine'] = 1
            elif occupancy in [7, 8]:
                additionalHours['BowTwelve'] += 1
                if 'BowTwelve' in additionalHoursLocal[build]:
                    additionalHoursLocal[build]['BowTwelve'] += 1
                else:
                    additionalHoursLocal[build]['BowTwelve'] = 1

        previous_occupancy = occupancy  # Update the previous occupancy for the next iteration
        # Update subtractHours based on room type
        room_key = room_type
        uniqLoc = build+"$"+room_type
        print("Molly & Percocet", uniqLoc, percentage_non_zero)
        locToRem[build][room_type] += 1
        if room_key in subtractHours:
            subtractHours[room_key] += 1
        if uniqLoc in locView:
            locView[uniqLoc] += 1
        else:
            locView.update({uniqLoc: 1})


def price_to_float(price_str):
    return float(price_str.replace('€', '').replace(',', '.'))


def analyze_mos_file(mos_file, name, maxpos):
    # Load data
    df = pd.read_csv(mos_file)
    print(df)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df['date'] = df['DateTime'].dt.date

    # Compute total and non-zero occupancy intervals
    total_intervals = len(df)
    non_zero_intervals = df[df['Occupancy'] > 0]
    print(non_zero_intervals)
    num_non_zero_occupancies = len(non_zero_intervals)
    occupancy_percentage = (num_non_zero_occupancies / total_intervals) * 100

    # Average occupancy when in use
    average_occupancy = non_zero_intervals['Occupancy'].mean()

    max_occupancy = non_zero_intervals['Occupancy'].max()

    # Exclusive occupancies for 1-8 Persons calculated from non-zero intervals
    exclusive_occupancies = {}
    cumulative_percentages = {}
    total_non_zero_intervals = len(non_zero_intervals)
    cumulative_percentage = 0
    for i in range(1, 9):  # From 1 to 8 persons
        print("sveeeeen ",name, i, total_non_zero_intervals)
        exclusive_occupancies[i] = non_zero_intervals[non_zero_intervals['Occupancy'] == i].shape[0] / total_non_zero_intervals * 100
        cumulative_percentage += exclusive_occupancies[i]
        cumulative_percentages[i] = cumulative_percentage

    # Build the row for this file
    row = {
        'Configurations': name,
        'Occupancy Space': f"{occupancy_percentage:.2f}%",
        'Max possible numerical occupancy': int(maxpos),
        'Average Occupancy When In Use': f"{average_occupancy:.2f}",
        'Max Occupancy': int(max_occupancy)
    }
    row.update({f'Cumulative Occupancy {i} Persons': f"{cumulative_percentages[i]:.2f}%" for i in range(1, 9)})


    return row

def load_data_overview(file_list, month, include_weekends=False):
    global data_rows
    data_rows = [] 
    global additionalHoursLocal
    additionalHoursLocal = {}
    if file_list == "random":
        #file_list = glob.glob('datas/*')
        file_list = generate_dataframes_based_on_template(template_path='mossom.csv')
        st.write(f"Number of Simulated Rooms to generate: {len(file_list)}")
        bear = "random"
    else:
        bear = "files"
    room_type_frequency = {}
    locations = {}
    additionalHours = {
        'BowOne': 0,
        'BowTwo': 0,
        'BowFour': 0,
        'BowSix': 0,
        'BowNine': 0,
        'BowTwelve': 0
    }
    subtractHours = {
        'BowOne': 0,
        'BowTwo': 0,
        'BowFour': 0,
        'BowSix': 0,
        'BowNine': 0,
        'BowTwelve': 0
    }
    buildings = []
    locView = {}
    quoteSet = {}
    roundDowns = {}
    roundOffs = {}
    locToRem = {}
    finalSetup = {}

    # List all files matching the pattern

    # Initialize total_present_parts dictionary
    total_present_parts_initial = {}
    total_present_parts_adjusted = {}
    parts_changes = {}
    
    for file_path in file_list:
        print(file_path)
        try:
            path_parts = file_path.name.split('#')
        except:
            path_parts = file_path.split('#')
        country, city, building, room_file = path_parts
        buildings.append(building)

    for gebouw in buildings:
        additionalHoursLocal.update({gebouw: {}})
        quoteSet.update({gebouw: {
        'BowOne': 0,
        'BowTwo': 0,
        'BowFour': 0,
        'BowSix': 0,
        'BowNine': 0,
        'BowTwelve': 0
    }})
        roundDowns.update({gebouw: {
        'BowOne': 0,
        'BowTwo': 0,
        'BowFour': 0,
        'BowSix': 0,
        'BowNine': 0,
        'BowTwelve': 0
    }})
        roundOffs.update({gebouw: {
        'BowOne': 0,
        'BowTwo': 0,
        'BowFour': 0,
        'BowSix': 0,
        'BowNine': 0,
        'BowTwelve': 0
    }})
        locToRem.update({gebouw: {
        'BowOne': 0,
        'BowTwo': 0,
        'BowFour': 0,
        'BowSix': 0,
        'BowNine': 0,
        'BowTwelve': 0
    }})
        finalSetup.update({gebouw: {
        'BowOne': 0,
        'BowTwo': 0,
        'BowFour': 0,
        'BowSix': 0,
        'BowNine': 0,
        'BowTwelve': 0
    }})
    
    print(roundDowns)

    for file_path in file_list:
        try:
            path_parts = file_path.name.split('#')
        except:
            path_parts = file_path.split('#')
        country, city, building, room_file = path_parts
        room_type = room_file.split('-')[0]

        room_type_frequency.setdefault(room_type, 0)
        room_type_frequency[room_type] += 1

        locations.setdefault(building, [])
        locations[building].append(room_type)
        finalSetup[building][room_type] += 1

        #print(building)
        #print(room_type)
        days = getdays( file_path, file_list, month, include_weekends)
        transformMOS(file_path, 'mossom.csv', additionalHours, subtractHours, room_type, locView, locToRem, file_list, bear, month, include_weekends)

    print("Locations",locations)
    print("locView",locView)

    ordered_keys = ['BowOne', 'BowTwo', 'BowFour', 'BowSix', 'BowNine', 'BowTwelve']
    hours = 8
    st.write(days,"Days")
    total_hours = days*hours
    capacity_needed = total_hours*0.75
    print("Total Hours & Capacity Needed", total_hours, capacity_needed)


    for key in additionalHours:
        additionalHours[key] /= 2
        print(key, additionalHours[key])

    for key in additionalHoursLocal:
        for keykey in additionalHoursLocal[key]:
            additionalHoursLocal[key][keykey] /= 2

    # Divide every value in additionalHours by total_hours and round up
    for key in additionalHours:
        print("additionalHours",key,additionalHours[key],capacity_needed)
        additionalHours[key] = math.ceil(additionalHours[key] / capacity_needed)
    
    #print("Room Type Frequencies:", room_type_frequency)
    print("Additional Hours to Reconfigure:", additionalHours)
    print("local",additionalHoursLocal)

    addSet = {'BowOne': 0, 'BowTwo': 0, 'BowFour': 0, 'BowSix': 0, 'BowNine': 0, 'BowTwelve': 0}

    for key in additionalHoursLocal:
        addSet['BowOne'] += additionalHoursLocal[key].get('BowOne', 0)
        addSet['BowTwo'] += additionalHoursLocal[key].get('BowTwo', 0)
        addSet['BowFour'] += additionalHoursLocal[key].get('BowFour', 0)
        addSet['BowSix'] += additionalHoursLocal[key].get('BowSix', 0)
        addSet['BowNine'] += additionalHoursLocal[key].get('BowNine', 0)
        addSet['BowTwelve'] += additionalHoursLocal[key].get('BowTwelve', 0)

    print("addSet",addSet)

    for build in additionalHoursLocal:
        print(build)
        for bow in additionalHoursLocal[build]:
            bowval = additionalHoursLocal[build][bow]
            print("bow bowval",bow,bowval)
            quote = bowval / ( addSet[bow] / additionalHours[bow])
            print("quote",quote)
            quoteSet[build][bow] = quote
            rounddown = math.floor(quote)
            print(rounddown)
            roundDowns[build][bow] = rounddown
            roundoff = quote-rounddown
            roundOffs[build][bow] = roundoff

    rankedRoundOffs = {}

    quoteSums = {}
    roundSums = {}
    deltaSet = {}

    # Initialize quoteSums for each Bow with 0
    for key in quoteSet[next(iter(quoteSet))]:
        quoteSums[key] = 0

    # Iterate over each top-level key and nested dictionary
    for nested_dict in quoteSet.values():
        for key, value in nested_dict.items():
            quoteSums[key] += value  # Add the value to the corresponding sum

    # quoteSums now contains the total for each Bow
    print("quoteSums",quoteSums)

    # Initialize quoteSums for each Bow with 0
    for key in roundDowns[next(iter(roundDowns))]:
        roundSums[key] = 0

    # Iterate over each top-level key and nested dictionary
    for nested_dict in roundDowns.values():
        for key, value in nested_dict.items():
            roundSums[key] += value  # Add the value to the corresponding sum

    # quoteSums now contains the total for each Bow
    print("roundSums",roundSums)

    # Initialize quoteSums for each Bow with 0
    for key in quoteSet[next(iter(quoteSet))]:
        deltaSet[key] = quoteSums[key] - roundSums[key]

    # quoteSums now contains the total for each Bow
    print("deltaSet",deltaSet)
    
    for bow_key in roundOffs[next(iter(roundOffs))]:
        temp_dict = {}

        # Gather values for this 'Bow' key from each top-level key
        for top_level_key, nested_dict in roundOffs.items():
            temp_dict[top_level_key] = nested_dict[bow_key]

        # Sort the temporary dictionary by its values in descending order, excluding zeros
        sorted_temp_dict = sorted([(k, v) for k, v in temp_dict.items() if v != 0], key=lambda item: item[1], reverse=True)

        # Assign ranks based on sorted order, excluding zeros
        rank = 1
        prev_value = None
        for top_level_key, value in sorted_temp_dict:
            if value != prev_value:
                prev_value = value
                temp_dict[top_level_key] = rank
                rank += 1
            else:
                temp_dict[top_level_key] = rank - 1

        # Assign the lowest possible rank to zeros
        lowest_rank = len(temp_dict)
        for top_level_key, value in temp_dict.items():
            if value == 0:
                temp_dict[top_level_key] = lowest_rank

        # Update the rankedRoundOffs with the ranks for this 'Bow' key
        rankedRoundOffs[bow_key] = temp_dict

    for locatie in roundOffs:
        #print("locatie",locatie)
        for spac in roundOffs[locatie]:
            space = roundOffs[locatie][spac]
            print("spac",spac,space)
            #code voor als rounddown kleiner is dan rankedroundoff
            if deltaSet[spac] < rankedRoundOffs[spac][locatie]:
                fakka = 5
            else:
                roundDowns[locatie][spac] += 1
                print("Addition +1 ",locatie," ",spac)

    firstSetup = finalSetup

    for hold in finalSetup:
        print("Gebouw",hold)
        for stud in finalSetup[hold]:
            print("stud",finalSetup[hold])
            print("roundDown",hold,stud, roundDowns[hold][stud])
            print("locToRem",hold,stud, locToRem[hold][stud])
            if roundDowns[hold][stud] - locToRem[hold][stud] != 0:
                print("WAAAAAATTTT ", roundDowns[hold][stud], locToRem[hold][stud])
            studio = finalSetup[hold][stud] + roundDowns[hold][stud] - locToRem[hold][stud]
            finalSetup[hold][stud] = finalSetup[hold][stud] + roundDowns[hold][stud] - locToRem[hold][stud]
            print("hold",stud,studio)
    
    print("quoteSet",quoteSet)
    print("roundDowns",roundDowns)
    print("roundOffs",roundOffs)
    print("rankedRoundOffs",rankedRoundOffs)
    print("Subtract Hours:", subtractHours)
    print("LocToRem:", locToRem)
    print("---")
    print("---")
    print("---")
    print("firstSetup",firstSetup)
    print("finalSetup",finalSetup)


    adjusted_frequencies = {key: room_type_frequency.get(key, 0) - subtractHours.get(key, 0) + additionalHours.get(key, 0) for key in set(room_type_frequency) | set(subtractHours) | set(additionalHours)}
    print("Recommended Configuration:", adjusted_frequencies)

    # Calculate total_present_parts based on room_type_frequency
    for room_type, frequency in room_type_frequency.items():
        if room_type in parts:
            for part, quantity in parts[room_type].items():
                total_present_parts_initial[part] = total_present_parts_initial.get(part, 0) + quantity * frequency

    # Calculate total_present_parts based on adjusted_frequencies
    for room_type, frequency in adjusted_frequencies.items():
        if room_type in parts:
            for part, quantity in parts[room_type].items():
                total_present_parts_adjusted[part] = total_present_parts_adjusted.get(part, 0) + quantity * frequency

    # Calculate changes in part quantities
    for part in set(total_present_parts_initial.keys()) | set(total_present_parts_adjusted.keys()):
        initial_qty = total_present_parts_initial.get(part, 0)
        adjusted_qty = total_present_parts_adjusted.get(part, 0)
        change = adjusted_qty - initial_qty
        if change != 0:
            parts_changes[part] = change

    #print("Total Present Parts (Initial):", total_present_parts_initial)
    #print("Total Present Parts (Adjusted):", total_present_parts_adjusted)
    #print("Parts Changes:", parts_changes)

    total_price_difference = 0
    for part, change in parts_changes.items():
        if part in dealerprices:
            if change > 0:
                part_price = price_to_float(dealerprices[part])
                newprice = part_price*1.33
                total_price_difference += newprice * change
            elif change < 0:
                part_price = price_to_float(dealerprices[part])
                newprice = part_price*1.33/5
                print(part,newprice)
                total_price_difference += newprice * change
            else:
                print("SVEEENLETTTOPPPPP",change)

    # Format the total price difference as a string with two decimal places
    total_price_difference_str = "€{:.2f}".format(total_price_difference)

    #print("Total Price Difference:", total_price_difference_str)
    ordered_room_freq = {k: room_type_frequency[k] for k in ordered_keys if k in room_type_frequency}
    ordered_adjusted = {k: adjusted_frequencies[k] for k in ordered_keys if k in adjusted_frequencies}

    room_freq_df = pd.DataFrame(list(ordered_room_freq.items()), columns=['Part', 'Quantity'])
    adjusted_freq_df = pd.DataFrame(list(ordered_adjusted.items()), columns=['Part', 'Quantity'])
    initial_parts_df = pd.DataFrame(list(total_present_parts_initial.items()), columns=['Part', 'Quantity'])
    adjusted_parts_df = pd.DataFrame(list(total_present_parts_adjusted.items()), columns=['Part', 'Quantity'])

    # Create a new dictionary for delta
    delta = {}

    # Iterate over the keys in the additions dictionary
    for key in additionalHours:
        # Calculate the change by subtracting the value in reductions from the value in additions
        # If the key is not found in reductions, it defaults to 0
        change = additionalHours[key] - subtractHours.get(key, 0)
        # Store the calculated change in the delta dictionary
        delta[key] = change

    dats = [{'Item': item, 'Quantity': quantity} for item, quantity in parts_changes.items()]

    # Create a DataFrame from the list of dictionaries
    df3 = pd.DataFrame(dats)

    delta_list = list(delta.items())
    

    # Convert the list of tuples to a DataFrame
    delta_df = pd.DataFrame(delta_list, columns=['Part', 'Value'])
    print("DELTAAAAA",delta)

    ordered_add = {k: additionalHours[k] for k in ordered_keys}

    # Create blank DataFrame for separation
    blank_df = pd.DataFrame({'': [''] * len(adjusted_parts_df)})

    # Concatenate all DataFrames with blank columns in between
    final_df = pd.concat([initial_parts_df, blank_df, adjusted_parts_df, blank_df.copy(), df3], axis=1)

    total_occupancies = sum(cumulative_occupancy_frequency.values())
    occupancy_percentages = {occupant: (count / total_occupancies) * 100 for occupant, count in cumulative_occupancy_frequency.items()}

    # Prepare data for cumulative percentages
    occupants = sorted(int(k) for k in occupancy_percentages.keys())
    percentages = list(occupancy_percentages.values())
    cumulative_percentages = [sum(percentages[:i+1]) for i in range(len(percentages))]


    cumdf = pd.DataFrame({
        "Occupants": occupants,
        "Percentage": [f"{p:.2f}%" for p in percentages],
        "Cumulative Percentage": [f"{cp:.2f}%" for cp in cumulative_percentages]
    })


    # Calculate the weighted sum of occupants
    weighted_sum_occupants = sum(occupancy_level * count for occupancy_level, count in cumulative_occupancy_frequency.items())

    # Calculate the total number of occupied intervals
    total_occupied_intervals = sum(cumulative_occupancy_frequency.values())

    # Calculate the average number of occupants when occupied
    if total_occupied_intervals > 0:  # Ensure there's at least one occupied interval to avoid division by zero
        average_occupants_when_occupied = weighted_sum_occupants / total_occupied_intervals
        print(f"Average Number of Occupants When Occupied (Across All Rooms): {average_occupants_when_occupied:.2f}")
    else:
        print("No occupied intervals found across all rooms.")


    # Calculate the total number of occupancies across all weekdays
    total_day_occupancies = sum(weekday_occupancy_counts.values())

    # Calculate percentages for each weekday
    weekday_percentages = {weekday: (count / total_day_occupancies) * 100 for weekday, count in weekday_occupancy_counts.items()}

    # Convert weekday numbers to names for readability
    weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_percentages_named = {weekday_names[weekday]: f"{percentage:.2f}%" for weekday, percentage in weekday_percentages.items()}

    total_non_zero_occupancies = sum(cumulative_occupancy_frequency.values())
    
    if total_intervals > 0:  # Ensure there is at least one interval to avoid division by zero
        persventage_occupied = (total_non_zero_occupancies / total_intervals) * 100

    num_rooms = len(file_list)

    # Step 2: Count intervals where all rooms are occupied
    intervals_all_occupied = sum(1 for occupancies in interval_occupancy_data.values() if sum(occupancies) == num_rooms)
    #st.write(interval_occupancy_data)

    fully_occupied_intervals = {
        interval: occupancies
        for interval, occupancies in interval_occupancy_data.items()
        if len([occ for occ in occupancies if occ > 0]) == num_rooms
    }

    # Create a DataFrame from the filtered intervals
    df_fully_occupied = pd.DataFrame(list(fully_occupied_intervals.keys()), columns=['Interval'])

    # Optionally, add more information, such as non-zero occupancy counts for each interval
    df_fully_occupied['Non-Zero Occupancy Counts'] = [
        [occ for occ in occupancies if occ > 0] for occupancies in fully_occupied_intervals.values()
    ]

    #print(f"Number of intervals where no room is available (all occupied): {intervals_all_occupied}")


    # Display the DataFrame as a table in Streamlit
    
    #col1, col2 = st.columns(2)

    # Display the first table with a title in the first column
    #with col1:
        #st.subheader("Current\nConfiguration")
        #st.table(room_freq_df)

    # Display the second table with a title in the second column
    #with col2:
        #st.subheader("Recommended\nConfiguration")
        #st.table(adjusted_freq_df)
    #st.subheader("Locations before")
    #st.write(locations)
    #st.subheader("Locations after")
    #st.write(finalSetup)
    #st.subheader("Additions")
    #st.write(ordered_add)
    #st.subheader("Reductions")
    #st.write(subtractHours)
    #left_co, cent_co,last_co = st.columns(3)
    #with cent_co:
        #st.subheader("Delta Table")
        #st.write(delta_df)
    #st.subheader("Rooms to add")
    #st.write(roundDowns)
    #st.subheader("Rooms to remove")
    #st.write(locView)
    #st.subheader("Total Present")
    #st.table(initial_parts_df)
    #st.subheader("Total Needed")
    #st.table(adjusted_parts_df)
    #st.write("Changes",parts_changes)
    #st.write("Total Price Difference:", total_price_difference_str)
    #csv = convert_df_to_csv(final_df)
    st.subheader("Total")
    if persventage_occupied < 33.3:
        zin = "too low"
    elif persventage_occupied < 66.7:
        zin = "healthy"
    else:
        zin = "too high"
    st.write(f"Your spaces have been occupied {persventage_occupied:.2f}% of the time. This average is deemed as {zin}.")
    st.table(cumdf)
    st.write("Percentage of Occupancies by Weekday:")
    st.write(weekday_percentages_named)
    #st.write("Occupancy Distribution:")
    #st.write(occupancy_percentages)
    st.write("Average occupancy when in use:", f"{average_occupants_when_occupied:.2f}")
    #data_rows = [analyze_mos_file(file) for file in file_list]
    mos_summary_df = pd.DataFrame(data_rows)
    st.table(mos_summary_df)
    
    
    
    

#days = 55
#hours = 8
#total_hours = days*hours
#capacity_needed = total_hours*0.75
#print("Total Hours & Capacity Needed", total_hours, capacity_needed)

#load_data_overview('datas/*')
# Function to convert DataFrame to CSV for downloading
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

def sven(files=None):
    """Function to display the first 5 rows of every uploaded CSV file."""
    if files is not None:
        for file in files:
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(file)
            
            # Display the file name and the first 5 rows of the DataFrame
            st.write(f"First 5 rows of {file.name}:")
            st.dataframe(df.head())

    else:
        # Perform a random action if no files are uploaded
        st.write("Performing a random action.")

def main():
    st.title("Welcome Knoed!")
    # File uploader widget
    uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, type=['csv'])

    # Include Weekends checkbox
    include_weekends = st.checkbox("Include Weekends")

    # Show 'Go with Files' button only if files are uploaded
    if uploaded_files:
        go_with_files = st.button("Go with Files")

        if go_with_files:
            load_data_overview(uploaded_files, include_weekends)

    # 'Go Random' button is always visible
    go_random = st.button("Go Random")
    if go_random:
        load_data_overview("random", include_weekends)

if __name__ == '__main__':
    main()
