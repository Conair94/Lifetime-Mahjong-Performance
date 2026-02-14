import matplotlib.pyplot as plt
import pandas as pd
import os
from . import config

def generate_plots(df_data, df):
    print("Generating plots...")
    
    # 1. Net Profit Chart (Big 3 + Guest Aggregate)
    _plot_net_profit(df_data, df)
    
    # 2. Guest Net Profit Chart
    _plot_guest_profit(df_data, df)
    
    # 3. Fan Distribution Histogram
    _plot_fan_distribution(df_data)
    
    # 4. Win Points Histograms (Self Drawn vs Non-Self Drawn)
    _plot_win_points_distribution(df_data)
    
    print("Plots generated successfully.")

def _plot_net_profit(df_data, df):
    ax1 = df[config.BIG3 + ['guest']].plot(figsize=(16, 9))
    ax1.set_title('Connor, Helio, and Sam versus Guest')
    
    _add_date_verticals(ax1, df_data)
    
    plt.grid(axis='y', linestyle='--')
    plt.xlabel("Game Number")
    plt.ylabel("Net Profit (in $USD)")
    plt.legend(bbox_to_anchor=(1.0, 1.0))
    
    output_path = os.path.join(config.BASE_DIR, "net_profit.png")
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def _plot_guest_profit(df_data, df):
    ax2 = df[config.GUESTS].plot(figsize=(16, 9))
    ax2.set_title('All Guests')
    
    _add_date_verticals(ax2, df_data)
    
    plt.grid(axis='y', linestyle='--')
    plt.xlabel("Game Number")
    plt.ylabel("Net Profit")
    plt.legend(bbox_to_anchor=(1.0, 1.0))
    
    output_path = os.path.join(config.BASE_DIR, "net_profit_guests.png")
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()

def _plot_fan_distribution(df_data):
    plt.figure(figsize=(10, 6))
    max_fan = df_data['fan'].max()
    if pd.isna(max_fan):
        max_fan = 0
    
    plt.hist(df_data['fan'].dropna(), bins=range(0, int(max_fan) + 2, 1), edgecolor='black', alpha=0.7)
    plt.title('Distribution of Winning Hand Sizes (Fan)')
    plt.xlabel('Fan')
    plt.ylabel('Frequency')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    output_path = os.path.join(config.BASE_DIR, "fan_distribution.png")
    plt.savefig(output_path, bbox_inches='tight')
    plt.close()

def _plot_win_points_distribution(df_data):
    current_players = config.BIG3 + config.GUESTS
    winning_points = df_data[current_players].max(axis=1)
    
    self_drawn_points = winning_points[df_data['from_wall'] == 1]
    discard_points = winning_points[df_data['from_wall'] == 0]
    
    # Self Drawn
    plt.figure(figsize=(10, 6))
    self_drawn_counts = self_drawn_points.dropna().value_counts().sort_index()
    if not self_drawn_counts.empty:
        plt.bar(self_drawn_counts.index, self_drawn_counts.values, width=10, edgecolor='black', alpha=0.7, color='green')
        plt.xticks(self_drawn_counts.index, rotation=45)
    
    plt.title('Distribution of Winning Hand Sizes (Points) - Self Drawn')
    plt.xlabel('Points')
    plt.ylabel('Frequency')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    output_path_sd = os.path.join(config.BASE_DIR, "win_points_self_drawn.png")
    plt.savefig(output_path_sd, bbox_inches='tight')
    plt.close()
    
    # Non-Self Drawn
    plt.figure(figsize=(10, 6))
    discard_counts = discard_points.dropna().value_counts().sort_index()
    if not discard_counts.empty:
        plt.bar(discard_counts.index, discard_counts.values, width=10, edgecolor='black', alpha=0.7, color='orange')
        plt.xticks(discard_counts.index, rotation=45)
        
    plt.title('Distribution of Winning Hand Sizes (Points) - Non-Self Drawn')
    plt.xlabel('Points')
    plt.ylabel('Frequency')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    output_path_nsd = os.path.join(config.BASE_DIR, "win_points_non_self_drawn.png")
    plt.savefig(output_path_nsd, bbox_inches='tight')
    plt.close()

def _add_date_verticals(ax, df_data):
    y_min, y_max = ax.get_ylim()
    date_changes = df_data.index[df_data['date'].ne(df_data['date'].shift())].tolist()
    for i in date_changes:
        if i == 0:
            plt.text(-1, y_max, df_data.loc[i, 'date'], rotation=90, verticalalignment='top', fontsize=10)
        else:
            plt.axvline(x=i-0.5, color='gray', linestyle='--', alpha=0.5)
            plt.text(i-0.5, y_max, df_data.loc[i, 'date'], rotation=90, verticalalignment='top', fontsize=10)
