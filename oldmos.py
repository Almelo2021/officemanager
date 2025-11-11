#oldmos.py

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

def get_max_occupancy(start_time, end_time, df):
    mask = (df['received_at'] >= start_time) & (df['received_at'] < end_time)
    filtered_df = df.loc[mask, 'people_counter_all']
    return 0 if filtered_df.empty else filtered_df.max()

def getdays(erin, dataframes, include_weekends=False):
    print("Transforming ",erin)
    try:
        df = pd.read_csv(erin)
    except Exception as error:
        print("svennnnx,",error)
        df = dataframes[erin]
    df['received_at'] = pd.to_datetime(df['received_at'])
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

def transformMOS(erin, eruit, additionalHours, subtractHours, room_type, locView, locToRem, dataframes, bear, include_weekends):
    print("Transforming ",erin)
    try:
        build = erin.name.split('#')[2]
    except:
        build = erin.split('#')[2]
    if bear is "random":
        df = dataframes[erin]
    else:
        erin.seek(0)
        df = pd.read_csv(erin)
        
    df['received_at'] = pd.to_datetime(df['received_at'])

    if not include_weekends:
        #st.write("Excluding Weekend Data...")
        # Filter out weekends: keep only rows where day of the week is less than 5 (Monday=0, Tuesday=1, ..., Friday=4)
        df = df[df['received_at'].dt.dayofweek < 5]

    df['date'] = df['received_at'].dt.date

    intervals_df = pd.DataFrame()

    for single_date in pd.date_range(start=df['date'].min(), end=df['date'].max(), freq='D'):
        datetime_range = pd.date_range(start=pd.Timestamp(single_date).replace(hour=8, minute=0),
                                       end=pd.Timestamp(single_date).replace(hour=18, minute=0),
                                       freq='30T')
        temp_df = pd.DataFrame({'DateTime': datetime_range, 'Occupancy': np.nan})
        intervals_df = pd.concat([intervals_df, temp_df], ignore_index=True)

    for i, row in intervals_df.iterrows():
        intervals_df.at[i, 'Occupancy'] = get_max_occupancy(row['DateTime'], row['DateTime'] + pd.Timedelta(minutes=30), df)

    intervals_df['Occupancy'].fillna(0, inplace=True)
    intervals_df.to_csv(eruit, index=False)

    occupancy_frequency = intervals_df['Occupancy'].value_counts().to_dict()
    #print("Occupancy Frequencies:", occupancy_frequency)
    st.write(occupancy_frequency)

    num_rows_non_zero = (intervals_df['Occupancy'] > 0).sum()
    percentage_non_zero = (num_rows_non_zero / len(intervals_df)) * 100
    st.write(f"Usage {room_type}: {percentage_non_zero:.2f}%")
    #print(f"Percentage of intervals where Occupancy is not 0: {percentage_non_zero:.2f}%")

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

def load_data(file_list, include_weekends=False):
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
        days = getdays( file_path, file_list, include_weekends)
        transformMOS(file_path, 'mossom.csv', additionalHours, subtractHours, room_type, locView, locToRem, file_list, bear, include_weekends)

    print("Locations",locations)
    print("locView",locView)

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
            part_price = price_to_float(dealerprices[part])
            total_price_difference += part_price * change

    # Format the total price difference as a string with two decimal places
    total_price_difference_str = "€{:.2f}".format(total_price_difference)

    #print("Total Price Difference:", total_price_difference_str)

    room_freq_df = pd.DataFrame(list(room_type_frequency.items()), columns=['Part', 'Quantity'])
    adjusted_freq_df = pd.DataFrame(list(adjusted_frequencies.items()), columns=['Part', 'Quantity'])
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

    

    # Display the DataFrame as a table in Streamlit
    st.subheader("Current Configuration")
    st.table(room_freq_df)
    st.subheader("Recommended Configuration")
    st.table(adjusted_freq_df)
    st.subheader("Locations before")
    st.write(locations)
    st.subheader("Locations after")
    st.write(finalSetup)
    st.subheader("Additions")
    st.write(additionalHours)
    st.subheader("Reductions")
    st.write(subtractHours)
    st.subheader("Delta Table")
    st.write(delta)
    st.subheader("Rooms to add")
    st.write(roundDowns)
    st.subheader("Rooms to remove")
    st.write(locView)
    st.subheader("Total Present")
    st.table(initial_parts_df)
    st.subheader("Total Needed")
    st.table(adjusted_parts_df)
    st.write("Changes",parts_changes)
    st.write("Total Price Difference:", total_price_difference_str)
    
    

#days = 55
#hours = 8
#total_hours = days*hours
#capacity_needed = total_hours*0.75
#print("Total Hours & Capacity Needed", total_hours, capacity_needed)

#load_data('datas/*')

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
            load_data(uploaded_files, include_weekends)

    # 'Go Random' button is always visible
    go_random = st.button("Go Random")
    if go_random:
        load_data("random", include_weekends)

if __name__ == '__main__':
    main()
