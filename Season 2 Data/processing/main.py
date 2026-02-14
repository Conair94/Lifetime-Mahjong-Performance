from . import data_loader
from . import plotting
from . import stats
from . import readme
from . import betting

def main():
    print("Starting Nightly Processing...")
    
    # 1. Load Data
    df_data, df = data_loader.load_data()
    
    # 2. Validate Data
    if not data_loader.validate_data(df_data):
        print("Warning: Data validation failed. Proceeding with caution...")
    
    # 3. Generate Plots
    plotting.generate_plots(df_data, df)
    
    # 4. Calculate Stats
    stats.calculate_player_stats(df_data)
    
    # 5. Update README
    readme.update_readme(df_data)
    
    # 6. Generate Betting Odds
    betting.generate_odds(df_data)
    
    print("Nightly Processing Complete!")

if __name__ == "__main__":
    main()
