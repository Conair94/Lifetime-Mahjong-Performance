import pandas as pd
import numpy as np
import os

def update_readme():
    data_path = 'data.csv'
    readme_path = '../README.md'
    
    if not os.path.exists(data_path):
        print(f"Error: {data_path} not found.")
        return

    df_data = pd.read_csv(data_path)
    
    # Recent Night Summary Logic
    df_data['date_obj'] = pd.to_datetime(df_data['date'], format='mixed', dayfirst=False)
    last_date = df_data['date_obj'].max()
    date_str = last_date.strftime('%m/%d/%Y') # Format as MM/DD/YYYY to match README

    recent_df = df_data[df_data['date_obj'] == last_date]
    games_count = len(recent_df)

    numeric_cols = df_data.select_dtypes(include=[np.number]).columns
    exclude = ['date', 'game_num', 'order_starting_at_east', 'fan', 'from_wall', 'dealer_win', 'tiles_remaining', 'date_obj', 'guest']
    players = [c for c in numeric_cols if c not in exclude]

    night_players = []
    for p in players:
        if not recent_df[p].isna().all():
            night_players.append(p)

    summary_data = []

    for p in night_players:
        profit = recent_df[p].sum()
        
        p_wins = recent_df[recent_df[p] > 0]
        hands_won = len(p_wins)
        
        if not p_wins.empty:
            max_hand = p_wins[p].max()
            high_hand_str = str(int(max_hand))
        else:
            high_hand_str = "0"

        history_df = df_data[df_data['date_obj'] < last_date]
        p_history = history_df[p].dropna()
        prev_stat = p_history.mean() if not p_history.empty else 0.0
        prev_std = p_history.std() if not p_history.empty else 1.0
        
        p_current = recent_df[p].dropna()
        curr_stat = p_current.mean()
        
        # Z-Score of the night's average performance
        if prev_std > 0:
            z_score = (curr_stat - prev_stat) / prev_std
        else:
            z_score = 0.0
            
        diff = curr_stat - prev_stat
        
        summary_data.append({
            'Player': p.capitalize(),
            'Net Profit': profit,
            'Highest Hand': high_hand_str,
            'Hands Won': hands_won,
            'Diff': diff,
            'Z-Score': z_score
        })

    summary_data.sort(key=lambda x: x['Net Profit'], reverse=True)

    # Generate Markdown Table
    new_content = f"### Most Recent Night: {date_str} ({games_count} Hands played)\n"
    new_content += "| Player | Net Profit | Highest Hand | Hands Won | Δ Avg Points per hand | Z-Score |\n"
    new_content += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"

    for row in summary_data:
        p = row['Player']
        prof = int(row['Net Profit'])
        hh = row['Highest Hand']
        won = row['Hands Won']
        diff = row['Diff']
        z = row['Z-Score']
        
        if prof > 0:
            prof_str = f"$\\color{{green}}{{+{prof}}}$"
        elif prof < 0:
            prof_str = f"$\\color{{red}}{{{prof}}}$"
        else:
            prof_str = f"{prof}"
            
        if diff > 0:
            diff_str = f"$\\color{{green}}{{+{diff:.2f}}}$"
        elif diff < 0:
            diff_str = f"$\\color{{red}}{{{diff:.2f}}}$"
        else:
            diff_str = f"{diff:.2f}"
            
        if z > 0:
            z_str = f"+{z:.2f}"
        else:
            z_str = f"{z:.2f}"
            
        new_content += f"| {p} | {prof_str} | {hh} | {won} | {diff_str} | {z_str} |\n"

    # Read README.md
    if not os.path.exists(readme_path):
        print(f"Error: {readme_path} not found.")
        return

    with open(readme_path, 'r') as f:
        readme_lines = f.readlines()

    # Find start and end indices for replacement
    start_index = -1
    end_index = -1
    
    for i, line in enumerate(readme_lines):
        if line.strip().startswith("### Most Recent Night:"):
            start_index = i
        elif start_index != -1 and line.strip().startswith("## ") and i > start_index:
             # Found the next section (e.g. ## Current Season Performance)
             end_index = i
             break
    
    if start_index != -1:
        if end_index == -1:
             # If no next section found, replace until end (or maybe just the table lines?)
             # Assuming standard format, we can just replace until end if it's the last section, 
             # but here we know there are subsequent sections.
             # If end_index is -1, it might mean we are at the end of file, but let's be safe.
             # We will just assume the table block ends when a new header starts or end of file.
             end_index = len(readme_lines)

        # Keep lines before start_index
        final_lines = readme_lines[:start_index]
        # Add new content
        final_lines.append(new_content)
        # Add newline if needed
        final_lines.append("\n")
        # Keep lines from end_index
        final_lines.extend(readme_lines[end_index:])
        
        with open(readme_path, 'w') as f:
            f.writelines(final_lines)
        print("README.md updated successfully.")
    else:
        print("Could not find '### Most Recent Night:' section in README.md")

if __name__ == "__main__":
    update_readme()
