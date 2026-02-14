import pandas as pd
import os
from . import config

def calculate_player_stats(df_data):
    print("Calculating player stats...")
    
    # 1. Average games per night
    games_per_night = df_data.groupby('date')['game_num'].max().mean()
    print(f"Avg games per night: {games_per_night:.2f}")

    # 2. Dealer Win Rate
    dealer_wins = df_data['dealer_win'].dropna()
    dealer_win_rate = dealer_wins.mean() if not dealer_wins.empty else 0
    print(f"Dealer Win Rate: {dealer_win_rate:.2%}")

    # 3. Self Draw Rate
    from_wall_counts = df_data['from_wall'].dropna()
    self_draw_rate = from_wall_counts.mean() if not from_wall_counts.empty else 0
    print(f"Self Draw Rate: {self_draw_rate:.2%}")

    player_stats = []
    all_players_list = config.BIG3 + config.GUESTS

    for p in all_players_list:
        if p not in df_data.columns:
            continue
            
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
            
            # Volatility (Standard Deviation)
            volatility = p_data.std()
            
            player_stats.append({
                'Player': p.capitalize(),
                'Games Played': games_played,
                'Win Rate': win_rate,
                'Avg Win Fan': f"{avg_win_fan:.1f}" if not pd.isna(avg_win_fan) else "0.0",
                'Avg Win Points': f"{avg_win_points:.1f}",
                'Avg Loss Points': f"{avg_loss_points:.1f}",
                'Net Profit': f"{int(p_data.sum())}",
                'Expected Points Per Hand': f"{p_data.mean():.2f}",
                'Volatility': f"{volatility:.2f}"
            })

    # Guest Aggregate Stats
    guest_series_list = [df_data[g].dropna() for g in config.GUESTS if g in df_data.columns]
    if guest_series_list:
        guest_data = pd.concat(guest_series_list)
        games_played = len(guest_data)
        if games_played > 0:
            wins = guest_data[guest_data > 0]
            losses = guest_data[guest_data < 0]
            win_rate = len(wins) / games_played
            
            win_indices = wins.index
            # Note: indices might be duplicated in guest_data, so we need to be careful.
            # However, df_data.loc[win_indices] works even with duplicates.
            avg_win_fan = df_data.loc[win_indices, 'fan'].mean()
            
            avg_win_points = wins.mean() if not wins.empty else 0
            avg_loss_points = losses.mean() if not losses.empty else 0
            
            volatility = guest_data.std()
            
            player_stats.append({
                'Player': 'Guest (aggregate)',
                'Games Played': games_played,
                'Win Rate': win_rate,
                'Avg Win Fan': f"{avg_win_fan:.1f}" if not pd.isna(avg_win_fan) else "0.0",
                'Avg Win Points': f"{avg_win_points:.1f}",
                'Avg Loss Points': f"{avg_loss_points:.1f}",
                'Net Profit': f"{int(guest_data.sum())}",
                'Expected Points Per Hand': f"{guest_data.mean():.2f}",
                'Volatility (Std)': f"{volatility:.2f}"
            })

    stats_df = pd.DataFrame(player_stats)
    if not stats_df.empty:
        stats_df = stats_df.sort_values(by='Games Played', ascending=False)
        stats_df['Win Rate'] = stats_df['Win Rate'].map(lambda x: f"{x:.2%}")
        
        stats_df.to_csv(config.STATS_CSV_PATH, index=False)
        print(f"player_stats.csv updated successfully at {config.STATS_CSV_PATH}")
    else:
        print("No stats to save.")
