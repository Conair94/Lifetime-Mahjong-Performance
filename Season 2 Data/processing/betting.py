import pandas as pd
import numpy as np
import os
from . import config

def prob_to_moneyline(prob, house_edge_multiplier=1.0):
    if prob <= 0: return 99999
    
    # Apply house edge
    implied_prob = prob * house_edge_multiplier
    if implied_prob >= 0.99: implied_prob = 0.99
    
    if implied_prob >= 0.5:
        # Negative Odds
        moneyline = - (implied_prob / (1 - implied_prob)) * 100
    else:
        # Positive Odds
        moneyline = ((1 - implied_prob) / implied_prob) * 100
        
    return int(round(moneyline))

def generate_odds(df_data):
    print("Checking if betting odds need generation...")
    
    # Check night count
    current_night_count = df_data['date'].nunique()
    previous_night_count = 0
    
    if os.path.exists(config.PROCESSED_NIGHT_COUNT_PATH):
        with open(config.PROCESSED_NIGHT_COUNT_PATH, "r") as f:
            try:
                previous_night_count = int(f.read().strip())
            except ValueError:
                previous_night_count = 0
    
    print(f"Current Nights: {current_night_count}, Previous Processed: {previous_night_count}")
    
    if current_night_count <= previous_night_count:
        print("No new nights detected. Skipping betting odds generation.")
        return

    print("New night detected! Generating betting odds...")

    # Identify player columns
    meta_cols = ['date', 'game_num', 'order_starting_at_east', 'fan', 'from_wall', 'dealer_win', 'tiles_remaining', 'date_obj', 'guest']
    player_cols = [c for c in df_data.columns if c not in meta_cols]
    
    # --- 1. Nightly Winner (Net Profit) ---
    nightly_results = df_data.groupby('date')[player_cols].sum()

    def get_nightly_winner(row):
        m = row.max()
        winners = row[row == m].index.tolist()
        # Tie-Breaker: Prefer Regulars (Connor/Helio/Sam) or first
        if 'sam' in winners: return 'sam'
        if 'connor' in winners: return 'connor'
        if 'helio' in winners: return 'helio'
        return winners[0]

    winners = nightly_results.apply(get_nightly_winner, axis=1)
    win_counts = winners.value_counts()
    total_nights = len(winners)
    probs = win_counts / total_nights

    # --- 2. Sam vs The World ---
    sam_prob = probs.get('sam', 0)
    field_prob = 1 - sam_prob
    
    sam_ml = prob_to_moneyline(sam_prob, config.HOUSE_EDGE)
    field_ml = prob_to_moneyline(field_prob, config.HOUSE_EDGE)
    
    sam_sign = "+" if sam_ml > 0 else ""
    field_sign = "+" if field_ml > 0 else ""

    # --- 3. High Hand of the Night ---
    max_fans = df_data.groupby('date')['fan'].max()
    over_fan_prob = (max_fans > config.FAN_THRESHOLD).mean()
    under_fan_prob = 1 - over_fan_prob
    
    over_fan_ml = prob_to_moneyline(over_fan_prob, config.HOUSE_EDGE)
    under_fan_ml = prob_to_moneyline(under_fan_prob, config.HOUSE_EDGE)
    
    over_fan_sign = "+" if over_fan_ml > 0 else ""
    under_fan_sign = "+" if under_fan_ml > 0 else ""

    # --- Generate Markdown Output ---
    # Calculate Next Friday 5PM
    last_date = df_data['date_obj'].max()
    days_ahead = (4 - last_date.weekday() + 7) % 7
    if days_ahead == 0:
        days_ahead = 7
    next_friday = last_date + pd.Timedelta(days=days_ahead)
    next_friday_str = next_friday.strftime('%B %d, %Y')

    md_content = f"# 🎲 Mahjong Nightly Betting Odds\n\n"
    md_content += f"**Date Generated:** {pd.Timestamp.now().strftime('%Y-%m-%d')}\n"
    md_content += f"**Basis:** {total_nights} Nights of Season 2 Data\n"
    md_content += f"**Place all bets before:** Friday, {next_friday_str} at 5:00 PM\n\n"
    
    md_content += "## 🏆 Nightly Winner (Net Profit)\n"
    md_content += "*Who will finish the night with the highest profit?*\n\n"
    md_content += "| Player | Money Line |\n"
    md_content += "| :--- | :--- |\n"
    
    for player, prob in probs.items():
        if player.lower() == 'nick': continue
        ml = prob_to_moneyline(prob, config.HOUSE_EDGE)
        sign = "+" if ml > 0 else ""
        md_content += f"| **{player.capitalize()}** | **{sign}{ml}** |\n"

    md_content += "\n## 🌍 Sam vs. The World\n"
    md_content += "*Will Sam win the night, or will anyone else take the crown?*\n\n"
    md_content += "| Selection | Money Line |\n"
    md_content += "| :--- | :--- |\n"
    md_content += f"| **Sam Wins** | **{sam_sign}{sam_ml}** |\n"
    md_content += f"| **The Field (Any Other Player)** | **{field_sign}{field_ml}** |\n"

    md_content += "\n## 🀄 Highest Hand Over/Under\n"
    md_content += f"*Will the highest scoring hand (Fan) of the night be Over or Under {config.FAN_THRESHOLD}?*\n\n"
    md_content += f"* **Over {config.FAN_THRESHOLD}**: **{over_fan_sign}{over_fan_ml}** ({over_fan_prob*100:.1f}%)\n"
    md_content += f"* **Under {config.FAN_THRESHOLD}**: **{under_fan_sign}{under_fan_ml}** ({under_fan_prob*100:.1f}%)\n"

    md_content += "\n---\n"
    md_content += "### 💡 How to Read Money Lines\n"
    md_content += "The Money Line is a way to express betting odds based on a $100 baseline:\n"
    md_content += "* **Positive Odds (+):** Indicates the underdog. The number represents the **profit** you would make on a $100 bet. (e.g., **+200** means a $100 bet wins $200 in profit, returning $300 total).\n"
    md_content += "* **Negative Odds (-):** Indicates the favorite. The number represents how much you need to **bet** to make $100 in profit. (e.g., **-150** means you must bet $150 to win $100 in profit, returning $250 total).\n"

    with open(config.BETTING_ODDS_PATH, 'w') as f:
        f.write(md_content)
    
    # Update counter file
    with open(config.PROCESSED_NIGHT_COUNT_PATH, "w") as f:
        f.write(str(current_night_count))
        
    print(f"Successfully generated odds to {config.BETTING_ODDS_PATH}")
