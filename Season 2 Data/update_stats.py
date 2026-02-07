import pandas as pd
import numpy as np

# Load data
df_data = pd.read_csv("data.csv")

# Define players
guests = ['oscar','nick','drew','ruohan','brandon','lixin','alice']
big3 = ['connor','helio','sam']
all_players_list = big3 + guests

player_stats = []

for p in all_players_list:
    p_data = df_data[p].dropna()
    games_played = len(p_data)
    
    if games_played > 0:
        wins = p_data[p_data > 0]
        losses = p_data[p_data < 0]
        win_rate = len(wins) / games_played
        
        # Avg Fan when winning
        win_indices = wins.index
        avg_win_fan = df_data.loc[win_indices, 'fan'].mean()
        
        # Avg Points
        avg_win_points = wins.mean() if not wins.empty else 0
        avg_loss_points = losses.mean() if not losses.empty else 0
        
        # New Metrics
        net_profit = p_data.sum()
        expected_points = p_data.mean()
        
        player_stats.append({
            'Player': p.capitalize(),
            'Games Played': games_played,
            'Win Rate': win_rate,
            'Avg Win Fan': avg_win_fan if not pd.isna(avg_win_fan) else 0.0,
            'Avg Win Points': avg_win_points,
            'Avg Loss Points': avg_loss_points,
            'Net Profit': net_profit,
            'Expected Points Per Hand': expected_points
        })

# Guest Aggregate Stats
guest_series_list = [df_data[g].dropna() for g in guests]
guest_data = pd.concat(guest_series_list)
games_played = len(guest_data)

if games_played > 0:
    wins = guest_data[guest_data > 0]
    losses = guest_data[guest_data < 0]
    win_rate = len(wins) / games_played
    
    # Avg Fan
    win_indices = wins.index
    avg_win_fan = df_data.loc[win_indices, 'fan'].mean()
    
    avg_win_points = wins.mean() if not wins.empty else 0
    avg_loss_points = losses.mean() if not losses.empty else 0
    
    net_profit = guest_data.sum()
    expected_points = guest_data.mean()
    
    player_stats.append({
        'Player': 'Guest (aggregate)',
        'Games Played': games_played,
        'Win Rate': win_rate,
        'Avg Win Fan': avg_win_fan if not pd.isna(avg_win_fan) else 0.0,
        'Avg Win Points': avg_win_points,
        'Avg Loss Points': avg_loss_points,
        'Net Profit': net_profit,
        'Expected Points Per Hand': expected_points
    })

stats_df = pd.DataFrame(player_stats)
# Sort by Games Played descending
stats_df = stats_df.sort_values(by='Games Played', ascending=False)

# Format columns
# Win Rate: %
# Others: 1 decimal place usually, maybe 2 for Expected Points
stats_df['Win Rate'] = stats_df['Win Rate'].map(lambda x: f"{x:.2%}")
stats_df['Avg Win Fan'] = stats_df['Avg Win Fan'].map(lambda x: f"{x:.1f}")
stats_df['Avg Win Points'] = stats_df['Avg Win Points'].map(lambda x: f"{x:.1f}")
stats_df['Avg Loss Points'] = stats_df['Avg Loss Points'].map(lambda x: f"{x:.1f}")
stats_df['Net Profit'] = stats_df['Net Profit'].map(lambda x: f"{x:.1f}")
stats_df['Expected Points Per Hand'] = stats_df['Expected Points Per Hand'].map(lambda x: f"{x:.2f}")

# Save to CSV
stats_df.to_csv("player_stats.csv", index=False)
print("player_stats.csv updated successfully.")
