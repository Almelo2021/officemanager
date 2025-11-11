#app.py

from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import math
import io
import json
from genebait import generate_dataframes_based_on_template

app = Flask(__name__)

# All your existing dictionaries and configurations
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


def price_to_float(price_str):
    return float(price_str.replace('€', '').replace(',', '.'))

def get_max_occupancy(start_time, end_time, df):
    mask = (df['received_at'] >= start_time) & (df['received_at'] < end_time)
    filtered_df = df.loc[mask, 'people_counter_all']
    return 0 if filtered_df.empty else filtered_df.max()

def getdays(erin, dataframes, include_weekends=False):
    if isinstance(erin, str):
        df = pd.read_csv(erin)
    else:
        erin.seek(0)
        df = pd.read_csv(erin)

    df['received_at'] = pd.to_datetime(df['received_at'])
    df['date'] = df['received_at'].dt.date

    if include_weekends:
        days = df['date'].nunique()
    else:
        df['weekday'] = df['received_at'].dt.weekday
        days = df[df['weekday'].between(0, 4)]['date'].nunique()

    return days

def transformMOS(erin, eruit, additionalHours, subtractHours, room_type, locView, locToRem, dataframes, bear, include_weekends, usage_stats):
    try:
        build = erin.name.split('#')[2]
    except:
        build = erin.split('#')[2]
    
    if bear == "random":
        df = dataframes[erin]
    else:
        if isinstance(erin, str):               # <-- Live mode (filepath string)
            df = pd.read_csv(erin)
        else:                                   # <-- Uploaded file (BytesIO)
            erin.seek(0)
            df = pd.read_csv(erin)

        
    df['received_at'] = pd.to_datetime(df['received_at'])

    if not include_weekends:
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
    occupancy_frequency = intervals_df['Occupancy'].value_counts().to_dict()
    
    num_rows_non_zero = (intervals_df['Occupancy'] > 0).sum()
    percentage_non_zero = (num_rows_non_zero / len(intervals_df)) * 100
    
    usage_stats[room_type] = {
        'percentage': round(percentage_non_zero, 2),
        'occupancy_frequency': occupancy_frequency
    }

    # Additional aggregated usage metrics
    intervals_df['Hour'] = intervals_df['DateTime'].dt.hour
    intervals_df['Weekday'] = intervals_df['DateTime'].dt.day_name()

    # Mean occupancy by hour
    hourly_avg = intervals_df.groupby('Hour')['Occupancy'].mean().round(2).to_dict()

    # Mean occupancy by weekday
    weekday_avg = intervals_df.groupby('Weekday')['Occupancy'].mean().round(2).to_dict()

    usage_stats[room_type].update({
        'hourly_avg': hourly_avg,
        'weekday_avg': weekday_avg,
        'timeline': intervals_df[['DateTime', 'Occupancy']].to_dict(orient='records')
    })


    previous_occupancy = None
    
    if percentage_non_zero > addifabove or percentage_non_zero < removeifbelow:
        for occupancy in intervals_df['Occupancy']:
            if occupancy == 1:
                if previous_occupancy is not None:
                    if previous_occupancy == 0:
                        additionalHours['BowOne'] += 1
                        if 'BowOne' in additionalHoursLocal[build]:
                            additionalHoursLocal[build]['BowOne'] += 1
                        else:
                            additionalHoursLocal[build]['BowOne'] = 1
                    elif previous_occupancy == 1:
                        additionalHours['BowTwo'] += 1
                        if 'BowTwo' in additionalHoursLocal[build]:
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

        previous_occupancy = occupancy

        room_key = room_type
        uniqLoc = build+"$"+room_type
        locToRem[build][room_type] += 1
        if room_key in subtractHours:
            subtractHours[room_key] += 1
        if uniqLoc in locView:
            locView[uniqLoc] += 1
        else:
            locView.update({uniqLoc: 1})

def load_data(file_list, include_weekends=False):
    global additionalHoursLocal
    additionalHoursLocal = {}
    
    if file_list == "random":
        file_list = generate_dataframes_based_on_template(template_path='mossom.csv')
        bear = "random"
    else:
        bear = "files"
    
    room_type_frequency = {}
    locations = {}
    usage_stats = {}
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

    total_present_parts_initial = {}
    total_present_parts_adjusted = {}
    parts_changes = {}
    
    for file_path in file_list:
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

        days = getdays(file_path, file_list, include_weekends)
        transformMOS(file_path, 'mossom.csv', additionalHours, subtractHours, room_type, locView, locToRem, file_list, bear, include_weekends, usage_stats)

    print("Locations",locations)
    print("locView",locView)

    hours = 8
    print(days,"Days")
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

    total_price_difference = 0
    for part, change in parts_changes.items():
        if part in dealerprices:
            part_price = price_to_float(dealerprices[part])
            total_price_difference += part_price * change

    # Format the total price difference as a string with two decimal places
    total_price_difference_str = "€{:.2f}".format(total_price_difference)

    # Create a new dictionary for delta
    delta = {}

    # Iterate over the keys in the additions dictionary
    for key in additionalHours:
        # Calculate the change by subtracting the value in reductions from the value in additions
        # If the key is not found in reductions, it defaults to 0
        change = additionalHours[key] - subtractHours.get(key, 0)
        # Store the calculated change in the delta dictionary
        delta[key] = change

    return {
        'days': days,
        'current_config': room_type_frequency,
        'recommended_config': adjusted_frequencies,
        'locations_before': locations,
        'locations_after': finalSetup,
        'additions': additionalHours,
        'reductions': subtractHours,
        'delta': delta,
        'rooms_to_add': roundDowns,
        'rooms_to_remove': locView,
        'total_present': total_present_parts_initial,
        'total_needed': total_present_parts_adjusted,
        'parts_changes': parts_changes,
        'total_price_difference': total_price_difference_str,
        'usage_stats': usage_stats
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    include_weekends = request.form.get('include_weekends') == 'true'
    mode = request.form.get('mode')
    
    if mode == 'live':
        live_files = [
            "Netherlands#Almelo#Ho Chi Minh-stad#BowSix-2 (1).csv",
            "Netherlands#Almelo#Studio#BowFour-11 (1).csv",
            "Netherlands#Almelo#Ho Chi Minh-stad#BowNine-15_balanced (2).csv",
            "Netherlands#Almelo#Ho Chi Minh-stad#BowNine-15_balanced (1).csv",
            "Netherlands#Almelo#Studio#BowNine-12_balanced (1).csv",
            "Netherlands#Almelo#EG#BowOne-3 (1).csv",
            "Netherlands#Almelo#deStreetzzz#BowFour-9 (1).csv"
        ]
        results = load_data(live_files, include_weekends)
    else:
        files = request.files.getlist('files')
        file_objects = []
        for file in files:
            file_objects.append(io.BytesIO(file.read()))
            file_objects[-1].name = file.filename
        results = load_data(file_objects, include_weekends)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run()
