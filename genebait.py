import pandas as pd
import random
import os
import numpy as np


def generate_dataframes_based_on_template(template_path):
    number_of_files = random.randint(13, 15)
    print(f"Number of DataFrames to generate: {number_of_files}")

    # Read the template CSV file to get the DateTime values
    template_df = pd.read_csv(template_path)

    dataframes = {}  # Using a dictionary to store DataFrames with their identifiers

    for file_number in range(1, number_of_files + 1):
        movie_list = ['BowOne', 'BowTwo', 'BowFour', 'BowSix', 'BowNine', 'BowTwelve']
        loclist = ['Studio', 'EG', 'Roffa', 'deStreetzzz', 'Ho Chi Minh-stad']

        # pick a random element from a list of strings
        movie = random.choice(movie_list)
        loc = random.choice(loclist)

        maximum_occupancy = {'BowOne': 1, 'BowTwo': 2, 'BowFour': 4, 'BowSix': 6, 'BowNine': 6, 'BowTwelve': 8}.get(movie, 0)

        # Construct DataFrame identifier
        df_identifier = f'Netherlands#Almelo#{loc}#{movie}-{file_number}'

        # Initialize DataFrame with the 'received_at' column from the template
        new_df = template_df[['DateTime']].copy()
        new_df.rename(columns={'DateTime': 'received_at'}, inplace=True)

        if maximum_occupancy < 4:
            # Generate a random occupancy percentage between 1 and 100
            occupancy_percentage = random.randint(1, 100)
            print(f"Occupancy Percentage: {occupancy_percentage}%")

            total_intervals = len(template_df)  # Total number of time intervals based on the template
            occupied_intervals = int((occupancy_percentage / 100) * total_intervals)  # Calculate number of occupied intervals

            # Generate occupancy numbers for occupied intervals, ensuring they are within the maximum occupancy limit
            occupancy_numbers = np.arange(1, maximum_occupancy + 1)
            repeats = occupied_intervals // len(occupancy_numbers)  # Number of times to repeat the occupancy range
            extra = occupied_intervals % len(occupancy_numbers)  # Extra occupancies to distribute

            # Repeat occupancy numbers and add extra to fully match the occupied_intervals count
            distributed_occupancies = np.tile(occupancy_numbers, repeats)
            if extra > 0:
                distributed_occupancies = np.append(distributed_occupancies, occupancy_numbers[:extra])

            # Shuffle to randomize distribution of occupancies across intervals
            np.random.shuffle(distributed_occupancies)

            # Initialize the 'people_counter_all' column with zeros
            new_df['people_counter_all'] = [0] * total_intervals

            # Randomly choose indices to place the occupied values, ensuring no duplicates
            occupied_indices = random.sample(range(total_intervals), occupied_intervals)

            # Place the distributed occupancies in the chosen indices
            for index, occupancy in zip(occupied_indices, distributed_occupancies):
                new_df.at[index, 'people_counter_all'] = occupancy
            dataframes[df_identifier] = new_df

        else:
            # Generate a random occupancy percentage, e.g., 80%
            occupancy_percentage = random.randint(1, 100)  # You can adjust the range as needed
            print(f"Occupancy Percentage: {occupancy_percentage}%")

            total_intervals = len(template_df)  # Total number of time intervals based on the template
            occupied_intervals = int((occupancy_percentage / 100) * total_intervals)  # Calculate number of occupied intervals

            # Generate occupancy numbers for occupied intervals
            occupancy_numbers = np.arange(1, maximum_occupancy + 1)
            repeats = occupied_intervals // len(occupancy_numbers)  # Number of times to repeat the occupancy range
            extra = occupied_intervals % len(occupancy_numbers)  # Extra occupancies to distribute

            # Repeat occupancy numbers and add extra to fully match the occupied_intervals count
            distributed_occupancies = np.tile(occupancy_numbers, repeats)
            if extra > 0:
                distributed_occupancies = np.append(distributed_occupancies, occupancy_numbers[:extra])

            # Shuffle to randomize distribution of occupancies across intervals
            np.random.shuffle(distributed_occupancies)

            # Create 'people_counter_all' column with 0s for empty intervals and distributed occupancies for others
            new_df['people_counter_all'] = [0] * (total_intervals - occupied_intervals) + distributed_occupancies.tolist()
            random.shuffle(new_df['people_counter_all'])  # Shuffle to mix empty and occupied intervals
            dataframes[df_identifier] = new_df
    
    return dataframes
