import pandas as pd
import numpy as np
from . import config

def load_data():
    """
    Loads data from CSV, processes player columns, and returns
    both the raw dataframe (df_data) and the cumulative dataframe (df).
    """
    if not os.path.exists(config.DATA_PATH):
        raise FileNotFoundError(f"Data file not found at {config.DATA_PATH}")

    df_data = pd.read_csv(config.DATA_PATH)
    
    # Add a guest column (sum of all guest scores)
    df_data['guest'] = df_data[config.GUESTS].sum(axis=1, min_count=1)
    
    all_players = config.BIG3 + config.GUESTS + ['guest']
    
    # Cumulative sum dataframe for plotting
    df = df_data[all_players].fillna(0).cumsum()
    
    # Mask non-played games
    df = df.mask(df_data[all_players].isna())
    
    # Add starting row at index -1 with all zeros
    start_row = pd.Series(0, index=all_players, name=-1)
    df = pd.concat([pd.DataFrame([start_row]), df]).sort_index()
    
    # Connection from 0 to first game for each player
    for p in all_players:
        first_idx = df_data[p].first_valid_index()
        if first_idx is not None and first_idx > 0:
            df.loc[first_idx - 1, p] = 0
            
    # Convert to Dollars (cents to dollars)
    df = df / 100
    
    # Add date object column to df_data for easier processing later
    df_data['date_obj'] = pd.to_datetime(df_data['date'], format='mixed', dayfirst=False)
    
    return df_data, df

def validate_data(df_data):
    """
    Validates that all game scores sum to zero.
    """
    all_players_check = config.BIG3 + config.GUESTS
    
    # Sum across player columns
    row_sums = df_data[all_players_check].sum(axis=1)
    
    non_zero_indices = row_sums[row_sums.abs() > 0.01].index # Use tolerance for potential float issues, though data is int usually
    
    if not non_zero_indices.empty:
        print("ALERT: Data entry errors found! The following rows do not sum to zero:")
        for idx in non_zero_indices:
            date = df_data.loc[idx, 'date']
            game_num = df_data.loc[idx, 'game_num']
            total = row_sums[idx]
            print(f"Row {idx}: Date {date}, Game {game_num} -> Sum: {total}")
        return False
    else:
        print("Data Validation Passed: All games sum to zero.")
        return True
import os
