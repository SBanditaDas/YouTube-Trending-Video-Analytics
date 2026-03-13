import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys
import os
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(filepath: str) -> pd.DataFrame:
    if not os.path.exists(filepath):
        logging.error(f"File not found: {filepath}")
        return pd.DataFrame()
    
    try:
        # Load the cleaned dataset, limit rows for performance if needed
        df = pd.read_csv(filepath)
        # Handle NA values
        df['tags'] = df['tags'].fillna('')
        df['title'] = df['title'].fillna('')
        df['description'] = df['description'].fillna('')
        return df
    except Exception as e:
        logging.error(f"Error loading file {filepath}: {e}")
        return pd.DataFrame()

def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create a single feature column combining title and tags."""
    if df.empty:
        return df
    
    # Combine title, tags and description into a single 'content' feature
    # Replace "|" in tags with spaces for better processing
    df['content'] = df['title'] + " " + df['tags'].str.replace('|', ' ', regex=False) + " " + df['description'].astype(str)
    return df

def recommend_videos(df: pd.DataFrame, video_title: str, top_n: int = 5):
    """Recommends top N similar videos based on a given video title."""
    if df.empty:
        return []

    # Drop duplicates for recommendation to avoid exact duplicates
    df_unique = df.drop_duplicates(subset=['title']).reset_index(drop=True)
    
    # Lowercase for robust matching
    df_unique['title_lower'] = df_unique['title'].str.lower()
    video_title_lower = video_title.lower()
    
    if video_title_lower not in df_unique['title_lower'].values:
        logging.warning(f"Video '{video_title}' not found in the dataset.")
        # Optional: You could implement fuzzy matching here to find the closest title
        return []

    # Get the index of the video that matches the title
    idx = df_unique[df_unique['title_lower'] == video_title_lower].index[0]

    # Initialize TF-IDF Vectorizer
    tfidf = TfidfVectorizer(stop_words='english')

    # Construct the required TF-IDF matrix by fitting and transforming the 'content' feature
    tfidf_matrix = tfidf.fit_transform(df_unique['content'])

    # Compute the cosine similarity between the given video and all others
    # For performance on large datasets, only compute similarity for the specific video
    cosine_sim = cosine_similarity(tfidf_matrix[idx:idx+1], tfidf_matrix).flatten()

    # Get scores of all videos
    sim_scores = list(enumerate(cosine_sim))

    # Sort the videos based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the scores of the `top_n` most similar videos (excluding itself)
    sim_scores = sim_scores[1:top_n+1]

    # Get the video indices
    video_indices = [i[0] for i in sim_scores]

    # Return the top N most similar videos
    recommendations = df_unique.iloc[video_indices][['title', 'channel_title', 'views', 'trending_date']]
    recommendations['similarity_score'] = [i[1] for i in sim_scores]
    return recommendations

def main():
    parser = argparse.ArgumentParser(description="YouTube Video Recommender")
    parser.add_argument("--video", type=str, required=True, help="Title of the video to base recommendations on.")
    parser.add_argument("--top_n", type=int, default=5, help="Number of recommendations to return.")
    args = parser.parse_args()

    clean_dir = os.path.join("data", "cleaned")
    input_path = os.path.join(clean_dir, "cleaned_youtube_data.csv")

    logging.info("Loading and preparing data...")
    df = load_data(input_path)
    if df.empty:
        return

    df_prepared = prepare_features(df)
    
    logging.info(f"Finding recommendations for: {args.video}")
    recs = recommend_videos(df_prepared, args.video, args.top_n)
    
    if len(recs) == 0:
         logging.info("No recommendations found.")
    else:
        print("\n--- TOP RECOMMENDATIONS ---\n")
        print(recs.to_string(index=False))

if __name__ == "__main__":
    main()
