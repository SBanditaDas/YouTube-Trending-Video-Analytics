import pandas as pd
import numpy as np
import os
import glob
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_and_combine_data(data_dir: str) -> pd.DataFrame:
    """Loads all CSV files from the given directory and combines them."""
    all_files = glob.glob(os.path.join(data_dir, "*.csv"))
    if not all_files:
        logging.warning(f"No CSV files found in {data_dir}")
        return pd.DataFrame()

    df_list = []
    for file in all_files:
        try:
            # Assuming files are named like USvideos.csv, GBvideos.csv
            country_code = os.path.basename(file)[:2]
            df = pd.read_csv(file, encoding='utf-8', on_bad_lines='skip')
            df['country'] = country_code
            df_list.append(df)
            logging.info(f"Loaded {os.path.basename(file)} with {len(df)} rows.")
        except Exception as e:
            logging.error(f"Error loading {file}: {e}")

    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)
        return combined_df
    return pd.DataFrame()

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Cleans the dataframe by handling missing values, duplicates, and standardizing columns."""
    if df.empty:
        return df

    initial_rows = len(df)
    
    # Drop completely duplicated rows
    df = df.drop_duplicates(subset=['video_id', 'trending_date'], keep='first')
    logging.info(f"Dropped {initial_rows - len(df)} duplicate records.")

    # Fill missing string values with empty string or 'Unknown'
    string_cols = ['title', 'channel_title', 'tags', 'description']
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].fillna('')

    # Convert dates to datetime if they exist
    if 'trending_date' in df.columns:
        # typical format: YY.DD.MM
        try:
            df['trending_date'] = pd.to_datetime(df['trending_date'], format='%y.%d.%m', errors='coerce')
        except:
            pass
            
    if 'publish_time' in df.columns:
        try:
            df['publish_time'] = pd.to_datetime(df['publish_time'], errors='coerce')
        except:
            pass

    return df

def main():
    raw_dir = os.path.join("data", "raw")
    clean_dir = os.path.join("data", "cleaned")
    
    # Ensure directories exist
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(clean_dir, exist_ok=True)

    logging.info("Starting data loading...")
    raw_df = load_and_combine_data(raw_dir)
    
    if raw_df.empty:
        logging.warning("No data returned. Add some datasets to data/raw/")
        return
        
    logging.info("Starting data cleaning...")
    cleaned_df = clean_data(raw_df)
    
    output_path = os.path.join(clean_dir, "cleaned_youtube_data.csv")
    cleaned_df.to_csv(output_path, index=False)
    logging.info(f"Saved cleaned data to {output_path}")

if __name__ == "__main__":
    main()
