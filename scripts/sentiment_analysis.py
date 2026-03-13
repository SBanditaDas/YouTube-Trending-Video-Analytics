import pandas as pd
from textblob import TextBlob
import os
import logging
import nltk

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_sentiment(text: str) -> tuple:
    """Returns polarity and subjectivity using TextBlob."""
    if not isinstance(text, str) or not text.strip():
        return 0.0, 0.0
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def analyze_sentiment(df: pd.DataFrame) -> pd.DataFrame:
    """Applies sentiment analysis to title and tags."""
    if df.empty:
        return df
        
    logging.info("Analyzing sentiments of titles and tags... This might take a while.")
    
    if 'title' in df.columns:
        # Applying sentiment to title
        title_sentiments = df['title'].apply(get_sentiment)
        df['title_polarity'] = [x[0] for x in title_sentiments]
        df['title_subjectivity'] = [x[1] for x in title_sentiments]
        
    if 'tags' in df.columns:
         # Applying sentiment to tags
        tags_sentiments = df['tags'].apply(lambda x: get_sentiment(str(x).replace('|', ' ')))
        df['tags_polarity'] = [x[0] for x in tags_sentiments]
        df['tags_subjectivity'] = [x[1] for x in tags_sentiments]

    return df

def main():
    clean_dir = os.path.join("data", "cleaned")
    input_path = os.path.join(clean_dir, "cleaned_youtube_data.csv")
    output_path = os.path.join(clean_dir, "sentiment_youtube_data.csv")
    
    if not os.path.exists(input_path):
        logging.error(f"Input file not found: {input_path}")
        return

    logging.info(f"Loading cleaned data from {input_path}")
    df = pd.read_csv(input_path)
    
    df_with_sentiment = analyze_sentiment(df)
    
    df_with_sentiment.to_csv(output_path, index=False)
    logging.info(f"Saved sentiment-analyzed data to {output_path}")

if __name__ == "__main__":
    main()
